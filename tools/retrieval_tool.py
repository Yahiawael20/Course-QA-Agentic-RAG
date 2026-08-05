from langchain_core.tools import tool

from sources.rag import RAG

rag = RAG()


@tool
def retrieval_tool(question: str) -> str:
    """
    Retrieve an answer from the course materials.

    Use this tool for:
    - Definitions
    - Concepts
    - Facts
    - Explanations
    """

    print("\nRunning Retrieval Tool...\n")

    result = rag.answer(
        question=question,
        k=3
    )

    answer = result["answer"]

    # لو السؤال خارج محتوى الـ PDF
    if len(result["sources"]) == 0:
        return answer

    sources = []

    for doc in result["sources"]:

        source = doc.metadata["source"]
        page = doc.metadata["page"] + 1

        sources.append(
            f"- {source} (Page {page})"
        )

    sources = sorted(set(sources))

    return f"""{answer}

Sources:
{chr(10).join(sources)}
"""