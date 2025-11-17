# m1_check.py
from openai import OpenAI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from tools import calc, web_search



# Load your .env file
load_dotenv()


#print(calc("(12/4)+3"))
#print(web_search("LangGraph tutorial"))

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "calc",
            "description": "Perform arithmetic on a math expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression to evaluate"}
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                },
                "required": ["query"],
            },
        },
    },
]

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Find me the current price of Bitcoin"}],
    tools=tools,
)
print(resp.choices[0].message)


