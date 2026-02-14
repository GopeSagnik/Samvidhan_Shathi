import os
import json
import shutil
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

load_dotenv()

JSON_PATH = "COI.json"
CHROMA_PATH = "./chroma_db"
EMBEDDING_MODEL = "nomic-embed-text" 

def setup_knowledge_base():

    if os.path.exists(CHROMA_PATH):
        print(f"✅ Knowledge Base already exists at {CHROMA_PATH}. Skipping build.")
        return

    if not os.path.exists(JSON_PATH):
        print(f"❌ Error: {JSON_PATH} not found.")
        return

    print("🔄 Loading JSON and Building Knowledge Base...")


    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error reading JSON: {e}")
        return

    print(f"   - Found {len(data)} articles in JSON.")

    documents = []
    for entry in data:

        page_content = f"Article {entry.get('article', 'N/A')}: {entry.get('title', '')}\n\n{entry.get('description', '')}"
        
        metadata = {
            "article_id": entry.get('article'),
            "title": entry.get('title')
        }
        
        documents.append(Document(page_content=page_content, metadata=metadata))

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    print(f"   - Created {len(chunks)} searchable chunks.")

    print(f"   - Embedding using Ollama model: {EMBEDDING_MODEL}...")
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    
    Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=CHROMA_PATH
    )
    
    print("✅ Knowledge Base built and saved successfully!")

if __name__ == "__main__":
    setup_knowledge_base()