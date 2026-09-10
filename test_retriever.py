"""
=========================================
Test Retriever
=========================================
"""

from rag.embeddings import create_embedding
from rag.vector_store import VectorStore
from rag.retriever import Retriever

chunks = [
    "Machine Learning is a subset of Artificial Intelligence.",
    "Deep Learning uses neural networks.",
    "Python is a programming language.",
    "Computer Vision processes images.",
    "Natural Language Processing understands human language."
]

# Create Vector Store
embedding = create_embedding(chunks[0])
dimension = len(embedding)

store = VectorStore(dimension)

# Store chunks
for chunk in chunks:
    emb = create_embedding(chunk)
    store.add(emb, chunk)

# Create Retriever
retriever = Retriever(store)

# Ask Question
question = "What is Machine Learning?"

results = retriever.retrieve(question)

print("=" * 50)
print("Relevant Chunks")
print("=" * 50)

for i, chunk in enumerate(results, start=1):
    print(f"\nChunk {i}")
    print(chunk)