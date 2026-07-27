import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from typing import List

# Extracting the text from the PDF files
def load_pdf_files(data_path: str) -> List[Document]:
    loader = DirectoryLoader(data_path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

# Filter metadata to keep only source and page to save Pinecone database space and reduce payload size
def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    minimal_docs = []
    for doc in docs:
        src = doc.metadata.get("source")
        page = doc.metadata.get("page", 0)
        minimal_docs.append(
            Document(page_content=doc.page_content, metadata={"source": src, "page": page})
        )
    return minimal_docs

# Split the documents into smaller chunks
def text_split(minimal_docs: List[Document]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20,
    )
    docs = text_splitter.split_documents(minimal_docs)
    return docs

# Download/load the sentence-transformers model
def download_embeddings() -> HuggingFaceEmbeddings:
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"local_files_only": True}  # Use local files to prevent offline/network timeouts
    )
    return embeddings
