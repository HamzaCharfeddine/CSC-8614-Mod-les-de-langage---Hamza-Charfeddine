# TP1 - Modèles de langage
- Nom: Charfeddine
- Prénom: Hamza
- Date: 08/01/2026

### Environnement virtuel

- Création et activation de l’environnement:

```
python -m venv venv_tp
venv_tp\Scripts\activate
pip install torch transformers plotly scikit-learn
```
- Python: 3.8.0
- pip: 25.0.1
- Versions des bibliothèques:
    - scikit-learn: 1.3.2
    - plotly: 6.5.1
    - transformers: 4.46.3
    - torch: 2.4.1
    - pandas: 2.0.3
- Seed utilisé: 42

## Découverte du tokenizer GPT-2

> *python TP1/ex1_tokenizer.py*

```
Tokens:
['Art', 'ificial', 'Ġintelligence', 'Ġis', 'Ġmet', 'amorph', 'osing', 'Ġthe', 'Ġworld', '!']
```

- Le symbole spécial Ġ indique la présence d’un espace avant le mot. Le tokenizer encode l’information de l’espace comme un caractère spécial pour distinguer par exemple "word" de " word". Cela permet au modèle de reconstruire correctement le texte avec les espaces.

![Screenshot](/TP1/img/TP1Q1a.jpg)

| Token décodé | Token ID | Remarque |
|-------------|----------|----------|
| Art | 8001 | sous-mot |
| ificial | 9542 | sous-mot |
|  intelligence | 4430 | espace + mot |
|  is | 318 | espace + mot |
|  met | 1138 | espace + sous-mot |
| amorph | 37670 | sous-mot |
| osing | 2752 | sous-mot |
|  the | 262 | espace + mot |
|  world | 995 | espace + mot |
| ! | 0 | ponctuation |

- Les tokens sont des fragments de texte (mots, sous-mots ou symboles). Alors que les token IDs sont leurs représentations numériques utilisées par le modèle.

### Observations:
- GPT-2 découpe les mots fréquents en tokens entiers ou en deux sous-mots simples comme Art et ificial.
Les mots plus longs sont découpés en plusieurs sous-mots fréquents comme met + amorph + osing.
La ponctuation est traitée comme un token indépendant (!).
Les espaces sont encodés à l’aide du symbole spécial Ġ.
- Cette découpe correspond au principe du BPE: le vocabulaire est composé de fragments fréquents réutilisables permettant de représenter efficacement des mots rares.

```
Tokens phrase 2:

['G', 'PT', 'Ġmodels', 'Ġuse', 'ĠB', 'PE', 'Ġtoken', 'ization', 'Ġto', 'Ġprocess', 'Ġunusual', 'Ġwords', 'Ġlike', 'Ġant', 'idis', 'establishment', 'arian', 'ism', '.']

Sous-tokens de antidisestablishmentarianism:

['Ġant', 'idis', 'establishment', 'arian', 'ism']
Nombre de sous-tokens: 5
```
- Le mot *antidisestablishmentarianism* est découpé en 5 sous-mots.
Ce découpage permet au modèle de traiter des mots très longs ou rares en combinant des fragments déjà connus.

## Analyse des encodages positionnels dans GPT-2

```
Shape position embeddings: torch.Size([1024, 768])
n_embd: 768
n_positions: 1024
```

- La matrice d’encodage positionnel a une shape [1024, 768].
La première dimension correspond au nombre maximum de positions possibles dans une séquence (1024 tokens).
La seconde dimension correspond à la taille des embeddings utilisés par GPT-2 (768).
- n_positions représente donc la longueur maximale du contexte que GPT-2 peut traiter.

![Screenshot](/TP1/img/TP1Q3a.jpg)

- Les encodages positionnels projetés en 2D forment une trajectoire continue et ordonnée. Les positions successives suivent une courbe régulière, ce qui montre que les embeddings de positions proches sont également proches dans l’espace vectoriel. Il n’y a pas de regroupements aléatoires. Cela indique que GPT-2 encode explicitement l’ordre des tokens de manière structurée.

