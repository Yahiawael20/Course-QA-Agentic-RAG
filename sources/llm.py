import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class LLM:

    _llm = None

    def __init__(self):

        if LLM._llm is None:

            print("Loading Groq LLM...")

            LLM._llm = ChatGroq(
                model="openai/gpt-oss-120b",
                temperature=0.2,
                api_key=os.getenv("GROQ_API_KEY"),
            )

            print("✅ LLM Loaded")

    def get_llm(self):

        return LLM._llm