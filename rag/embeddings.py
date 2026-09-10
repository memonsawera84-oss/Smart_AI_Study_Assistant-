"""
=========================================
Embedding Module
=========================================

Purpose:
Convert text chunks into embeddings
using Ollama.

Author: SK
=========================================
"""

import ollama


def create_embedding(text):
    """
    Create embedding for one text chunk.
    """

    response = ollama.embed(
        model="nomic-embed-text",
        input=text
    )

    return response["embeddings"][0]