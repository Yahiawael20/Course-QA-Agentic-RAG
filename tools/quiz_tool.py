from langchain_core.tools import tool

from sources.rag import RAG
from sources.llm import LLM

rag = RAG()
llm = LLM().get_llm()


@tool
def quiz_tool(question: str) -> str:
    """
    Generate multiple-choice questions from the course materials.

    Use this tool when the user asks for:
    - quiz
    - MCQs
    - practice questions
    - test
    """

    print("\nRunning Quiz Tool...\n")

    result = rag.retrieve(
        question=question,
        k=4
    )

    context = result["context"]

    prompt = f"""
You are an AI teaching assistant.

Generate exactly 5 multiple-choice questions using ONLY the provided context.

Rules:
- Each question must have 4 options (A, B, C, D).
- Give the correct answer after each question.
- Do NOT invent information.
- If the context is insufficient, say so.

Context:
{context}

Quiz:
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