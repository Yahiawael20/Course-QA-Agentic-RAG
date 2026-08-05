from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentSplitter:
    """
    Split documents into overlapping chunks for retrieval.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def split_documents(self, documents):

        chunks = self.splitter.split_documents(documents)

        print(f"Created {len(chunks)} chunks.")

        return chunks