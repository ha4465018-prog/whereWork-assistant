from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# HF token for authenticated Hugging Face downloads
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN", "")

# Paths
PDF_PATH = "datamanual/manual.pdf"
CACHE_PATH = "datamanual/index_cache.pkl"

def build_index():
    """Build FAISS index from PDF and cache it to disk."""
    print("[INFO] Loading PDF and building index...")

    reader = PdfReader(PDF_PATH)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    chunks = chunk_text(text)

    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(chunks, show_progress_bar=True)

    dimension = embeddings.shape[1]
    idx = faiss.IndexFlatL2(dimension)
    idx.add(np.array(embeddings))

    # Save to cache
    with open(CACHE_PATH, "wb") as f:
        pickle.dump({"chunks": chunks, "embeddings": embeddings, "dimension": dimension}, f)

    print("[INFO] Index built and cached.")
    return idx, chunks, model


def load_index():
    """Load cached FAISS index from disk."""
    print("[INFO] Loading cached index...")
    with open(CACHE_PATH, "rb") as f:
        data = pickle.load(f)

    chunks = data["chunks"]
    embeddings = data["embeddings"]
    dimension = data["dimension"]

    idx = faiss.IndexFlatL2(dimension)
    idx.add(np.array(embeddings))

    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("[INFO] Cached index loaded.")
    return idx, chunks, model


def chunk_text(text, chunk_size=400, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


# Load or build index on startup
if Path(CACHE_PATH).exists():
    index, chunks, model = load_index()
else:
    index, chunks, model = build_index()


# Search function
def search(query, k=3):
    query_vector = model.encode([query])
    distances, indices = index.search(np.array(query_vector), k)
    return [chunks[i] for i in indices[0]]