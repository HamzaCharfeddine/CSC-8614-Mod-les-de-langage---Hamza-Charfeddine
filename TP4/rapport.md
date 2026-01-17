# TP3 - Retrieval-Augmented Generation (RAG)

- Nom: Charfeddine
- Prénom: Hamza
- Date: 16/01/2026

## Démarrage d'Ollama (local)

> *curl http://127.0.0.1:11434*

![Screenshot](/TP4/img/P1.jpg)

> *ollama pull qwen2.5:7b-instruct*

> *ollama run qwen2.5:7b-instruct "Réponds en français : donne 3 avantages du RAG."*

```
Voici trois avantages du RAG (Recherche Assistée par la Génération) :

1. Amélioration de l'accessibilité des informations :
Le RAG permet aux utilisateurs d'accéder rapidement et facilement à une grande quantité d'informations pertinentes, sans avoir besoin de naviguer dans un ensemble complexe de documents
ou de sites Web.

2. Personnalisation du contenu :
Grâce à l'intelligence artificielle, le RAG peut analyser les préférences et les besoins spécifiques de chaque utilisateur pour fournir des informations personnalisées et pertinentes.

3. Génération de contenu original :
Le RAG ne se contente pas de recycler ou d'extraire du texte existant ; il est capable de générer des réponses originales, créatives ou innovantes basées sur les données qu'il a
analysées, ce qui peut être particulièrement utile pour créer du contenu unique ou pour répondre à des questions complexes.
```

![Screenshot](/TP4/img/P2.jpg)

- Port utilisé : 11434 (local)
- Modèle : qwen2.5:7b-instruct

![Screenshot](/TP4/img/P3.jpg)

## Constituer le dataset et installer les dépendances

![Screenshot](/TP4/img/P4.jpg)

> *python download_emails_imap.py*

![Screenshot](/TP4/img/P7.jpg)

> *ls data/emails*

![Screenshot](/TP4/img/P5.jpg)

> *Get-Content data/emails\202512_pfe_sujets_additionnels_7779381635.md -TotalCount 20*

![Screenshot](/TP4/img/P6.jpg)

## Indexation

> *python TP4/build_index.py*

![Screenshot](/TP4/img/P8.jpg)

> *ls TP4\chroma_db*

![Screenshot](/TP4/img/P9.jpg)

## Retrieval

```TOP_K = 5```

> *python TP4/test_retrieval.py "Quels sont les sujets de PFE supplémentaires proposés par Luca Benedetto ?"*

![Screenshot](/TP4/img/P10.jpg)

- Pour la première question, les chunks retournés ne contiennent pas la bonne réponse: les emails et le document ne sont pas pertinents. L’index n’est pas optimisé pour cette question. Le type de document est approprié.


![Screenshot](/TP4/img/P11.jpg)

- Pour la deuxième question, le retrieval retourne des extraits qui permettent d’identifier une partie de la réponse attendue. Toutefois, les résultats provient du même PDF, ce qui entraîne une redondance dans les résultats. Le type de document est approprié.

![Screenshot](/TP4/img/P12.jpg)


- Après ce premier essai, j'ai procédé à un ajustement du chunking et reconstruction de l’index. Malgré cette reconstruction, les résultats restent similaires.

## RAG complet

> *python TP4/rag_answer.py "Quels sont les sujets de PFE supplémentaires proposés par Luca Benedetto ?"*

