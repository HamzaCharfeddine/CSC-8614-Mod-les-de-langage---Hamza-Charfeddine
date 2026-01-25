# TP5/agent/nodes/draft_reply.py
import json
from typing import Dict, List
import re

from langchain_ollama import ChatOllama

from TP5.agent.logger import log_event
from TP5.agent.state import AgentState, EvidenceDoc

PORT = "11434"
LLM_MODEL = "qwen2.5:7b-instruct"


def evidence_to_context(evidence: List[EvidenceDoc]) -> str:
    blocks = []
    for d in evidence:
        blocks.append(f"[{d.doc_id}] (type={d.doc_type}, source={d.source}) {d.snippet}")
    return "\n\n".join(blocks)


DRAFT_PROMPT = """\
SYSTEM:
Tu rédiges une réponse email institutionnelle et concise.
Tu t'appuies UNIQUEMENT sur le CONTEXTE.
Si le CONTEXTE est insuffisant, tu dois poser 1 à 3 questions précises (pas de suppositions).

RÈGLE OBLIGATOIRE : Chaque affirmation DOIT être suivie de [doc_X] où X est le numéro du document.
Exemple : "La médiathèque propose 3 modèles [doc_1]."

Si le CONTEXTE ne contient PAS l'information demandée, tu DOIS retourner :
{{
  "reply_text": "INFORMATION_MANQUANTE",
  "citations": []
}}

USER:
Email:
Sujet: {subject}
De: {sender}
Corps:
<
{body}
>>>

CONTEXTE:
{context}

Retourne UNIQUEMENT ce JSON (pas de Markdown):
{{
  "reply_text": "...",
  "citations": ["doc_1"]
}}
"""


def safe_mode_reply(state: AgentState, reason: str) -> str:
    # TODO: réponse prudente + demander infos manquantes
    return (
        f"Bonjour,\n\n"
        f"Je n'ai pas trouvé suffisamment d'informations pour répondre précisément à votre demande.\n"
        f"Pourriez-vous me fournir plus de détails ?\n\n"
        f"Cordialement."
    )


def call_llm(prompt: str) -> str:
    llm = ChatOllama(base_url=f"http://127.0.0.1:{PORT}", model=LLM_MODEL)
    resp = llm.invoke(prompt)
    return re.sub(r"<think>.*?</think>\s*", "", resp.content.strip(), flags=re.DOTALL).strip()


def draft_reply(state: AgentState) -> AgentState:
    log_event(state.run_id, "node_start", {"node": "draft_reply"})

    if not state.budget.can_step():
        log_event(state.run_id, "node_end", {"node": "draft_reply", "status": "budget_exceeded"})
        return state

    state.budget.steps_used += 1

    if not state.evidence and state.decision.needs_retrieval:
        state.last_draft_had_valid_citations = False
        state.draft_v1 = safe_mode_reply(state, "no_evidence")
        log_event(state.run_id, "node_end", {"node": "draft_reply", "status": "safe_mode", "reason": "no_evidence"})
        return state
    
    context = evidence_to_context(state.evidence)
    prompt = DRAFT_PROMPT.format(subject=state.subject, sender=state.sender, body=state.body, context=context)
    raw = call_llm(prompt)

    try:
        data = json.loads(raw)
        reply_text = data.get("reply_text", "").strip()
        citations = data.get("citations", [])
    except Exception as e:
        state.add_error(f"draft_reply json parse error: {e}")
        state.last_draft_had_valid_citations = False
        state.draft_v1 = safe_mode_reply(state, "invalid_json")
        log_event(state.run_id, "node_end", {"node": "draft_reply", "status": "safe_mode", "reason": "invalid_json"})
        return state

    valid_ids = {d.doc_id for d in state.evidence}
    if (not citations or any(c not in valid_ids for c in citations)) and state.decision.needs_retrieval:
        state.last_draft_had_valid_citations = False
        state.draft_v1 = safe_mode_reply(state, "invalid_citations")
        log_event(state.run_id, "node_end", {"node": "draft_reply", "status": "safe_mode", "reason": "invalid_citations"})
        return state


    state.last_draft_had_valid_citations = True
    state.draft_v1 = reply_text
    log_event(state.run_id, "node_end", {"node": "draft_reply", "status": "ok", "n_citations": len(citations)})
    return state