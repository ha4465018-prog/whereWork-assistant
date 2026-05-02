# whereWork-assistant
WhereWork AI: A high-performance PDF chatbot featuring vector search (FAISS), lightning-fast LLM responses via Groq, and a clean web UI.
# WhereWork AI Assistant

WhereWork AI is a smart, context-aware chatbot built with FastAPI and a Retrieval-Augmented Generation (RAG) pipeline. It provides instant answers to user queries based on a provided knowledge base (PDF manual).

## Features

- **FastAPI Backend:** High-performance RESTful API.
- **RAG System:** Extracts, chunks, and processes text from PDF documents.
- **Vector Search:** Uses `sentence-transformers` and `FAISS` for fast and accurate similarity search.
- **LLM Integration:** Powered by the cutting-edge `llama-3.3-70b-versatile` model via the **Groq API** for rapid text generation.
- **Responsive UI:** A clean frontend interface built with Jinja2 templates and static web assets.
- **Caching Mechanism:** Saves the FAISS index to disk (`index_cache.pkl`) to ensure lightning-fast startup times on subsequent runs.

## Project Structure

```text
wherework-ai/
├── datamanual/
│   ├── manual.pdf          # Knowledge base document
│   └── index_cache.pkl     # Generated FAISS index cache (created automatically)
├── static/                 # Static assets (CSS, JS, images)
├── templates/
│   └── index.html          # Chatbot user interface
├── main.py                 # FastAPI application, route definitions, and LLM prompt logic
├── rag.py                  # RAG pipeline: PDF extraction, embedding generation, vector search
├── test_api.py             # Script for testing the API endpoint
├── test_rag.py             # Script for testing the RAG functionality
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables (API keys)
```

## Prerequisites

- Python 3.8 or higher
- A [Groq API Key](https://console.groq.com/keys)

## Installation & Setup

1. **Navigate to the project directory:**
   ```bash
   cd wherework-ai
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Ensure you have a `.env` file in the root directory containing your API keys:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   # Optional: Hugging Face token if needed for downloading sentence-transformers
   HF_TOKEN=your_huggingface_token_here
   ```

5. **Prepare the Knowledge Base:**
   Ensure your source document is named `manual.pdf` and placed inside the `datamanual/` directory.

## Running the Application

You can start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
```
Alternatively, simply run the main script:
```bash
python main.py
```

The server will be available at `http://127.0.0.1:8000`.

### Usage

- **Web UI:** Open your browser and navigate to `http://127.0.0.1:8000/` to interact with the web-based chatbot.
- **REST API:** You can programmatically query the chat API via a GET request:
  `http://127.0.0.1:8000/chat?query=your_question`

## How It Works

1. **Initialization:** On startup, `rag.py` checks for an existing index cache (`datamanual/index_cache.pkl`). If it doesn't exist, it reads `manual.pdf`, splits the text into chunks, generates vector embeddings using `all-MiniLM-L6-v2`, and builds a FAISS index.
2. **Retrieval:** When a user submits a query, the application converts the question into an embedding and performs a similarity search against the FAISS index to find the most relevant text chunks from the PDF.
3. **Generation:** The retrieved context and the user's query are passed to the Groq API. The LLM generates a strictly context-aware response, which is then returned to the user interface.

