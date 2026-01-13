# Environment Variables Configuration

Copy this to `.env` and fill in your values:

```bash
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Qdrant Vector Database URL
# For local development: http://localhost:6333
# For production: https://your-qdrant-cloud-url.com or http://your-server-ip:6333
QDRANT_URL=http://localhost:6333

# Collection name for storing embeddings
COLLECTION_NAME=pdf_collection
```

## Deployment Steps

### 1. **Set up Qdrant in Production**

**Option A: Qdrant Cloud** (Recommended)
- Sign up at https://cloud.qdrant.io
- Create a cluster
- Get your cluster URL (e.g., `https://xyz.cloud.qdrant.io`)
- Update `QDRANT_URL` in your `.env`

**Option B: Self-hosted Qdrant**
- Deploy Qdrant on your server using Docker:
  ```bash
  docker run -p 6333:6333 qdrant/qdrant
  ```
- Update `QDRANT_URL` to your server IP/domain

### 2. **Update Environment Variables**

Create a `.env` file with production values:
```bash
OPENAI_API_KEY=sk-...
QDRANT_URL=https://your-qdrant-instance.com  # or http://your-server-ip:6333
COLLECTION_NAME=pdf_collection
```

### 3. **Deploy Options**

**Option 1: Deploy as API (FastAPI/Flask)**
- Wrap your RAG logic in REST API
- Deploy to AWS Lambda, Google Cloud Run, or Railway

**Option 2: Deploy as Web App (Streamlit)**
- Create Streamlit UI
- Deploy to Streamlit Cloud or Render

**Option 3: Docker Container**
- Containerize your app
- Deploy to any cloud provider

### 4. **Test Locally First**
```bash
# Make sure Docker Compose is running (for local Qdrant)
docker-compose up -d

# Run the app
python main.py
```

### 5. **Security Checklist**
- ✅ Never commit `.env` file
- ✅ Use environment variables for all secrets
- ✅ Enable authentication on Qdrant in production
- ✅ Use HTTPS for production URLs
