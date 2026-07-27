import os
import sys
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Set offline mode for Hugging Face to prevent connection timeouts and latency
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

if not GOOGLE_API_KEY or not PINECONE_API_KEY:
    print("Error: GOOGLE_API_KEY or PINECONE_API_KEY is not set in environment.")
    sys.exit(1)

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

from src.helper import download_embeddings
from src.prompt import system_prompt
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__)

# Initialize Retriever and RAG chain
print("Initializing embeddings and vector store...")
embeddings = download_embeddings()
index_name = "medical-chatbot"
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 4})

print("Initializing Gemini LLM model...")
chatModel = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0.7,
    max_retries=1
)

# Setup prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}")
    ]
)

print("Constructing RAG chain...")
question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)
print("Application setup complete. Ready to serve requests!")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get", methods=["POST"])
def chat():
    user_message = request.form.get("msg", "").strip()
    if not user_message:
        return jsonify({"response": "Please enter a message.", "sources": []})
    
    print(f"User query received: {user_message}")
    try:
        response = rag_chain.invoke({"input": user_message})
        answer = response.get("answer", "I could not generate an answer.")
        
        # Extract sources from retrieved documents
        sources = []
        for doc in response.get("context", []):
            src = doc.metadata.get("source", "Unknown Source")
            # Format source name for display (e.g. data\Medbook.pdf -> Medbook.pdf)
            base_src = os.path.basename(src)
            page = doc.metadata.get("page")
            page_str = f"Page {int(page) + 1}" if page is not None else "Unknown Page"
            sources.append({"source": base_src, "page": page_str})
            
        # De-duplicate sources
        unique_sources = []
        seen = set()
        for s in sources:
            key = (s["source"], s["page"])
            if key not in seen:
                seen.add(key)
                unique_sources.append(s)
                
        return jsonify({"response": answer, "sources": unique_sources})
    except Exception as e:
        print(f"Error invoking RAG chain: {e}")
        return jsonify({"response": "Sorry, an error occurred while processing your request.", "sources": []})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085, debug=True)
