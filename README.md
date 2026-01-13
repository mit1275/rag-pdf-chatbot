# 🤖 RAG PDF Chatbot

AI-powered Q&A assistant using RAG (Retrieval Augmented Generation) to answer questions from PDF documents. Built with LangChain, OpenAI GPT-4, and Qdrant vector database.

## ✨ Features

- 🤖 **GPT-4 Powered**: Intelligent answers using OpenAI's GPT-4o model
- 📄 **PDF Processing**: Automatic document parsing and text extraction
- 🔍 **Semantic Search**: Advanced vector similarity search with embeddings
- 💾 **Persistent Storage**: Qdrant vector database for efficient retrieval
- 🚀 **Production Ready**: Environment-based configuration for easy deployment
- 🔄 **Smart Caching**: Avoids re-embedding documents on subsequent runs
- 💬 **Interactive CLI**: Simple command-line interface for Q&A

## 🛠️ Tech Stack

- **LangChain** - Framework for LLM applications
- **OpenAI** - GPT-4o for generation, text-embedding-3-large for embeddings
- **Qdrant** - Vector database for semantic search
- **PyPDF** - PDF document processing
- **Python-dotenv** - Environment variable management

## 📋 Prerequisites

- Python 3.11+
- Docker & Docker Compose (for Qdrant)
- OpenAI API key

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/mit1275/rag-pdf-chatbot.git
cd rag-pdf-chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory:

```bash
# OpenAI API Key (required)
OPENAI_API_KEY=sk-your-api-key-here

# Qdrant Configuration (optional, defaults shown)
QDRANT_URL=http://localhost:6333
COLLECTION_NAME=pdf_collection
```

### 4. Start Qdrant vector database

```bash
docker-compose up -d
```

This will start Qdrant on `http://localhost:6333`

### 5. Run the application

```bash
cd rag
python main.py
```

## 💡 Usage

### First Run (Creating Collection)

On the first run, you'll be prompted to upload a PDF:

```
Collection does not exist, creating a new one...
Enter the path to your PDF file: /path/to/your/document.pdf
```

The system will:
1. Load and parse the PDF
2. Split it into chunks
3. Generate embeddings
4. Store them in Qdrant

### Subsequent Runs

After the collection is created:

```
Using existing collection...

💬 RAG Assistant Ready! Type 'exit' to quit.

Enter your query: What is the main topic of the document?
Answer: [AI-generated answer based on document content]

Enter your query: exit
```

## 🏗️ Architecture

```
┌─────────────┐
│   PDF File  │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  PyPDF Loader       │
│  Text Splitter      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  OpenAI Embeddings  │
│  (text-embedding-   │
│   3-large)          │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Qdrant Vector DB   │
│  (Persistent Store) │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  User Query         │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Similarity Search  │
│  (Top-k Retrieval)  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  GPT-4o             │
│  (Answer Generation)│
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Final Answer       │
└─────────────────────┘
```

## 📁 Project Structure

```
rag-pdf-chatbot/
├── rag/
│   ├── main.py              # Main application
│   └── docker-compose.yml   # Qdrant container config
├── .env                     # Environment variables (not in repo)
├── .gitignore
├── requirements.txt         # Python dependencies
├── README.md
└── DEPLOYMENT.md           # Production deployment guide
```

## ⚙️ Configuration

### Chunk Size & Overlap

Adjust in `main.py`:

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,      # Characters per chunk
    chunk_overlap=150    # Overlap between chunks
)
```

### Retrieval Settings

Modify number of relevant chunks:

```python
results = vector_store.similarity_search_by_vector(embedded_query, k=10)  # Top 10 chunks
```

### Model Selection

Change models in `main.py`:

```python
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
llm = ChatOpenAI(model="gpt-4o")  # or gpt-4, gpt-3.5-turbo
```

## 🚢 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed production deployment instructions.

**Quick Production Setup:**

1. **Qdrant Cloud**:
   - Sign up at https://cloud.qdrant.io
   - Create cluster and get URL
   - Update `QDRANT_URL` in `.env`

2. **Deploy Options**:
   - AWS Lambda / Google Cloud Run
   - Streamlit Cloud
   - Docker container on any platform

## 🔒 Security Best Practices

- ✅ Never commit `.env` file
- ✅ Use environment variables for all secrets
- ✅ Enable authentication on Qdrant in production
- ✅ Use HTTPS for production URLs
- ✅ Rotate API keys regularly

## 📝 Example Queries

```
"Summarize the main points of this document"
"What are the key findings?"
"Explain the methodology used"
"List all recommendations mentioned"
"Who are the authors?"
```

## 🐛 Troubleshooting

### Qdrant connection fails

```bash
# Check if Qdrant is running
docker ps

# Restart Qdrant
docker-compose restart
```

### OpenAI API errors

- Verify API key in `.env`
- Check account balance at https://platform.openai.com/usage

### PDF parsing issues

- Ensure PDF is not password-protected
- Try with a different PDF to isolate the issue

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com) for the framework
- [Qdrant](https://qdrant.tech) for the vector database
- [OpenAI](https://openai.com) for GPT-4 and embeddings

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

Made with ❤️ using LangChain and OpenAI
