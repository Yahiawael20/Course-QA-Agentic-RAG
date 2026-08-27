from langchain_core.tools import tool

from sources.rag import RAG
from sources.llm import LLM

rag = RAG()
llm = LLM().get_llm()


@tool
def summary_tool(question: str) -> str:
    """
    Summarize a topic using the course materials.

    Use this tool when the user asks to:
    - summarize
    - give an overview
    - provide key points
    """

    print("\nRunning Summary Tool...\n")

    result = rag.retrieve(
        question=question,
        k=3
    )

    context = result["context"]

    prompt = f"""
You are an AI teaching assistant.

Summarize the following course material.

Rules:
- Use ONLY the provided context.
- Use bullet points.
- Keep the summary concise.
- Do not add information that is not in the context.

Context:
{context}

Summary:
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