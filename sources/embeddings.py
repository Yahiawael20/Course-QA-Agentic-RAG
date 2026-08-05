from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingModel:
    """
    Create and return the embedding model.
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-base-en-v1.5"
    ):

        self.embedding = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={
                "device": "cpu"
            },
            encode_kwargs={
                "normalize_embeddings": True
            }
        )

    def get_embedding(self):

        return self.embedding