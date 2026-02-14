import os
import streamlit as st
from typing import TypedDict, List
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()
st.set_page_config(page_title="Samvidhan-Sathi", page_icon="🇮🇳", layout="wide")

with st.sidebar:
    st.header("⚙️ Configuration")
    llm_choice = st.radio("Select AI Model:", ["Groq (Fast/Cloud)", "Ollama (Local/Offline)"])
    enable_web_search = st.checkbox("Enable Web Search (Recommended)", value=True)
    
    st.divider()
    st.info("💡 Note: 'Ollama' requires the app running locally. \n'Groq' requires Internet. \nDisable Web Search in case of No Internet")

if llm_choice == "Groq (Fast/Cloud)":
    if "GROQ_API_KEY" not in os.environ:
        st.error("Missing GROQ_API_KEY in .env")
        st.stop()
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
else:
    llm = ChatOllama(model="llama3.1-8b-clean", temperature=0.7, num_ctx=4096)

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

if enable_web_search and "TAVILY_API_KEY" in os.environ:
    web_search_tool = TavilySearchResults(max_results=2, topic="news", exclude_domains=["quora.com", "reddit.com", "medium.com", "linkedin.com"])
else:
    web_search_tool = None

class GraphState(TypedDict):
    question: str
    chat_history: List[str]
    category: str
    context: str
    web_results: str
    response: str

memory = MemorySaver()


def node_categorize(state: GraphState):
    """Classifies the question."""
    question = state["question"]
    prompt = PromptTemplate.from_template(
        "Classify the legal question into exactly one category: "
        "'Civil', 'Criminal', 'Constitutional', or 'General'. Return ONLY the category name.\nQuestion: {question}"
    )
    chain = prompt | llm | StrOutputParser()
    try:
        category = chain.invoke({"question": question}).strip()
    except:
        category = "General"
    return {"category": category}

def node_research_local(state: GraphState):
    """Retrieves from ChromaDB (COI.json)."""
    question = state["question"]
    docs = retriever.invoke(question)
    context = "\n\n".join([d.page_content for d in docs]) if docs else "No local laws found."
    return {"context": context}

def node_web_search(state: GraphState):
    """Searches the web for recent Indian legal cases."""
    if not web_search_tool:
        return {"web_results": "Web search disabled."}
    
    question = state["question"]
    print(f"--- Searching Web: {question} ---")
    
    try:
        search_query = f"{question} related to India legal news"
        results = web_search_tool.invoke({"query": search_query})
        if isinstance(results, list):
            formatted_results = "\n".join(
                [f"- {r.get('content', '')} (Source: {r.get('url', '')})" for r in results]
            )
        else:
            formatted_results = str(results)
            
        return {"web_results": formatted_results}
        
    except Exception as e:
        print(f"Error in web search: {e}")
        return {"web_results": "No recent cases found due to search error."}

def node_draft(state: GraphState):
    """Drafts response using Context + Web Results + Chat History."""
    question = state["question"]
    context = state["context"]
    web_data = state.get("web_results", "")
    category = state["category"]

    template = """
    You are 'Samvidhan-Sathi', an expert Indian Legal AI Assistant.
    
    USER QUESTION: {question}
    CATEGORY: {category}
    
    1. CONSTITUTIONAL CONTEXT (Local DB):
    {context}
    
    2. WEB SEARCH CONTEXT (Recent Cases/News):
    {web_data}
    
    INSTRUCTIONS:
    - Synthesize the answer using BOTH the Constitution and (if available) Web Search.
    - If the user asks about something not in the Constitution (like a recent 2024 case), rely on Web Search.
    - If can't find direct laws for issues, mention as not found in Constitute of India.
    - If the question is not related to legal issue, mention to describe issues to get legal opinion based on Constitution of India.
    - If the question is not related to legal Issue, or Web Search not needed, or websearch is disabled, no need to give Recent Context Point.
    - Structure: 
      1. **Simplification**: Explain clearly.
      2. **Legal Basis**: Cite Articles from the Local Context. Give a positive tone as the law is in the user's favour.
        > **Description**: write what the selected Article states from the local DB.
      3. **Recent Context**: Mention insights from Web Search if relevant.
      4. **Next Steps**: Practical advice.
    - If any contact is required for next step, provide the cntact details.
    - If the question is not related to legal Issue, or Web Search not needed, or websearch is disabled, no need to give Recent Context Point.
    """
    
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    
    response = chain.invoke({
        "question": question,
        "context": context,
        "web_data": web_data,
        "category": category
    })
    
    return {"response": response}


workflow = StateGraph(GraphState)

workflow.add_node("categorize", node_categorize)
workflow.add_node("research_local", node_research_local)
workflow.add_node("web_search", node_web_search)
workflow.add_node("draft", node_draft)


workflow.add_edge("categorize", "research_local")
workflow.add_edge("research_local", "web_search")
workflow.add_edge("web_search", "draft")
workflow.add_edge("draft", END)

workflow.set_entry_point("categorize")

app_graph = workflow.compile(checkpointer=memory)

st.title("Samvidhan-Sathi")
st.caption("Your own Samvidhan-Assistant.")


if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "user_session_1"


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


if user_input := st.chat_input("Ask about Indian Law..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    config = {"configurable": {"thread_id": st.session_state.thread_id}}

    with st.status("🤖 Processing...", expanded=True) as status:
        st.write("🔹 Analyzing intent...")
        
        result = app_graph.invoke(
            {"question": user_input, "chat_history": []}, 
            config=config
        )
        
        st.write(f"🔹 Category: **{result['category']}**")
        st.write("🔹 Searching Constitution & Web...")
        status.update(label="✅ Response Ready", state="complete", expanded=False)


    final_response = result["response"]
    with st.chat_message("assistant"):
        st.markdown(final_response)
    st.session_state.messages.append({"role": "assistant", "content": final_response})