- *Intérêt de la PCA*: Les encodages positionnels de GPT-2 sont des vecteurs de dimension 768, ce qui est impossible à visualiser directement. La PCA permet de projeter ces vecteurs de haute dimension dans un espace 2D tout en conservant au maximum la variance des données.

![Screenshot](/TP1/img/TP1Q3b.jpg)

- Avec les 200 premières positions, la trajectoire devient beaucoup plus longue et plus étendue.
Les points forment une grande courbe quasi circulaire, montrant que les encodages positionnels évoluent progressivement avec la position.

- *Comparaison*: 

    - Avec 50 positions, la structure est compacte et facilement lisible. La trajectoire est courte et la progression est clairement observable.

    - Avec 200 positions, la trajectoire est beaucoup plus étendue et la visualisation est plus dense.La structure globale devient plus difficile à lire localement, mais on observe une organisation continue et régulière à grande échelle.

- *Hypothèse*: Ces visualisations suggèrent que GPT-2 apprend une représentation positionnelle continue et progressive.

## Probabilités et génération de texte avec GPT-2


> *python TP1/ex3_probs.py*
```
1 'ificial' 1.920e-05
2 ' intelligence' 1.505e-01
3 ' is' 1.955e-01
4 ' fascinating' 6.504e-04 
5 '.' 1.773e-01
```

- On observe que les tokens prévisibles comme " intelligence", " is" et la ponctuation ont des probabilités plus élevées.

- On lit la probabilité du token t dans les logits à la position t−1 car GPT-2 est un modèle causal : à chaque position, il prédit le token suivant à partir du contexte précédent.

```
total_logp: -23.454848885536194
avg_neg_logp: 4.690969777107239
perplexity: 108.9587943322403
```
- La perplexité mesure à quel point le modèle est surpris par une phrase. Elle correspond au nombre moyen de choix possibles que le modèle hésite à chaque token. En d'autres termes, plus la perplexité est faible, plus la phrase est conforme aux régularités apprises lors de l’entraînement.

- Avec "Artificial fascinating intelligence is.", on obtient:

    - total_logp: -42.1645941734314
    - avg_neg_logp: 8.43291883468628
    - perplexity: 4595.895192713277

- La perplexité est extrêmement élevée (≈ 4600), ce qui indique que la phrase est très improbable selon GPT-2. Cette phrase viole l’ordre syntaxique naturel de l’anglais. Le modèle a appris des régularités fortes sur les structures sujet–verbe–complément.

- Avec "L'intelligence artificielle est fascinante.":

    - total_logp:   -59.4814  
    - avg_neg_logp:  5.9481  
    - perplexity:   383.04

- La perplexité est bien plus élevée que pour la phrase anglaise correcte, mais bien plus basse que pour la phrase anglaise incorrecte.

- GPT-2 est principalement entraîné sur des corpus anglophones. Le français est moins représenté, ce qui entraîne: des découpages en sous-mots plus fréquents, des probabilités conditionnelles plus faibles et une surprise globale plus élevée.

```
' a' 1.204e-01
' the' 5.254e-02
' not' 4.324e-02
' an' 3.092e-02
' now' 2.062e-02
' one' 1.890e-02
' also' 1.880e-02
' already' 1.716e-02
' becoming' 1.606e-02
' just' 1.422e-02
```

- Les tokens proposés sont plausibles et correspondent tous à des continuations naturelles de la phrase. On observe la présence explicite du token d’espace partout.

## Exploration des méthodes de génération avec GPT-2

- Seed utilisé: 42. En effet, fixer un seed permet de rendre les expériences reproductibles.

> *python TP1/ex4_generation.py*

