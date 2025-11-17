# tools.py
from pydantic import BaseModel, Field
from tavily import TavilyClient
import ast, operator, math, re
from dotenv import load_dotenv
import os


load_dotenv()  # 👈 this ensures your .env file is read


# ✅ Initialize Tavily web search client
t_client = TavilyClient()

# ---------------------------
# TOOL 1: Calculator
# ---------------------------
class CalcOut(BaseModel):
    value: float


MATH_RUN = re.compile(r"[0-9\.\+\-\*\/\(\)\s]+")

def _normalize_expression(text: str) -> str:
    """Extract the longest math-looking substring from arbitrary text."""
    # Common unicode fixes
    text = (text or "").replace("−", "-").replace("×", "*").replace("÷", "/")
    # Find all runs that contain only digits/operators/space/parentheses
    runs = [r.strip() for r in MATH_RUN.findall(text)]
    if not runs:
        return ""
    # Choose the longest run (simple, works well for prompts like “What is (12/4)+3?”)
    expr = max(runs, key=len)
    # Final sanity: must contain at least one digit
    return expr if re.search(r"\d", expr) else ""

def _eval_ast(node):
    # Python 3.11+ uses ast.Constant for numbers
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise ValueError("Only numeric constants allowed")
    # Unary minus
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval_ast(node.operand)
    # Binary ops
    if isinstance(node, ast.BinOp):
        ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
        }
        fn = ops.get(type(node.op))
        if fn is None:
            raise ValueError("Unsupported operator")
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)
        return fn(left, right)
    raise ValueError("Invalid expression")

def calc(text_or_expression: str) -> CalcOut:
    """
    Safely evaluate a basic math expression. Accepts natural language like
    'What is (12/4)+3?' by extracting the expression first.
    Allowed operators: + - * / and parentheses.
    """
    expr = _normalize_expression(text_or_expression)
    if not expr:
        raise ValueError("No math expression found in input")

    try:
        tree = ast.parse(expr, mode="eval")
        value = _eval_ast(tree.body)
    except ZeroDivisionError:
        raise ValueError("Division by zero")
    except Exception as e:
        raise ValueError(f"Bad expression: {expr!r} ({e})")

    return CalcOut(value=float(value))



# ---------------------------
# TOOL 2: Web Search (Tavily)
# ---------------------------
class WebItem(BaseModel):
    title: str
    url: str
    snippet: str = ""

class WebOut(BaseModel):
    results: list[WebItem] = Field(default_factory=list)

def web_search(query: str, max_results: int = 3) -> WebOut:
    """
    Perform a web search and return results with title, URL, and snippet.
    """
    r = t_client.search(query=query, max_results=max_results)
    items = [
        WebItem(title=i["title"], url=i["url"], snippet=i.get("content", ""))
        for i in r.get("results", [])
    ]
    return WebOut(results=items[:max_results])





