# 🧠 LLM Workflow

A practical guide for building effective LLM-powered systems using **pure Python**—no heavy frameworks, just proven patterns and reusable code snippets.

## 📚 About This Repository

This repository provides real-world examples and design patterns for building reliable, composable LLM workflows. Whether you're working on agents, assistants, or task-specific pipelines, you'll find ready-to-use patterns like:

- 🔗 Prompt Chaining  
- 🔀 Request Routing  
- ⚡ Parallel Execution  
- 🤖 Orchestrator–Worker Architecture


💡 Inspired by:
- [Building AI Agents in Pure Python](https://www.youtube.com/watch?v=bZzyPscbtI8) - by Dave Ebbelaar

🔗 Learn more about the theory and practice behind these patterns:
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) - Anthropic's blog post

---

## 🧩 Contents

### Part 1: Core LLM Techniques  
- Basic LLM calls  
- Structured outputs  
- Tool usage  
- Retrieval integration  

### Part 2: Workflow Patterns  
- Prompt chaining  
- Routing  
- Parallel guardrails  
- Orchestrator–Worker design  

> 🔧 Requirements: Python basics, OpenAI SDK, and API key

---

## 🔁 Example Use Case: Calendar Assistant

Includes implementations using the above patterns to build a functional calendar assistant:

### ✅ Prompt Chaining  
Break down complex tasks into structured steps for better reliability.

### 🔀 Routing  
Direct user input to specialized logic based on intent.

### ⚡ Parallelization  
Run multiple LLM checks (e.g., security + calendar validation) concurrently.

### 🤖 Orchestrator–Worker  
Coordinate planning, writing, and review stages with specialized agents.

---

## ⚙️ Setup Guide

Follow these steps to set up the project locally:

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd llm-workflow-cookbook

2. **Create and activate a virtual environment:**
   ```bash
    python -m venv .venv
    source venv/bin/activate  # On Windows use `.venv\Scripts\activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Set up environment variables:**
    Create a `.env` file in the root directory and add your OpenAI API key:
   ```bash
    OPENAI_API_KEY=your-api-key-here

---
