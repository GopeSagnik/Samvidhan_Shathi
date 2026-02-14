# 🇮🇳 Samvidhan-Sathi: AI Legal Aid Companion

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit)
![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange?style=for-the-badge)
![RAG](https://img.shields.io/badge/Architecture-Hybrid%20RAG-green?style=for-the-badge)

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

## 🌟 Key Features

| Feature | Description |
| :--- | :--- |
| **🧠 Hybrid Intelligence** | Seamlessly switches between **Groq (Cloud)** for speed and **Ollama (Local)** for privacy/offline access. |
| **⚖️ Constitution First** | RAG system grounded strictly in the **Constitution of India** (`COI.json`) to prevent hallucinations. |
| **🌐 Live Legal Search** | Integrates **Tavily API** to fetch real-time Supreme Court judgments and legal news from 2024-25. |
| **🗣️ Smart Categorization** | Auto-detects legal intent (Civil vs. Criminal vs. Constitutional) for precise context setting. |
| **💾 Contextual Memory** | Remembers your conversation history, allowing for follow-up questions like *"What is the punishment for that?"* |

---

## 🛠️ Technical Stack

<div align="center">

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Orchestration** | ![LangGraph](https://img.shields.io/badge/LangGraph-Stateful_Workflow-orange?style=flat-square) | Manages the decision flow (Categorize → Research → Draft). |
| **Frontend** | ![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=flat-square) | Fast, responsive, dark-themed chat interface. |
| **Vector DB** | ![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-green?style=flat-square) | Stores the Constitution locally for semantic retrieval. |
| **LLM Engine** | ![Llama3](https://img.shields.io/badge/Llama_3-Groq_%2F_Ollama-blue?style=flat-square) | High-performance reasoning and drafting. |
| **Search Tool** | ![Tavily](https://img.shields.io/badge/Tavily-Web_Search-purple?style=flat-square) | Filters web results for "Indian Legal News" only. |

</div>

---

## ⚖️ Usage Guide

### 1. Select Your Engine
Toggle the model in the sidebar based on your needs:
* 🚀 **Groq (Fast/Cloud):** Best for general users with internet access.
* 🔒 **Ollama (Local/Offline):** Best for remote areas or privacy-focused queries.

### 2. Ask a Question
Try these example queries to test the system:
> * *"What is Article 21 of the Constitution?"* (Constitutional)
> * *"My landlord is not returning my security deposit. Draft a legal notice."* (Civil)
> * *"Can a police officer arrest a woman after sunset?"* (Criminal)

### 3. Enable Web Search
Check the **"Enable Web Search"** box to include recent case laws (e.g., *Right to Privacy judgments 2024*) in the answer.

---

## 🔮 Future Roadmap

* [ ] **🎙️ Voice-to-Justice (Bhashini):** Add support for regional Indian languages (Hindi, Bengali, Tamil) via voice input.
* [ ] **📄 Document Analysis:** Allow users to upload legal notices or FIR copies for instant summarization.
* [ ] **🤝 Vakil Connect:** One-click integration to book appointments with pro-bono lawyers.
* [ ] **📱 Mobile App:** Port the prototype to Flutter/React Native for wider accessibility.