from langchain_community.vectorstores import FAISS

from sources.embeddings import EmbeddingModel


class Retriever:

    def __init__(self):

        embedding_model = EmbeddingModel().get_embedding()

        self.vector_store = FAISS.load_local(
            "vector_store",
            embedding_model,
            allow_dangerous_deserialization=True
        )

    def search(self, query: str, k: int = 3):

        return self.vector_store.similarity_search_with_score(
            query=query,
            k=k
        )