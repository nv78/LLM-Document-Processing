import numpy as np
from app.rag.embed import get_embedding

def cosine_sim(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

class VectorStore:
    def __init__(self):
        self.vectors = []

    def add(self, doc_id, text):
        emb = get_embedding(text)
        self.vectors.append((doc_id, emb, text))

    def query(self, query_text, top_k=1):
        q_emb = get_embedding(query_text)
        sims = [(doc_id, cosine_sim(q_emb, emb), text) for doc_id, emb, text in self.vectors]
        sims.sort(key=lambda x: x[1], reverse=True)
        return sims[:top_k]

store = VectorStore()