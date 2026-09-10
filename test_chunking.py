"""
=========================================
Test Chunking Module
=========================================
This file tests whether the PDF text
is being split into chunks correctly.
=========================================
"""

from rag.chunking import split_text

# Sample text (for testing)
sample_text = """
Artificial Intelligence (AI) is changing the world.
Machine Learning is a subset of AI.
Deep Learning is a subset of Machine Learning.
Natural Language Processing allows computers to understand language.
Computer Vision helps machines understand images.
""" * 20   # Repeat to make the text longer

# Split the text into chunks
chunks = split_text(sample_text)

print("=" * 50)
print("Number of Chunks:", len(chunks))
print("=" * 50)

# Display each chunk
for i, chunk in enumerate(chunks, start=1):
    print(f"\n📄 Chunk {i}")
    print("-" * 40)
    print(chunk)