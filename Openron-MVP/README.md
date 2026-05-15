# Openron B2A Engine MVP

The **B2A (Business-to-Agent) Engine** is a headless "Software-as-a-Tool" (SaaT) platform designed to bridge the gap between legacy web interfaces and the next generation of AI Agents. 

Following the vision outlined in `VISION.md`, this MVP turns complex web workflows into deterministic, agent-executable tools using CrewAI for orchestration and Stagehand for autonomous web interaction.

## 🚀 How it Works (The B2A Lifecycle)

1.  **Intent Capture**: User/Agent submits a natural language intent (e.g., "Extract stock prices" or "Analyze GitHub contributors").
2.  **B2A Schema Planning**: A **B2A Schema Planner** (LLM Agent) interprets the intent and maps it to a structured execution schema (Target URL + Deterministic Task).
3.  **B2A Execution**: The **B2A Execution Agent** leverages the **Stagehand Engine** to navigate legacy UIs, bypass visual inconsistency, and extract high-signal data.
4.  **B2A Data Synthesis**: The **B2A Data Synthesizer** converts raw execution logs into a token-efficient, high-signal response optimized for LLM context windows.

## 🛠️ Mapping to VISION.md

| VISION.md Goal | Implementation in this MVP |
| :--- | :--- |
| **Schema-Driven Tools** | `B2A Schema Planner` enforces strict JSON/Pydantic schemas for execution. |
| **Token-Efficient Context** | `B2A Data Synthesizer` compresses raw browser output into high-signal summaries. |
| **Agentic Accessibility** | Turns any website into a headless tool accessible via simple CLI or API call. |
| **Actionable Error Logs** | Refined error handling in `stagehand_tool.py` provides LLM-readable diagnostics. |
| **Local or API Flexibility** | Full support for local LLMs (Ollama) or API providers (OpenAI/Anthropic). |

## ⚙️ Setup & Configuration

### 1. Configure Environment
Copy `.env.example` to `.env` and configure your preferred models and providers.

```env
# Example for a Local-First Setup
PLANNER_MODEL=ollama/llama3
AUTOMATION_MODEL=openai/gpt-4o
STAGEHAND_PROVIDER=openai
STAGEHAND_MODEL=gpt-4o
```

### 2. Install Prerequisites
- **Ollama (Optional for Local)**: [Download Ollama](https://ollama.com/download) and pull your model: `ollama pull llama3`.
- **Playwright**: Required for browser automation. [Install Playwright](https://playwright.dev/docs/intro).

### 3. Install Dependencies
```bash
uv sync
source .venv/bin/activate # or .venv\Scripts\activate on Windows
playwright install
```

## 🏃 Running the B2A Engine

To execute the agentic workflow:

```bash
python flow.py
```

This will trigger the multi-agent orchestration, demonstrating the transformation of a web browsing task into a B2A execution flow.

## 📦 Stack
- [Stagehand](https://docs.stagehand.dev/): The autonomous browser machinery.
- [CrewAI](https://docs.crewai.com): The agentic orchestration layer.
- [uv](https://docs.astral.sh/uv/): Fast Python package management.
