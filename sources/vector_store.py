import os

from tqdm import tqdm
from langchain_community.vectorstores import FAISS


class VectorStore:

    def __init__(self, embedding):
        self.embedding = embedding

    def build(self, chunks, batch_size=100):

        print(f"Creating FAISS Index ({len(chunks)} chunks)...\n")

        db = None

        for i in tqdm(
            range(0, len(chunks), batch_size),
            desc="Embedding Chunks",
            unit="batch"
        ):

            batch = chunks[i:i + batch_size]

            if db is None:
                db = FAISS.from_documents(
                    documents=batch,
                    embedding=self.embedding
                )
            else:
                db.add_documents(batch)

        return db

    def save(self, vector_db, path="vector_store"):

        os.makedirs(path, exist_ok=True)

        vector_db.save_local(path)

        print(f"\n✅ Vector store saved to '{path}'")

    def load(self, path="vector_store"):

        return FAISS.load_local(
            path,
            self.embedding,
            allow_dangerous_deserialization=True
        )