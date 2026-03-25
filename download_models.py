from transformers import pipeline
pipeline("summarization", model="t5-small")
pipeline("question-answering", model="deepset/minilm-uncased-squad2")