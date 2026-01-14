from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Optional

class OptimalAgent:
    """Agent responsible for generating optimal, efficient solutions."""
    
    def __init__(self, model_name: str):
        if ":" in model_name:
            provider, model = model_name.split(":", 1)
        else:
            model = model_name
        
        if model.startswith("models/"):
            model = model.replace("models/", "")
        
        # Optimal temperature for code generation
        self.model = ChatGoogleGenerativeAI(model=model, temperature=0.1, top_p=0.9)
        
        self.system_prompt = """You are an expert competitive programmer solving contest problems.

ROLE: Generate OPTIMAL solutions that meet time and space complexity requirements.

STRATEGY:
- Analyze the problem constraints carefully
- Choose the most efficient algorithm and data structures
- Optimize for the given constraints (array size, value ranges, etc.)
- Aim for best possible time complexity (O(n), O(n log n), O(n²) only if necessary)
- Use efficient techniques: two pointers, sliding window, DP, greedy, graph algorithms, etc.

CODE REQUIREMENTS:
1. Read input from stdin efficiently
2. Write output to stdout using print()
3. Parse input according to the EXACT format specified
4. Handle ALL test cases if multiple are given
5. Handle edge cases: empty input, single element, boundary values
6. Ignore blank lines in input gracefully
7. Must be CORRECT (passing all test cases is priority #1)

OUTPUT:
- Generate ONLY Python code
- NO markdown formatting
- NO code blocks with ```
- NO explanations or comments
- Complete, runnable solution only
"""

    def _strip_code_blocks_and_preamble(self, code: str) -> str:
        """Remove markdown code fences and preamble."""
        if not code:
            return ""
        
        code = code.strip().strip("`").strip()
        
        # Handle fenced code blocks
        if "```python" in code:
            code = code.split("```python", 1)[1]
            if "```" in code:
                code = code.split("```", 1)[0]
        elif "```" in code:
            code = code.split("```", 1)[1]
            if "```" in code:
                code = code.split("```", 1)[0]
        
        lines = code.splitlines()
        start_idx = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                continue
            if (
                stripped.startswith(('import ', 'from ', 'def ', 'class ', '#', 'if __name__', 'print('))
                or '=' in stripped
                or stripped.startswith(('for ', 'while ', 'with ', 'try:'))
            ):
                start_idx = i
                break
        
        return "\n".join(lines[start_idx:]).strip()

    def generate_solution(self, problem_statement: str, feedback: Optional[str] = None, attempt: int = 1) -> str:
        """Generate optimal solution with optional feedback-based refinement."""
        # Read PROBLEM.txt if exists
        try:
            with open("PROBLEM.txt", "r", encoding="utf-8") as f:
                file_content = f.read().strip()
        except Exception:
            file_content = ""
        
        # Combine problem sources
        if file_content and problem_statement:
            combined_problem = file_content + "\n\n" + problem_statement
        elif file_content:
            combined_problem = file_content
        else:
            combined_problem = problem_statement
        
        user_message = f"Problem:\n\n{combined_problem}\n\nGenerate an optimal Python solution."
        
        if feedback:
            user_message += (
                f"\n\n=== FEEDBACK FROM ATTEMPT {attempt - 1} ===\n"
                f"{feedback}\n\nFix the issues above and generate a corrected solution."
            )
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        response = self.model.invoke(messages)
        code = getattr(response, "content", "") or ""
        
        return self._strip_code_blocks_and_preamble(code)
