# TP1 - Fine-tuning GPT-2 for Spam Detection

- Nom: Charfeddine
- Prénom: Hamza
- Date: 09/01/2026

- Python : 3.11
- Versions des bibliothèques:
    - torch : 2.9.1
    - tiktoken : 0.12.0
    - tqdm : 4.67.1
    - pandas : 2.3.3
    - matplotlib : 3.10.8
    - tensorflow : 2.20.0
    - jupyterlab : 4.5.1

- Seed utilisé : 123

## Question 2 — Structure de settings

- Type : dict
- Clés :
    - n_vocab
    - n_ctx
    - n_embd
    - n_head
    - n_layer

```
{
  'n_vocab': 50257,
  'n_ctx': 1024,
  'n_embd': 768,
  'n_head': 12,
  'n_layer': 12
}
```

## Question 3 — Structure de params

- Type : dict
- Contient :
    - wte : embeddings de tokens
    - wpe : embeddings de position
    - blocks : 12 blocs Transformer
    - b, g : paramètres de normalisation

## Question 4 — Configuration du modèle

- Le constructeur GPTModel attend un dictionnaire de configuration avec les clés :

    ```
    {
    "vocab_size",
    "context_length",
    "emb_dim",
    "n_heads",
    "n_layers",
    "drop_rate",
    "qkv_bias"
    }
    ```

- Mappage des paramètres vers cette structure:
    ```
    model_config = {
        "vocab_size": settings["n_vocab"],
        "context_length": settings["n_ctx"],
        "emb_dim": settings["n_embd"],
        "n_heads": settings["n_head"],
        "n_layers": settings["n_layer"],
        "drop_rate": 0.1,
        "qkv_bias": True,
    }
    ```

## Préparation des données

- Dataset : SMS Spam Collection (UCI)
- Total : 5572 messages
- Split :
    - Entraînement : 4457
    - Test : 1115

## Question 5.1 — Pourquoi mélanger le dataset ?

> *df = df.sample(frac=1, random_state=123)*

- Cela permet :
    - de mélanger les données
    - d’éviter un biais d’ordre
    - d’avoir un split train/test représentatif

## Question 5.2 — Distribution des classes

- Le dataset est fortement déséquilibré:
    - ham  : 3860
    - spam : 597

- Cela peut entraîner un biais du modèle vers la classe majoritaire (*'ham'*).


- Dataloaders :
    - Training samples: 4457
    - Batch size : 16
    - Nombre de batches : 279

## Question 8 — Tête de sortie
    - GPT-2 original : *Linear(in_features=768, out_features=50257)*
    - Nouvelle tête : *Linear(in_features=768, out_features=2)*
- On passe donc d’une génération de tokens à une classification binaire.

- Pourquoi geler les couches internes ? : 
    - pour réduire le coût d’entraînement
    - pour conserver les représentations linguistiques de GPT-2

## Question 10 — Analyse de l’apprentissage

![Screenshot](/TP2/img/TP2Q10.jpg)


- La loss diminue globalement au fil des epochs, indiquant que le modèle apprend.
- Les performances sur le jeu de test augmentent également, ce qui montre une bonne généralisation.