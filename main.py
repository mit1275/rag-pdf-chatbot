from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from a .env file if needed

# Get Qdrant URL from environment variable, default to localhost for development
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "pdf_collection")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

llm = ChatOpenAI(model="gpt-4o")

try:
        vector_store = QdrantVectorStore.from_existing_collection(
            url=QDRANT_URL,
            collection_name=COLLECTION_NAME,
            embedding=embeddings
        )
        print("Using existing collection...")
except Exception as e:
        print("Collection does not exist, creating a new one...")
        pdf_path = input("Enter the path to your PDF file: ")
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
        texts = text_splitter.split_documents(documents)
    
        vector_store = QdrantVectorStore.from_documents(
            documents=texts,
            embedding=embeddings,
            url=QDRANT_URL,
            collection_name=COLLECTION_NAME
        )

def generate_rag_answer(query):
    embedded_query = embeddings.embed_query(input_query)
    results = vector_store.similarity_search_by_vector(embedded_query, k=10)

    if not results:
        return "No relevant information found."

    context = "\n\n".join(doc.page_content for doc in results)

    system_prompt = f"""
You are a helpful assistant. U only answer questions from context give to u.

Context:
{context}

Question: {query}
Answer:
"""

    response = llm.invoke(system_prompt)
    return response.content


print("\n💬 RAG Assistant Ready! Type 'exit' to quit.\n")
while True :
    input_query = input("Enter your query: ")
    if input_query.lower() == "exit":
        break
    answer = generate_rag_answer(input_query)
    print(f"Answer: {answer}\n")