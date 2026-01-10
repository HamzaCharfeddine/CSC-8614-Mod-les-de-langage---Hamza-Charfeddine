from transformers import GPT2Tokenizer

# Charger le tokenizer GPT-2
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

phrase = "Artificial intelligence is metamorphosing the world!"

# Tokenisation
tokens = tokenizer.tokenize(phrase)

print("Tokens:")
print(tokens)

# Obtenir les IDs des tokens
token_ids = tokenizer.encode(phrase)
print("\nToken IDs:")
print(token_ids)

print("\nDétails par token:")
for tid in token_ids:
    txt = tokenizer.decode([tid])
    print(tid, repr(txt))

phrase2 = "GPT models use BPE tokenization to process unusual words like antidisestablishmentarianism."

tokens2 = tokenizer.tokenize(phrase2)
print("\nTokens phrase 2:")
print(tokens2)

# Extraire uniquement les tokens du mot long
long_word_tokens = tokenizer.tokenize(" antidisestablishmentarianism")
print("\nSous-tokens de antidisestablishmentarianism:")
print(long_word_tokens)
print("Nombre de sous-tokens:", len(long_word_tokens))