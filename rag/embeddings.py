"""
=========================================
Embedding Module
=========================================

Purpose:
Convert text chunks into embeddings
using Sentence Transformers.

Author: SK
=========================================
"""

from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text):
    """
    Create embedding for one text chunk.
    """

    embedding = model.encode(text)

    return embedding.tolist()