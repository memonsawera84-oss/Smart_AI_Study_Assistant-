"""
=========================================
Vector Store
=========================================
Store embeddings in FAISS.
=========================================
"""

import faiss
import numpy as np


class VectorStore:

    def __init__(self, dimension):

        # Create FAISS index
        self.index = faiss.IndexFlatL2(dimension)

        # Store original text chunks
        self.text_chunks = []

    def add(self, embedding, text):

        vector = np.array([embedding]).astype("float32")

        self.index.add(vector)

        self.text_chunks.append(text)

    def search(self, embedding, k=3):

        vector = np.array([embedding]).astype("float32")

        distances, indices = self.index.search(vector, k)

        results = []

        for idx in indices[0]:

            if idx < len(self.text_chunks):

                results.append(self.text_chunks[idx])

        return results