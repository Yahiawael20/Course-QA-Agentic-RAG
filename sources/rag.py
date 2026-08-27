from sources.retriever import Retriever
from sources.llm import LLM


class RAG:

    def __init__(self):

        self.retriever = Retriever()
        self.llm = LLM().get_llm()

        
        self.threshold = 0.75

    # ---------------------------------
    # Retrieve Context Only
    # ---------------------------------

    def retrieve(self, question: str, k: int = 3):

        results = self.retriever.search(
            query=question,
            k=k
        )

        if len(results) == 0:

            return {
                "context": "",
                "sources": [],
                "found": False
            }

        best_score = results[0][1]

        print(f"\nBest Similarity Score: {best_score}")

        if best_score > self.threshold:

            return {
                "context": "",
                "sources": [],
                "found": False
            }

        documents = [doc for doc, score in results]

        context = "\n\n".join(
            doc.page_content
            for doc in documents
        )

        return {
            "context": context,
            "sources": documents,
            "found": True
        }

    # ---------------------------------
    # Generate Final Answer
    # ---------------------------------

    def answer(self, question: str, k: int = 3):

        result = self.retrieve(
            question=question,
            k=k
        )

        if not result["found"]:

            return {
                "answer": "I don't know. This topic is not covered in the provided course materials.",
                "sources": []
            }

        prompt = f"""
You are an AI teaching assistant.

Answer ONLY using the provided course materials.

Rules:

- Answer ONLY from the context.
- Do NOT use outside knowledge.
- Do NOT guess.
- If the answer cannot be found in the context, reply exactly:

I don't know. This topic is not covered in the provided course materials.

Context:
{result["context"]}

Question:
{question}

Answer:
"""

        response = self.llm.invoke(prompt)

        return {
            "answer": response.content,
            "sources": result["sources"]
        }