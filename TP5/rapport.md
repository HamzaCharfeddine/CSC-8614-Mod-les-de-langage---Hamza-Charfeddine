# TP5 - IA Agentique

- Nom: Charfeddine
- Prénom: Hamza
- Date: 16/01/2026

## Mise en place de TP5

> *python TP4/rag_answer.py "Combien de nouveaux modèles de liseuses sont disponibles à la médiathèque ?"*

![Screenshot](/TP5/img/P1.jpg)


```
[QUESTION]
Combien de nouveaux modèles de liseuses sont disponibles à la médiathèque ?
================================================================================
[ANSWER]
Trois nouveaux modèles de liseuses sont disponibles à la médiathèque : Elipsa 2, Libra Colour et Clara BW. [doc_1]
================================================================================

[SOURCES RETRIEVED]
- doc_1: (email) 202512_newsletter_de_la_mdiathque_-_janvier_2026_3012152423.md
- doc_2: (admin_pdf) Reglement_Interieur_TSP_valide_conseil_ecole_27_novembre_2025.pdf
- doc_3: (email) 202512_une_information_rglementaire_est_disponible_dans_votre_messagerie_scurise_6400249566.md
- doc_4: (email) 202512_notice_rapport_de_fin_dtudes_en_entreprise_1265602119.md
- doc_5: (admin_pdf) Reglement_Interieur_TSP_valide_conseil_ecole_27_novembre_2025.pdf
```

## Constituer un jeu de test

- La liste des 10 mails : 'E01.md' .jusqu'à 'E10.md'

![Screenshot](/TP5/img/P2_1.jpg)

- La majorité de ce jeu de test a été générée par ChatGPT et couvre des cas variés:
emails administratifs (attestation, inscription), pédagogiques (organisation de cours,
évaluation), recherche (réunion, paper), ainsi que des situations ambiguës nécessitant
une clarification. Il inclut également des emails à risque, notamment des demandes de
données personnelles et une tentative de prompt injection.

> *python TP5/load_test_emails.py*


![Screenshot](/TP5/img/P3.jpg)


## Implémenter le State typé (Pydantic) et un logger JSONL (run events)

![Screenshot](/TP5/img/P4.jpg)

> *python -m TP5.agent.test_logger*

```
{"run_id": "TEST_RUN", "ts": "2026-01-23T07:52:46.752358Z", "event": "node_start", "data": {"node": "classify_email"}}
{"run_id": "TEST_RUN", "ts": "2026-01-23T07:52:46.753359Z", "event": "node_end", "data": {"node": "classify_email", "status": "ok"}}
```

![Screenshot](/TP5/img/P5.jpg)

## Router LLM

> *python -m TP5.test_router*

![Screenshot](/TP5/img/P6.jpg)

- Dans *TP5\runs\1af5c426-532e-452e-add9-6ab2e6353c16.jsonl* :

![Screenshot](/TP5/img/P7.jpg)

## LangGraph : routing déterministe et graphe minimal (MVP)

> *pip freeze --all*

![Screenshot](/TP5/img/P8.jpg)

> *python -m TP5.test_graph_minimal*


![Screenshot](/TP5/img/P9.jpg)

- Dans *TP5\runs\8a1e3404-7d66-49d8-bc72-3084f3ca1e63.jsonl* :

![Screenshot](/TP5/img/P10.jpg)

## Tool use : intégrer votre RAG comme outil (retrieval + evidence)

> *python -m TP5.test_graph_minimal*

![Screenshot](/TP5/img/P11.jpg)

- Lors de l’exécution de test_graph_minimal sur l’email E01, la décision produite par le nœud classify_email indique needs_retrieval = false.

- Par conséquent, le nœud maybe_retrieve est ignoré et aucun appel au tool RAG n’est effectué. Le champ retrieval_query est vide et le state final ne contient pas d’evidence.

## Génération : rédiger une réponse institutionnelle avec citations

![Screenshot](/TP5/img/P12.jpg)

- Dans `10349f02-308d-45cc-8c4f-9428b1071c29`:

