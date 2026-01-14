from langchain_google_genai import ChatGoogleGenerativeAI

class BruteAgent:
    """Agent responsible for generating simple, correct brute force solutions."""
    
    def __init__(self, model_name: str):
        if ":" in model_name:
            provider, model = model_name.split(":", 1)
        else:
            model = model_name
        
        if model.startswith("models/"):
            model = model.replace("models/", "")
        
        # Optimal temperature for code generation
        self.model = ChatGoogleGenerativeAI(model=model, temperature=0.1, top_p=0.9)
        
        self.system_prompt = """You are a competitive programming expert specializing in brute force solutions.

ROLE: Generate SIMPLE, CORRECT brute force solutions that prioritize correctness over efficiency.

STRATEGY:
- Use straightforward approaches: nested loops, recursion, exhaustive search
- Don't worry about time/space complexity
- Prioritize code clarity and correctness
- Test all possibilities if needed

CODE REQUIREMENTS:
1. Read input from stdin using standard Python input methods
2. Write output to stdout using print()
3. Parse input according to the EXACT format specified
4. Handle ALL test cases if multiple are given (process entire input)
5. Handle edge cases: empty input, single element, boundary values
6. Ignore blank lines in input gracefully


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
        
        code = code.strip()
        
        # Extract from fenced code blocks
        if "```python" in code:
            code = code.split("```python", 1)[1]
            if "```" in code:
                code = code.split("```", 1)[0]
        elif "```" in code:
            code = code.split("```", 1)[1]
            if "```" in code:
                code = code.split("```", 1)[0]
        
        # Remove stray backticks
        code = code.strip("`").strip()
        
        # Find first Python-relevant line
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

    def generate_solution(self, problem_statement: str) -> str:
        """Generate brute force solution."""
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
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Problem:\n\n{combined_problem}\n\nGenerate a brute force Python solution."}
        ]
        
        response = self.model.invoke(messages)
        code = getattr(response, "content", "") or ""
        
        return self._strip_code_blocks_and_preamble(code)














