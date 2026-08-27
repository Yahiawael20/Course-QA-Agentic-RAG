from langchain_core.tools import tool

from sources.rag import RAG
from sources.llm import LLM

rag = RAG()
llm = LLM().get_llm()


@tool
def compare_tool(question: str) -> str:
    """
    Compare two or more topics using the course materials.

    Use this tool when the user asks to:
    - compare
    - difference between
    - compare X and Y
    """

    print("\nRunning Compare Tool...\n")

    result = rag.retrieve(
        question=question,
        k=4
    )

    context = result["context"]

    prompt = f"""
You are an AI teaching assistant.

Compare the requested topics using ONLY the provided context.

Instructions:
- Use a markdown table whenever possible.
- Highlight similarities and differences.
- If information is missing, say so.
- Do NOT use your own knowledge.

Context:
{context}

Question:
{question}

Comparison:
"""

    response = llm.invoke(prompt)

    sources = []

    for doc in result["sources"]:

        source = doc.metadata["source"]
        page = doc.metadata["page"] + 1

        sources.append(
            f"- {source} (Page {page})"
        )

    sources = sorted(set(sources))

    return f"""{response.content}

Sources:
{chr(10).join(sources)}
"""