```
{"run_id": "10349f02-308d-45cc-8c4f-9428b1071c29", "ts": "2026-01-24T23:42:05.765007Z", "event": "node_start", "data": {"node": "classify_email", "email_id": "E11"}}
{"run_id": "10349f02-308d-45cc-8c4f-9428b1071c29", "ts": "2026-01-24T23:44:23.455021Z", "event": "node_end", "data": {"node": "classify_email", "status": "ok", "decision": {"intent": "reply", "category": "admin", "priority": 3, "risk_level": "low", "needs_retrieval": false, "retrieval_query": "", "rationale": "Email administratif standard nécessitant une réponse."}}}
{"run_id": "10349f02-308d-45cc-8c4f-9428b1071c29", "ts": "2026-01-24T23:44:23.458021Z", "event": "node_start", "data": {"node": "maybe_retrieve"}}
{"run_id": "10349f02-308d-45cc-8c4f-9428b1071c29", "ts": "2026-01-24T23:44:26.226897Z", "event": "tool_call", "data": {"tool": "rag_search", "args_hash": "3e26a1bca103", "latency_ms": 2766, "status": "ok", "k": 5, "n_docs": 5}}
{"run_id": "10349f02-308d-45cc-8c4f-9428b1071c29", "ts": "2026-01-24T23:44:26.230904Z", "event": "node_end", "data": {"node": "maybe_retrieve", "status": "ok", "n_docs": 5}}
{"run_id": "10349f02-308d-45cc-8c4f-9428b1071c29", "ts": "2026-01-24T23:44:26.232901Z", "event": "node_start", "data": {"node": "draft_reply"}}
{"run_id": "10349f02-308d-45cc-8c4f-9428b1071c29", "ts": "2026-01-24T23:50:29.600378Z", "event": "node_end", "data": {"node": "draft_reply", "status": "ok", "n_citations": 1}}
```

- La génération avec retrieval fonctionne correctement. L'agent récupère les documents pertinents via Chroma et génère des réponses correctes basées sur les données indexées. La principale limitation identifiée est la fiabilité du routeur LLM pour décider needs_retrieval=true. Dans l'exemple, j'ai ajouté `tate.decision.needs_retrieval = True` dans maybe_retrieve.py.


## Boucle contrôlée : réécriture de requête et 2e tentative de retrieval

- Le modèle `qwen2.5:7b-instruct` génère systématiquement des citations valides même lorsque les documents récupérés ne contiennent pas l'information demandée. Cela empêche le mécanisme de retry de se déclencher naturellement. Ce problème a persisté même en modifiant le prompt.

![Screenshot](/TP5/img/P14.jpg)

![Screenshot](/TP5/img/P13.jpg)

## Finalize + Escalade (mock) : sortie propre, actionnable, et traçable

![Screenshot](/TP5/img/P15.jpg)

![Screenshot](/TP5/img/P16.jpg)


## Robustesse & sécurité : budgets, allow-list tools, et cas “prompt injection”

![Screenshot](/TP5/img/P17.jpg)

![Screenshot](/TP5/img/P18.jpg)


## Évaluation pragmatique

> *python -m TP5.run_batch*

![Screenshot](/TP5/img/P19.jpg)

![Screenshot](/TP5/img/P20.jpg)