```
================================================================================
[QUESTION]
Quels sont les sujets de PFE supplémentaires proposés par Luca Benedetto ?
================================================================================
[ANSWER]
Information insuffisante.
1. Il n'y a aucune mention de Luca Benedetto ni des sujets de PFE dans le contexte fourni.
2. Aucun document ne contient les informations nécessaires pour répondre à cette question.

[doc_1] [doc_2] [doc_3] [doc_4] [doc_5]
================================================================================

[SOURCES RETRIEVED]
- doc_1: (admin_pdf) Reglement_Interieur_TSP_valide_conseil_ecole_27_novembre_2025.pdf
- doc_2: (email) 202512_vous_avez_remis_votre_travail_pour_le_devoir_soumission_de_la_vido_tous_les_grou_6814947011.md
- doc_3: (email) 202512_ingenieur-3_rappel__nouvel_espace_jobteaser_tlcom_sudparis_-_accdez_aux_offres_d_8270599453.md
- doc_4: (email) 202512_redevance_demebre_2025_5937033520.md
- doc_5: (admin_pdf) Reglement_Interieur_TSP_valide_conseil_ecole_27_novembre_2025.pdf
```

> *python TP4/rag_answer.py "Quelle est la météo à Paris demain ?"*

```
================================================================================
[QUESTION]
Quelle est la météo à Paris demain ?
================================================================================
[ANSWER]
Information insuffisante.
1. Le contexte ne contient aucune information concernant la météo.
2. Aucun document ni email ne traite du sujet de la météo à Paris.

[doc_1] [doc_2] [doc_3] [doc_4] [doc_5]
================================================================================

[SOURCES RETRIEVED]
- doc_1: (admin_pdf) Reglement_scolarite_FISA_conseil_ecole_27novembre2025.pdf
- doc_2: (email) 202512_vous_avez_remis_votre_travail_pour_le_devoir_soumission_de_la_vido_tous_les_grou_6814947011.md
- doc_3: (admin_pdf) Reglement_Interieur_TSP_valide_conseil_ecole_27_novembre_2025.pdf
- doc_4: (admin_pdf) Reglement_Interieur_TSP_valide_conseil_ecole_27_novembre_2025.pdf
- doc_5: (admin_pdf) Reglement_Interieur_TSP_valide_conseil_ecole_27_novembre_2025.pdf
```

- Le modèle n'est pas du tout robuste, cela peut être causé par le nombre faible des documents (108)


## Évaluation

> *python TP4/eval_recall.py*

```
================================================================================
[EVAL] proxy Recall@5 (doc_type attendu dans top-k)
================================================================================

[q1] Quels sont les sujets de PFE supplémentaires proposés par Luca Benedetto ?
  expected: email
  got: ['admin_pdf', 'email', 'email', 'email', 'admin_pdf']
  hit: True

[q2] Comment valider une UE ?
  expected: admin_pdf
  got: ['admin_pdf', 'admin_pdf', 'admin_pdf', 'admin_pdf', 'admin_pdf']
  hit: True

[q3] Quel le nombre minimal des membres d'un groupe dans le module ENG 8601 ?
  expected: email
  got: ['email', 'email', 'email', 'email', 'email']
  hit: True

[q4] Combien de nouveaux modèles de liseuses sont disponibles à la médiathèque ?
  expected: email
  got: ['email', 'admin_pdf', 'email', 'email', 'admin_pdf']
  hit: True

[q5] Combien va durer l'ouverture de l'évaluation du module CSC8607 ?
  expected: email
  got: ['email', 'email', 'email', 'email', 'email']
  hit: True

[q6] Combien d'étudiants et de jeunes diplômés font déjà confiance à Trainy ?
  expected: email
  got: ['email', 'admin_pdf', 'admin_pdf', 'admin_pdf', 'admin_pdf']
  hit: True

[q7] Quelle est la date du job dating de Sopra Steria ?
  expected: email
  got: ['email', 'admin_pdf', 'admin_pdf', 'admin_pdf', 'email']
  hit: True

[q8] Faut-il supprimer l'ancien compte IMTBS/TSP sur le site Job Teaser avant de créer le nouveau compte Télécom SudParis ?
  expected: email
  got: ['email', 'email', 'email', 'email', 'email']
  hit: True

[q9] A quelle adresse la visite d’entreprise chez TALAN aura lieu ?
  expected: email
  got: ['email', 'email', 'admin_pdf', 'email', 'admin_pdf']
  hit: True

[q10] QuelLe bâtiment a subi une coupure d'électricité et n'a pas été en mesure d'assurer le service de restauration ?
  expected: email
  got: ['email', 'email', 'email', 'email', 'email']
  hit: True

--------------------------------------------------------------------------------
[SCORE] 10/10 = 1.00
--------------------------------------------------------------------------------
```

