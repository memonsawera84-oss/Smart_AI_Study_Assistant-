"""
=========================================
Test Embedding Module
=========================================
"""

from rag.embeddings import create_embedding

text = "Machine Learning is a subset of Artificial Intelligence."

embedding = create_embedding(text)

print("=" * 50)
print("Embedding Length:", len(embedding))
print("=" * 50)

print(embedding[:10])