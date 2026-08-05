import re
import unicodedata
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


class PDFLoader:
    """
    Load and clean PDF documents while preserving
    technical content such as code and mathematical expressions.
    """

    def __init__(self, data_path: str):
        self.data_path = Path(data_path)

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean extracted PDF text without destroying
        technical or scientific content.
        """

        if not text:
            return ""

        # -----------------------------
        # Remove null characters
        # -----------------------------
        text = text.replace("\x00", "")

        # -----------------------------
        # Replace tabs
        # -----------------------------
        text = text.replace("\t", " ")

        # -----------------------------
        # Normalize new lines
        # -----------------------------
        text = re.sub(r"\r\n?", "\n", text)

        # -----------------------------
        # Remove multiple spaces
        # -----------------------------
        text = re.sub(r"[ ]{2,}", " ", text)

        # -----------------------------
        # Remove excessive blank lines
        # -----------------------------
        text = re.sub(r"\n{3,}", "\n\n", text)

        # -----------------------------
        # Normalize Unicode
        # -----------------------------
        text = unicodedata.normalize("NFKC", text)

        # -----------------------------
        # Remove invalid surrogate chars
        # -----------------------------
        text = "".join(
            ch for ch in text
            if not (0xD800 <= ord(ch) <= 0xDFFF)
        )

        # -----------------------------
        # Remove control characters
        # (Keep newline only)
        # -----------------------------
        text = "".join(
            ch
            for ch in text
            if ch == "\n" or unicodedata.category(ch)[0] != "C"
        )

        # -----------------------------
        # Final cleanup
        # -----------------------------
        text = text.strip()

        return text

    def load_documents(self):

        documents = []

        pdf_files = sorted(self.data_path.glob("*.pdf"))

        if not pdf_files:
            raise FileNotFoundError(
                f"No PDF files found inside '{self.data_path}'."
            )

        for pdf in pdf_files:

            print(f"Loading: {pdf.name}")

            loader = PyPDFLoader(str(pdf))

            pages = loader.load()

            for page in pages:

                cleaned_text = self.clean_text(page.page_content)

                if not cleaned_text:
                    continue

                documents.append(
                    Document(
                        page_content=cleaned_text,
                        metadata={
                            "source": pdf.name,
                            "page": page.metadata.get("page", 0),
                            "page_label": page.metadata.get("page_label", "")
                        }
                    )
                )

        print(f"\nLoaded {len(documents)} pages successfully.")

        return documents