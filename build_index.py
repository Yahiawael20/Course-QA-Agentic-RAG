from sources.loader import PDFLoader
from sources.splitter import DocumentSplitter
from sources.embeddings import EmbeddingModel
from sources.vector_store import VectorStore


def main():

    print("=" * 60)
    print("Loading PDFs...")
    print("=" * 60)

    loader = PDFLoader("Data")
    documents = loader.load_documents()

    print("\nSplitting Documents...\n")

    splitter = DocumentSplitter()

    chunks = splitter.split_documents(documents)

    print("\nLoading Embedding Model...\n")

    embedding = EmbeddingModel().get_embedding()

    print("\nCreating FAISS Index...\n")

    vector_db = VectorStore(embedding)

    db = vector_db.build(chunks)

    vector_db.save(db)

    print("\nIndex Created Successfully ✅")


if __name__ == "__main__":
    main()