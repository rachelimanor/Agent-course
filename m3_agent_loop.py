# m3_agent_loop.py
from openai import OpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langchain_community.tools.tavily_search import TavilySearchResults
from tools import calc, web_search
import json
from typing import TypedDict, Any

client = OpenAI()

# Define the shared state structure
class AgentState(TypedDict, total=False):
    user_input: str
    model_message: Any
    tool_calls: list[Any]
    tool_results: list[dict[str, Any]]
    final_answer: str


# Node 1: The model decides what to do next
def planner(state: AgentState):
    user_query = state["user_input"]
    messages = [
        {"role": "system", "content": "You are an AI agent that can use tools to answer questions."},
        {"role": "user", "content": user_query},
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "calc",
                "description": "Perform arithmetic on a math expression",
                "parameters": {
                    "type": "object",
                    "properties": {"text_or_expression": {"type": "string"}},
                    "required": ["text_or_expression"],
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
                    "properties": {"query": {"type": "string"}},
                    "required": ["query"],
                },
            },
        },
    ]

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
    )

    msg = resp.choices[0].message

    state["model_message"] = msg
    state["tool_calls"] = msg.tool_calls or []

    # print("stet[model_message]: ", state["model_message"])
    # print("state[tool_calls]: ", state["tool_calls"])
    return state


# Node 2: Execute any tool calls from the model
def executor(state: AgentState):
    results = []

    for call in state.get("tool_calls", []):
        fn = call.function.name
        args = json.loads(call.function.arguments)

        if fn == "calc":
            r = calc(**args)
            results.append({"tool": fn, "result": r.model_dump()})
        elif fn == "web_search":
            r = web_search(**args)
            results.append({"tool": fn, "result": r.model_dump()})
        else:
            results.append({"tool": fn, "result": "Unknown tool"})

    state["tool_results"] = results
    return state


# Node 3: Feed the tool results back to the model for final reasoning
def summarizer(state: AgentState):
    results_text = json.dumps(state["tool_results"], indent=2)
    messages = [
        {"role": "system", "content": "You are an AI assistant summarizing results."},
        {"role": "user", "content": f"Question: {state['user_input']}"},
        {"role": "assistant", "content": f"Tool outputs:\n{results_text}"},
        {"role": "user", "content": "Please give a final short answer."},
    ]

    resp = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    state["final_answer"] = resp.choices[0].message.content
    return state


# Build the graph
graph = StateGraph(AgentState)
graph.add_node("planner", planner)
graph.add_node("executor", executor)
graph.add_node("summarizer", summarizer)

graph.add_edge(START, "planner")
graph.add_edge("planner", "executor")
graph.add_edge("executor", "summarizer")
graph.add_edge("summarizer", END)

compiled_graph = graph.compile()

# === RUN TEST ===
if __name__ == "__main__":
    user_query = input("Ask me something: ")
    final_state = compiled_graph.invoke({"user_input": user_query})
    print("\n🧠 Final answer:\n", final_state["final_answer"])
