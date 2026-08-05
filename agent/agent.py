from agent.planner import Planner

from tools.retrieval_tool import retrieval_tool
from tools.summary_tool import summary_tool
from tools.compare_tool import compare_tool
from tools.quiz_tool import quiz_tool


class CourseAgent:

    def __init__(self):

        self.planner = Planner()

        self.tools = {

            "retrieve": retrieval_tool,
            "summary": summary_tool,
            "compare": compare_tool,
            "quiz": quiz_tool

        }

    def chat(self, question: str):

        print("=" * 70)
        print("Planning...")
        print("=" * 70)

        plan = self.planner.plan(question)

        answers = []

        for i, step in enumerate(plan["steps"], start=1):

            tool_name = step["tool"]

            tool_input = step["input"]

            print(f"\nStep {i}")

            print(f"Tool : {tool_name}")

            print(f"Input: {tool_input}")

            tool = self.tools[tool_name]

            result = tool.invoke(
                {
                    "question": tool_input
                }
            )

            answers.append(result)

        return "\n\n" + "\n\n".join(answers)