from langchain_google_genai import ChatGoogleGenerativeAI


class TesterAgent:
    """Agent responsible for generating diverse test cases from a problem statement."""

    def __init__(self, model_name: str):
        # Handle provider prefixes like "google:models/gemini-pro"
        if ":" in model_name:
            _, model = model_name.split(":", 1)
        else:
            model = model_name

        if model.startswith("models/"):
            model = model.replace("models/", "")

        # Lower temperature for deterministic and constraint-following output
        self.model = ChatGoogleGenerativeAI(model=model, temperature=0.1, top_p=0.9)

        self.system_prompt = """You are an expert test case generator for competitive programming.

TASK: Generate 5-8 small, diverse test cases that follow the problem's input format exactly.

REQUIREMENTS:
1. Extract ALL constraints from the problem (ranges, sizes, relationships)
2. Generate test cases covering:
   - Minimum values (edge case)
   - Maximum values allowed by constraints (edge case)
   - Single element cases
   - Empty/zero cases if allowed
   - Random medium-sized cases
   - Tricky cases that might break naive solutions
3. Follow the EXACT input format specified
4. Keep values SMALL for manual verification (arrays ≤5 elements)
5. Each test case must satisfy ALL problem constraints

OUTPUT FORMAT:
- Output ONLY raw test input data
- NO markdown, NO code blocks, NO explanations
- NO backticks or formatting
- Separate multiple test cases with a blank line

Example output:
3
1 2 3

2
5 10

1
42
"""

    def generate_test_cases(self, problem_statement: str) -> str:
        """Generate test cases for the given problem statement."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {
                "role": "user",
                "content": f"Problem:\n\n{problem_statement}\n\nGenerate test cases following the constraints above.",
            },
        ]

        response = self.model.invoke(messages)
        ai_content = getattr(response, "content", "").strip()

        # Clean any markdown or code block artifacts
        if ai_content.startswith("```"):
            lines = ai_content.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            ai_content = "\n".join(lines).strip()

        return ai_content
