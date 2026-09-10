"""
=========================================
RAG Engine
=========================================

This module builds and searches
the knowledge base.

Author: SK
=========================================
"""

from rag.chunking import split_text
from rag.embeddings import create_embedding
from rag.vector_store import VectorStore
from rag.retriever import Retriever


class RAGEngine:

    def __init__(self):

        self.store = None
        self.retriever = None
        self.total_chunks = 0

    def build_database(self, pdf_text):

        # Split PDF into chunks
        chunks = split_text(pdf_text)

        if not chunks:
            raise ValueError("No text chunks were created from the PDF.")

        self.total_chunks = len(chunks)

        # Get embedding size
        first_embedding = create_embedding(chunks[0])

        dimension = len(first_embedding)

        # Create FAISS Database
        self.store = VectorStore(dimension)

        # Store every chunk
        for chunk in chunks:

            embedding = create_embedding(chunk)

            self.store.add(embedding, chunk)

        # Create Retriever
        self.retriever = Retriever(self.store)

        return self.total_chunks

    def search(self, question, k=3):

        return self.retriever.retrieve(question, k)

    def get_total_chunks(self):

        return self.total_chunks