| email_id | subject | intent | category | risk | final_kind | tool_calls | retrieval_attempts | notes |
|---|---|---|---|---|---|---:|---:|---|
| E01 | Demande d’attestation de scolarité | reply | admin | low | reply | 0 | 0 | run=5acb222d-01d9-42eb-8621-ae3771393c61.jsonl |
| E02 | Inscription pédagogique – rappel | reply | admin | low | reply | 0 | 0 | run=1b55fa9d-a252-4f2b-b463-df3445cc277f.jsonl |
| E03 | Organisation des groupes – ENG8601 | reply | admin | low | reply | 0 | 0 | run=ae221cb9-fe9a-44a0-be07-9f17ef629b6b.jsonl |
| E04 | Évaluation CSC8607 | reply | teaching | low | reply | 0 | 0 | run=2328f27d-5654-4f82-9865-839915bdd64d.jsonl |
| E05 | Réunion projet de recherche | reply | research | low | reply | 0 | 0 | run=1c6db1df-596b-4b83-b976-e5789aea60f0.jsonl |
| E06 | Paper submission – minor revisions | reply | admin | low | reply | 0 | 0 | run=8b02a8c6-b038-4c9a-a7b5-5d0585257f0c.jsonl |
| E12 | URGENT: Mise à jour de sécurité | escalate | other | high | handoff | 0 | 0 | run=facde673-ae74-4f41-b79d-e43c2231975e.jsonl |
| E08 | Vérification urgente de votre compte | reply | admin | low | reply | 0 | 0 | run=ea042391-6920-4f18-a6fb-2bff4ef12c11.jsonl |
| E09 | Instruction spéciale | ignore | other | low | ignore | 0 | 0 | run=0f6f38f8-3647-43a2-8844-8fe672fc03c8.jsonl |
| E10 | Situation particulière – étudiant | reply | admin | low | reply | 0 | 0 | run=92d3e4b6-3147-45d9-8a1a-5f26776c24cf.jsonl |
| E11 | Information sur les liseuses de la médiathèque | reply | admin | low | reply | 0 | 0 | run=5d37e868-b3db-4fe1-bd7a-6282c93993ed.jsonl |
| E12 | Question très spécifique technique | reply | admin | low | reply | 0 | 0 | run=038556a4-a8a4-4dbe-b453-3425365ebd7d.jsonl |


**Observations sur les 12 emails testés :**

- **Intents dominants :** 10 `reply`, 1 `escalate`, 1 `ignore`
- **Catégories :** Majorité `admin` (8/12), puis `teaching` (2/12), `research` (1/12), `other` (1/12)
- **Escalades :** 1 seul cas (E12 - tentative de prompt injection détectée avec `risk_level=high`)
- **Tool calls :** 0 pour tous les emails car l'override de retrieval a été retiré après les tests
- **Limitation observée :** Le routeur LLM ne déclenche pas `needs_retrieval=true` de manière fiable, ce qui empêche le retrieval automatique en production

**Exemple de trajectoire simple (E11 - avec override) :**
```
classify_email → maybe_retrieve → draft_reply → check_evidence → finalize → END
(1 retrieval, 5 docs, génération avec citations valides)
```

**Architecture**

![Screenshot](/TP5/img/diagram.png)


## Trajectoires

### Exemple 1 : Run simple (E11 - liseuses médiathèque)

![Screenshot](/TP5/img/P12.jpg)

**Extrait JSONL (TP5/runs/10349f02-308d-45cc-8c4f-9428b1071c29.jsonl) :**
```json
{"event": "node_start", "data": {"node": "classify_email", "email_id": "E11"}}
{"event": "node_end", "data": {"node": "classify_email", "status": "ok"}}
{"event": "node_start", "data": {"node": "maybe_retrieve"}}
{"event": "tool_call", "data": {"tool": "rag_search", "status": "ok", "n_docs": 5}}
{"event": "node_start", "data": {"node": "draft_reply"}}
{"event": "node_end", "data": {"node": "draft_reply", "status": "ok", "n_citations": 1}}
```

**Trajectoire :** classify → maybe_retrieve (5 docs) → draft_reply (succès) → check_evidence (ok) → finalize → END. Pas de retry car citations valides dès la première tentative.

---

### Exemple 2 : Run avec escalade (E12 - prompt injection)

![Screenshot](/TP5/img/P17.jpg)

**Trajectoire :** classify → escalate (heuristique injection détectée) → stub_escalate → finalize (handoff_packet créé) → END. Aucun retrieval car `risk_level=high` détecté.

## Réflexion finale

**Ce qui fonctionne bien :**
- **Traçabilité complète** : Les logs JSONL permettent de reconstruire chaque trajectoire avec précision (nœuds, tools, latences, erreurs)
- **Intégration RAG ** : Le système récupère correctement les documents pertinents et génère des réponses basées sur les données indexées (vérifié avec E11 - liseuses)

**Points fragiles :**
- **Routeur LLM peu fiable** : Le modèle ne déclenche pas systématiquement `needs_retrieval=true` pour les emails, nécessitant un override manuel
- **Validation des citations** : Le LLM génère des citations même avec des documents non pertinents, empêchant la boucle de retry de se déclencher naturellement