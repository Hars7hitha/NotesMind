from transformers import pipeline
pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")
pipeline("question-answering", model="deepset/minilm-uncased-squad2")