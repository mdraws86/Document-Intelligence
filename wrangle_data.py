# Modules
from pathlib import Path
from typing import List, Dict
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

def load_and_chunk(path: str) -> List[Document]:
    """Load a PDF contract and split it into text chunks.

    Input:
        path (str): Path to the PDF file.

    Output:
        List[Document]: List of chunked document objects.
    """
    # Load PDF file
    loader = PyPDFLoader(path)
    
    # Each page is treated as a separate document
    documents = loader.load()

    # Define a text splitter for structured chunking
    text_splitter = RecursiveCharacterTextSplitter(
        separators=[
            r"\n(?=[^:\n]{3,100}:)",  # split on lines with a colon header
            "\n\n",                    # split on double newline
            "\n",                      # split on single newline
        ],
        is_separator_regex=True,
        chunk_size=800,              # max chunk size in characters
        chunk_overlap=100            # overlap between chunks
    )

    # Split documents into chunks
    chunks = text_splitter.split_documents(documents)
    return chunks

def build_retriever(chunks: List[Document]) -> BaseRetriever:
    """Create a FAISS-based retriever from document chunks.

    Input:
        chunks (List[Document]): List of chunked document objects.

    Output:
        BaseRetriever: Configured retriever for similarity search.
    """
    # Initialize embeddings model
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-base-en-v1.5"
    )

    # Build FAISS vector store from the document chunks
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # Convert the vector store into a retriever object
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 10}  # retrieve 10 most relevant chunks
    )

    return retriever

def build_context(retriever: BaseRetriever) -> str:
    """Query a retriever and assemble a consolidated context string.

    Input:
        retriever (BaseRetriever): Retriever object supporting `.invoke()`.

    Output:
        str: Combined context from relevant document chunks.
    """
    # Predefined queries for contract extraction
    queries = [
        "who are the parties to this agreement",
        "payment terms fees pricing amount currency",
        "contract term duration start date end date renewal termination",
        "governing law jurisdiction liability indemnification",
        "services scope deliverables obligations responsibilities",
        "signature date signed by parties"
    ]

    retrieved_chunks = []

    # Retrieve relevant chunks for each query
    for q in queries:
        docs = retriever.invoke(q)
        retrieved_chunks.extend(docs)

    # Build final context with page references
    context = "\n\n".join(
        [f"[Source: page {doc.metadata.get('page', '?')}]\n{doc.page_content}" for doc in retrieved_chunks]
    )

    return context