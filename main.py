from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from a .env file if needed

# Get Qdrant config
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "pdf_collection")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
llm = ChatOpenAI(model="gpt-4o")   # can be gpt-4.1 / mini too

# ---------- VECTOR STORE SETUP ----------
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

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    texts = text_splitter.split_documents(documents)

    vector_store = QdrantVectorStore.from_documents(
        documents=texts,
        embedding=embeddings,
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME
    )


# ---------- RAG ANSWER ----------
def generate_rag_answer(query):
    embedded_query = embeddings.embed_query(query)
    results = vector_store.similarity_search_by_vector(embedded_query, k=10)

    if not results:
        return "No relevant information found."

    context = "\n\n".join(doc.page_content for doc in results)

    prompt = f"""
You are a helpful assistant. Only answer using the provided context.
If answer is not in the context, reply: "Not found in document".

Context:
{context}

Question: {query}
Answer:
"""

    response = llm.invoke([{"role": "user", "content": prompt}])
    return response.content


# ---------- LOOP ----------
print("\n💬 RAG Assistant Ready! Type 'exit' to quit.\n")

while True:
    input_query = input("Enter your query: ")
    if input_query.lower() == "exit":
        break

    answer = generate_rag_answer(input_query)
    print(f"\nAnswer:\n{answer}\n")
