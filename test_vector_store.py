"""
=========================================
Test Vector Store
=========================================
This file tests whether FAISS stores
and retrieves text correctly.
=========================================
"""

from rag.embeddings import create_embedding
from rag.vector_store import VectorStore

# Sample text chunks
chunks = [
    "Machine Learning is a subset of Artificial Intelligence.",
    "Deep Learning uses neural networks.",
    "Python is a popular programming language.",
    "Computer Vision processes images.",
    "Natural Language Processing understands text."
]

# Create embedding for first chunk to determine vector size
embedding = create_embedding(chunks[0])

dimension = len(embedding)

print("=" * 50)
print("Embedding Dimension:", dimension)
print("=" * 50)

# Create FAISS Vector Store
store = VectorStore(dimension)

# Store all chunks
for chunk in chunks:

    emb = create_embedding(chunk)

    store.add(emb, chunk)

print("✅ All chunks stored successfully.")

print()

# Search
query = "Explain Machine Learning"

query_embedding = create_embedding(query)

results = store.search(query_embedding, k=2)

print("=" * 50)
print("Top Search Results")
print("=" * 50)

for i, result in enumerate(results, start=1):

    print(f"\nResult {i}")
    print(result)