```
The future of artificial intelligence is uncertain.

"We're not sure what the future will look like," said Dr. Michael S. Schoenfeld, a professor of computer science at the University of California, Berkeley. "But we're not
````

- En relançant plusieurs fois, le texte généré est identique. En effet, le greedy decoding choisit à chaque étape le token le plus probable. Le processus est donc entièrement déterministe càd mêmes entrées => même sortie.

![Screenshot](/TP1/img/TP1Q5a.jpg)

- Exemples de générations:

```
The future of artificial intelligence is uncertain. "There's a lot of talk about how to make artificial intelligence better," says Eric Johnson, a professor at the University of California, Los Angeles, who has studied artificial intelligence for more than 40 years.
```

```
The future of artificial intelligence is uncertain. It will be a long, long time before AI becomes a reality.

In the meantime, let's take a look at how the future of artificial intelligence will change the way we live and work.
```

- Le greedy decoding produit toujours exactement le même texte. Par contre, le sampling introduit de l’aléa contrôlé, ce qui permet de générer des textes variés.

- On observe que:
    - Les phrases sont globalement cohérentes et grammaticales.
    - Le ton et la structure changent selon le seed.

- Rôle des paramètres:
    - Température (0.7): contrôle l’aléa (basse = conservateur, haute = créatif)
    - top-k (50): limite le choix aux 50 tokens les plus probables
    - top-p (0.95): sélection dynamique des tokens couvrant 95% de la masse de probabilité

### Effet de la pénalité de répétition

```
Sans pénalité:

The future of artificial intelligence is uncertain. "There's a lot of talk about how to make artificial intelligence better," says Eric Johnson, a professor at the University of California, Los Angeles, who has studied artificial intelligence for more than 40 years.

Avec pénalité:

The future of artificial intelligence is uncertain. "There's a lot to learn from how people interact with each other," says Eric Johnson, an expert in AI at the University Of California Irvine who has studied neural networks for more than 30 years and recently published
```

- La pénalité de répétition réduit la probabilité de réutiliser les mêmes tokens déjà générés. On observe moins de répétitions de segments comme "artificial intelligence. 

- Effet secondaire: parfois des formulations plus forcées ou moins naturelles

### Effet de la température

```
Température 0.1

The future of artificial intelligence is uncertain. But the future of artificial intelligence is not.
The future of artificial intelligence is not.
The future of artificial intelligence is not.
The future of artificial intelligence is not.
The

Température 2.0

The future of artificial intelligence is hard in any other sector (of technology but even when done within human space will need support and services), so far we haven't even gone where artificial intelligence is being integrated. Our goal is to be first in-house
```

- Une température basse rend la distribution extrêmement concentrée: le modèle choisit presque toujours le token le plus probable, ce qui entraîne des répétitions fréquentes.

- Par contre, une température élevée aplatit la distribution de probabilité, ce qui favorise l’exploration de tokens peu probables. Le texte devient plus varié mais perd en cohérence syntaxique et sémantique.

=> La température contrôle donc directement le compromis entre cohérence et diversité (créativité).

### Beam Search

```
Beam Search

The future of artificial intelligence is in the hands of the next generation of scientists and engineers.
The future of artificial intelligence is in the hands of the next generation of scientists and engineers.
The future of artificial intelligence is in the hands of
```

- Le beam search produit un texte très cohérent et grammaticalement correct. Cependant, on observe une forte tendance à la répétition, car l’algorithme cherche à maximiser la probabilité globale de la séquence complète.

### Augmentation du nombre de beams

- On modifie *num_beams* :
    - num_beams=5 : Temps: 4.884
    - num_beams=10 : Temps: 6.479
    - num_beams=20 : Temps: 6.985
    - num_beams=40 : Temps: 13.963

- Plus le nombre de beams augmente, plus la génération est lente. Beam search explore plusieurs chemins en parallèle. Ainsi, sa complexité est proportionnelle au nombre de beams, ce qui augmente fortement le coût de calcul.

