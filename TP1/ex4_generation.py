import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import time

SEED = 42
torch.manual_seed(SEED)

model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

prompt = "The future of artificial intelligence is"
inputs = tokenizer(prompt, return_tensors="pt")

outputs = model.generate(
    **inputs,
    max_length=50,
)

text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(text)

def generate_once(seed):
    torch.manual_seed(seed)
    out = model.generate(
        **inputs,
        max_length=50,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
    )
    return tokenizer.decode(out[0], skip_special_tokens=True)

for s in [1, 2, 3, 4, 5]:
    print("SEED", s)
    print(generate_once(s))
    print("-" * 40)

def generate_with_penalty(seed, penalty):
    torch.manual_seed(seed)
    out = model.generate(
        **inputs,
        max_length=50,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        repetition_penalty=penalty
    )
    return tokenizer.decode(out[0], skip_special_tokens=True)

print("Sans pénalité:")
print(generate_with_penalty(1, 1.0))

print("\nAvec pénalité:")
print(generate_with_penalty(1, 2.0))


def generate_temp(temp):
    torch.manual_seed(1)
    out = model.generate(
        **inputs,
        max_length=50,
        do_sample=True,
        temperature=temp,
        top_k=50,
        top_p=0.95,
    )
    return tokenizer.decode(out[0], skip_special_tokens=True)

print("Température 0.1")
print(generate_temp(0.1))

print("\nTempérature 2.0")
print(generate_temp(2.0))

print("\nBeam Search")
print("\n")
start = time.time()
out_beam = model.generate(
    **inputs,
    max_length=50,
    num_beams=40,
    early_stopping=True
)

end = time.time()
txt_beam = tokenizer.decode(out_beam[0], skip_special_tokens=True)
print(txt_beam)
print("Temps:", end - start)