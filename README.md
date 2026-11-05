# 🩺 Medical Chatbot (Virtual Doctor)

An AI-powered medical chatbot that uses **Retrieval-Augmented Generation (RAG)** to provide fast, context-aware, and accurate responses to medical queries. 

## 🚀 Overview
This project is a full-stack application designed to act as a virtual doctor. Instead of relying solely on the LLM's pre-trained knowledge (which can hallucinate), this chatbot retrieves relevant information from a custom medical knowledge base using vector embeddings before generating a response.

## 🧠 Architecture & Tech Stack
*   **Core Concept:** RAG (Retrieval-Augmented Generation)
*   **Vector Database:** Pinecone (for semantic search and context retrieval)
*   **LLM:** Gemini-3.5-flash
*   **Backend:** Python (Flask)
*   **Frontend:** HTML, CSS, JavaScript
*   **Environment/Tools:** Google Colab, Jupyter Notebook, VS Code

## 📂 Repository Structure
*   `app.py` - Main application entry point (Backend server).
*   `src/` - Core logic, including RAG pipeline and LLM integration.
*   `data/` - Medical knowledge base / documents used for embedding.
*   `research/` - Experiments and Jupyter notebooks used during development.
*   `static/` & `templates/` - Frontend UI and assets.
*   `requirements.txt` - Python dependencies.

## ⚙️ How It Works
1.  **Ingestion:** Medical data is chunked, converted into vector embeddings, and stored in the **Pinecone** vector database.
2.  **Retrieval:** When a user asks a question, the query is embedded, and Pinecone retrieves the most relevant medical context.
3.  **Generation:** The retrieved context and the user's query are sent to the **Gemini-3.5-flash** model to generate a precise, grounded answer.

## 🛠️ Installation & Setup (Local)

1. **Clone the repository:**
   git clone https://github.com/monisharani1/Medical-chatbot.git
   cd Medical-chatbot

2. **Create a virtual environment & install dependencies:**
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt

3. **Set up Environment Variables:**
   Create a `.env` file in the root directory and add your API keys:
   PINECONE_API_KEY=your_pinecone_api_key
   GEMINI_API_KEY=your_gemini_api_key

4. **Run the application:**
   python app.py

## 👨‍💻 Author
**Monisha Rani**
*   Final Year B.E. Computer Science (Data Science) Student
*   Specialization: AI & ML
*   [GitHub Profile](https://github.com/monisharani1)

---
*Disclaimer: This chatbot is for informational purposes only and does not constitute professional medical advice. Always consult a qualified healthcare provider for medical concerns.*
