# TP5/agent/nodes/finalize.py
import re
from typing import List

from TP5.agent.logger import log_event
from TP5.agent.state import AgentState

RE_CIT = re.compile(r"\[(doc_\d+)\]")

def _extract_citations(text: str) -> List[str]:
    return sorted(set(RE_CIT.findall(text or "")))

def finalize(state: AgentState) -> AgentState:
    log_event(state.run_id, "node_start", {"node": "finalize"})

    intent = state.decision.intent

    if intent == "reply":
        cits = _extract_citations(state.draft_v1)
        state.final_kind = "reply"
        if cits:
            state.final_text = state.draft_v1.strip() + "\n\nSources: " + " ".join(f"[{c}]" for c in cits)
        else:
            state.final_text = state.draft_v1.strip() or "Bonjour,\n\nJe reviens vers vous prochainement.\n\nCordialement."

    elif intent == "ask_clarification":
        state.final_kind = "clarification"
        state.final_text = state.draft_v1.strip() or "Bonjour,\n\nPouvez-vous préciser votre demande ?\n\nMerci."

    elif intent == "escalate":
        state.final_kind = "handoff"
        state.actions.append({
            "type": "handoff_packet",
            "run_id": state.run_id,
            "email_id": state.email_id,
            "summary": f"Escalade pour email {state.email_id} (catégorie: {state.decision.category}, risque: {state.decision.risk_level})",
            "evidence_ids": [d.doc_id for d in state.evidence],
        })
        state.final_text = "Votre demande nécessite une validation humaine. Je transmets avec un résumé et les sources."

    else:  # ignore
        state.final_kind = "ignore"
        state.final_text = "Email ignoré (hors périmètre)."

    log_event(state.run_id, "node_end", {"node": "finalize", "status": "ok", "final_kind": state.final_kind})
    return state