# TP3 — Fine-tuning with LoRA

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

- Seed utilisé : 42


## Question 1 

- Yes, there is a difference. In the original model, the layers are standard `Linear` layers. After adding LoRA, these layers are replaced by `LinearWithLoRA` modules.  

- Each of them contains:
    - the original frozen linear layer  
    - an additional LoRA layer that is trainable  

- We can see the `LinearWithLoRA` modules in the model structure after LoRA.

## Question 2  

Before adding the classification head:

- Trainable parameters: **1,327,104**  
- Total parameters: **164,364,288**  
- Trainable fraction: **0.81%**

So more than 99% of the model parameters are frozen and only the LoRA layers are trained.

## Question 3  

After adding the classification head:

- Trainable parameters: **1,328,642**  
- Total parameters: **125,768,450**  
- Trainable fraction: **1.06%**

There are slightly more trainable parameters because of the new classification head.  
The total number of parameters is much smaller because the GPT-2 language head was removed.

## Question 4  

During training, the loss decreases quickly:

- Initial loss: **2.2565**
- Average loss: **0.2570**
- Final accuracy: **93.04%**

The loss goes down fast, which shows the model is learning correctly.  
An accuracy above 93% is reasonable for a spam classification task.


```
Epoch 1 | Batch 0 | Loss: 2.2565
Epoch 1 | Batch 10 | Loss: 1.2277
Epoch 1 | Batch 20 | Loss: 0.1822
Epoch 1 | Batch 30 | Loss: 0.2611
Epoch 1 | Batch 40 | Loss: 0.0652
Epoch 1 | Batch 50 | Loss: 0.0331
Epoch 1 | Batch 60 | Loss: 0.0512
Epoch 1 | Batch 70 | Loss: 0.0144
Epoch 1 | Batch 80 | Loss: 0.0065
Epoch 1 | Batch 90 | Loss: 0.0030
Epoch 1 | Batch 100 | Loss: 0.3394
Epoch 1 | Batch 110 | Loss: 0.0128
Epoch 1 | Batch 120 | Loss: 0.1301
Epoch 1 | Batch 130 | Loss: 0.4440
Epoch 1 | Batch 140 | Loss: 0.0187
Epoch 1 Finished | Avg Loss: 0.2570 | Acc: 93.04% | Time: 51.18s
```

## Question 5  

- Training accuracy: **93.04%**
- Test accuracy: **97.99%**

The test accuracy is even higher than the training accuracy, which means the model generalizes well and does not overfit.


## Conclusion

This lab shows that LoRA is a very efficient way to fine-tune large models.