- Exemple d'une bonne réponse: score = 2

> *python TP4/rag_answer.py "Quelle est la date du job dating de Sopra Steria ?"*

```
================================================================================
[QUESTION]
Quelle est la date du job dating de Sopra Steria ?
================================================================================
[ANSWER]
La date du job dating de Sopra Steria pour les stages de fin d'études est le mardi 20 janvier 2026. [doc_1]
================================================================================

[SOURCES RETRIEVED]
- doc_1: (email) 202512_ingenieur-3_en_recherche_de_stage_de_fin_dtudes__jobdating_stage_sopra_steria_20_5938690341.md
- doc_2: (admin_pdf) Reglement_Interieur_TSP_valide_conseil_ecole_27_novembre_2025.pdf
- doc_3: (admin_pdf) Reglement_scolarite_FISA_conseil_ecole_27novembre2025.pdf
- doc_4: (admin_pdf) Reglement_Interieur_TSP_valide_conseil_ecole_27_novembre_2025.pdf
- doc_5: (email) 202512_ingenieur-3_rappel__nouvel_espace_jobteaser_tlcom_sudparis_-_accdez_aux_offres_d_8270599453.md
```

- Exemple d'une bonne réponse: score = 2

> *python TP4/rag_answer.py "Combien de nouveaux modèles de liseuses sont disponibles à la médiathèque ?"*

```
================================================================================
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

- Exemple d'une réponse incomplète : score = 1

> *python TP4/rag_answer.py "Quel le nombre minimal des membres d'un groupe dans le module ENG 8601 ?" *

```
================================================================================
[QUESTION]
Quel le nombre minimal des membres d'un groupe dans le module ENG 8601 ?
================================================================================
[ANSWER]
Information insuffisante.

Pour répondre à la question, il manque les informations suivantes :
1. Le nombre minimal de membres requis pour un groupe dans le module ENG 8601.
2. Si des restrictions ou recommandations spécifiques existent concernant la composition des groupes pour ce module.
================================================================================

[SOURCES RETRIEVED]
- doc_1: (email) 202512_eng_8601__votre_module_danglais_2026_2090099750.md
- doc_2: (email) 202512_eng_8601__votre_module_danglais_2026_2090099750.md
- doc_3: (email) 202512_sujet_pfe_et_composition_du_groupe_4817973980.md
- doc_4: (email) 202512_re_sujet_pfe_et_composition_du_groupe_961902288.md
- doc_5: (email) 202512_sujet_pfe_et_composition_du_groupe_4817973980.md
```

- La réponse existe dans le premier document `... et que vous choisissez en groupe de 2 à 4 personnes ...`. 

- Le retrieval retrouve correctement le bon email 202512_eng_8601__votre_module_danglais_2026_2090099750.md,
mais le modèle ne parvient pas à extraire l’information pourtant présente dans le chunk.

- Les causes possibles: Chunk trop long/bruité ou prompt trop prudent

- Les corrections proposées : 
    - Réduire la taille des chunks
    - Ajouter une consigne explicite dans le prompt, par exemple, "Si l'information est présente dans les sources, même brièvement, réponds directement."

![Screenshot](/TP4/img/P14.jpg)

## Conclusion

- Ce TP a permis de mettre en place un pipeline RAG complet avec indexation, retrieval, génération et évaluation. Le retrieval fonctionne correctement. En revanche, la génération reste fragile: dans certains cas, le modèle n’exploite pas correctement des informations pourtant présentes dans les sources. La principale limite rencontrée est donc la sensibilité du modèle à la qualité du chunking et au prompt. Une amélioration serait donc d’optimiser la taille des chunks et de renforcer le prompt.