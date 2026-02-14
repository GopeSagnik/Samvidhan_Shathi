# 🇮🇳 Samvidhan-Sathi: AI Legal Aid Companion

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit)
![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange?style=for-the-badge)
![RAG](https://img.shields.io/badge/Architecture-Hybrid%20RAG-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Hackathon%20Prototype-yellow?style=for-the-badge)

> **"Justice delayed is justice denied."** > *Samvidhan-Sathi bridges the gap between complex Indian laws and the common citizen using Generative AI.*

---

## 📜 Preamble (The Problem)
In India, legal literacy is low, and professional legal advice is expensive. Citizens often don't know if a problem is **Civil** or **Criminal**, let alone which Article of the Constitution protects them.

**Samvidhan-Sathi** acts as a **"Legal First Responder"**. It doesn't replace a lawyer; it empowers you before you meet one.

---

## 🧠 The Architecture (Hybrid RAG)

This isn't just a chatbot. It's a **State-Aware Agent** built with **LangGraph**.

```mermaid
graph TD
    User(User Input) --> Categorizer{Categorize Intent}
    Categorizer -->|Civil/Criminal| DB[(Local ChromaDB)]
    Categorizer -->|Recent Events| Web{Tavily Search}
    DB --> Context
    Web --> Context
    Context --> Drafter[LLM Drafter]
    Drafter --> Output(Final Advice)