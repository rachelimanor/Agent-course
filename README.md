# 🧠 Agentic AI – 1-Week Hands-On Course

This repository contains a **step-by-step hands-on curriculum** for learning how to build and reason about **Agentic AI systems** using Python, OpenAI’s API, and LangGraph.

Over 7 days, you’ll go from a simple LLM call → to tool-calling → to a fully working agent that plans, acts, remembers, and retrieves knowledge.

---

## 📚 Course Overview

| Day    | Milestone                            | Focus                                                        |
| ------ | ------------------------------------ | ------------------------------------------------------------ |
| **M1** | Agentic Fundamentals & Tooling Setup | Environment, OpenAI API test, structured outputs             |
| **M2** | Tool Calling & Structured Outputs    | Create callable tools (`calc`, `web_search`)                 |
| **M3** | Planning / Acting Loop with State    | Build a LangGraph agent with planner → executor → summarizer |
| **M4** | Retrieval-Augmented QA (RAG)         | Add FAISS vector store and local-knowledge search            |
| **M5** | Evals & Telemetry                    | Measure tool-call success, latency, traces (coming soon)     |
| **M6** | Capstone: Ship Your Agent            | Package into CLI / web demo (coming soon)                    |

---

## 🧩 Tech Stack

| Component                           | Purpose                               |
| ----------------------------------- | ------------------------------------- |
| **Python 3.11+**                    | Base runtime                          |
| **OpenAI SDK**                      | Core LLM and embedding APIs           |
| **LangGraph / LangChain Community** | Agent orchestration & graph state     |
| **Pydantic**                        | Data validation & structured tool I/O |
| **FAISS**                           | Local vector index for RAG            |
| **dotenv**                          | Environment variable management       |
| **pytest**                          | Quick smoke tests                     |

---

## ⚙️ Setup

1. **Clone the repo**

   ```bash
   git clone https://github.com/<your-username>/agentic-ai-course.git
   cd agentic-ai-course
   ```

2. **Create a virtual environment**

   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   (If missing, you can re-create it from the package list in this README.)

4. **Add your keys in `.env`**

   ```env
   OPENAI_API_KEY=sk-...
   TAVILY_API_KEY=tvly_...
   ```

---

## 🧠 Milestone Summaries

### **M1 – Fundamentals**

`m1_check.py`

* Tests OpenAI connectivity and structured JSON output.
* Introduces Pydantic models for typed data.

### **M2 – Tools**

`tools.py`, `m2_tool_test.py`

* Implements:

  * `calc(expression)` → validated math evaluator
  * `web_search(query)` → Tavily web search
* Demonstrates JSON schemas & function-calling.

### **M3 – Agent Loop**

`m3_agent_loop.py`

* Introduces **LangGraph**.
* Three-node pipeline:
  **Planner → Executor → Summarizer**
* Tracks state via `AgentState` (TypedDict).
* Chooses and executes tools automatically.

### **M4 – Retrieval-Augmented QA**

`rag_build_index.py`, `rag_tool.py`

* Builds FAISS vector index from `data/*.txt`.
* Adds `rag_search(query)` tool for local knowledge retrieval.
* Agent can now choose between `calc`, `web_search`, and `rag_search`.

---

## 🧾 Example Runs

**Math:**

```bash
python m3_agent_loop.py
Ask me something: What is (12/4)+3?
🧠 Final answer:
The answer is 6.
```

**Web Search:**

```bash
Ask me something: Who founded LangChain?
🧠 Final answer:
LangChain was founded by Harrison Chase.
```

**RAG:**

```bash
Ask me something: What does our intro document say?
🧠 Final answer:
(Concise summary with [source] citation)
```

---

## 🧮 Testing

Run smoke tests:

```bash
pytest -q
```

Expected:

* `calc()` returns correct values
* `web_search()` yields results
* `rag_search()` retrieves from local docs

---

## 🧱 Folder Structure

```
agentic-ai-course/
│
├── data/                 # your text corpus for RAG
├── index/                # FAISS index (auto-generated)
│
├── tools.py              # calc() and web_search() tools
├── rag_tool.py           # rag_search() tool
├── rag_build_index.py    # builds local vector store
│
├── m1_check.py           # OpenAI API check
├── m2_tool_test.py       # manual tool test
├── m3_agent_loop.py      # planner → executor → summarizer agent
│
├── tests/                # simple pytest smoke tests
│
├── .env                  # API keys
├── requirements.txt
└── README.md
```

---

## ⚡ Tips

* Run `pip check` if you hit dependency conflicts.
* Regenerate FAISS index whenever you change `data/`.
* Use `print(state)` in `m3_agent_loop.py` to debug the graph flow.

---

## 🧩 Next Steps

* **M5:** add metrics & telemetry (trace latency, tool success rate)
* **M6:** deploy via FastAPI or Streamlit
* Extend with custom tools (DB query, file search, API calls)

---

## 🪄 Author & Credits

Created as part of the *Agentic AI Fundamentals — Hands-On Course* led by ChatGPT (GPT-5) with student implementation in Python 3.11.
Built using OpenAI, LangGraph, LangChain Community, and FAISS.
