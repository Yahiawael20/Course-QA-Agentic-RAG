import json

from sources.llm import LLM


class Planner:

    def __init__(self):

        self.llm = LLM().get_llm()

    def plan(self, question: str):

        prompt = f"""
You are an AI planning agent.

Available tools:

- retrieve
- summary
- compare
- quiz

Analyze the user's request.

If one tool is enough, return one step.

If multiple tools are needed,
return multiple steps in execution order.

Return ONLY valid JSON.

Example 1:

{{
    "steps":[
        {{
            "tool":"retrieve",
            "input":"What is Deep Learning?"
        }}
    ]
}}

Example 2:

{{
    "steps":[
        {{
            "tool":"compare",
            "input":"Machine Learning and Deep Learning"
        }},
        {{
            "tool":"quiz",
            "input":"Machine Learning and Deep Learning"
        }}
    ]
}}

Question:

{question}
"""

        response = self.llm.invoke(prompt)

        try:

            return json.loads(response.content)

        except Exception:

            print(response.content)

            return {
                "steps": [
                    {
                        "tool": "retrieve",
                        "input": question
                    }
                ]
            }