# ID2223


# Lab 1
## Task 1

Link for daily Iris predictor

https://huggingface.co/spaces/Redve/ID2223Task1IrisSpace

Link for interactive Iris

https://huggingface.co/spaces/Redve/ID2223Task1Iris

## Task 2

Link for interactive Wine

https://huggingface.co/spaces/Redve/Wine_Interactive

Link for daily Wine predictor

https://huggingface.co/spaces/Redve/Daily_Wine

# Lab 2

Bengali Transcriber

Link for interactive model 

This finetuning was done with the bengali dataset of mozilla common voice. However, only 30% was used as the dataset was very large. The model took approx 15 hours to train in total. Checkpointing was also done in order to resume training when colab timed out.

This resulted in a validation loss of 0.2531 and a Wer score of 43.0365.

https://huggingface.co/spaces/Redve/BengaliModel

For Task2
We upped the amount of steps to see if we got a better score.

The Wer score went down to 42.2126 and the validation loss went up to 0.2751

We would want to train the model on the whole dataset however this was restricted due to colab

# Project

For project and README please visit: https://github.com/Redve/ID2223/tree/main/Project
