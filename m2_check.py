# m2_tool_test.py
from openai import OpenAI
from tools import calc, web_search

client = OpenAI()

# We'll simulate tool use manually for now.
question = "Can you calculate the value of (12/4)+3 for me please?"

if any(ch in question for ch in "+-*/"):
    out = calc(question)
    print(f"🧮 Tool used: calc → {out.value}")
else:
    out = web_search(question)
    print(f"🌐 Tool used: web_search → {len(out.results)} results")
