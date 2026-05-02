from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from rag import search
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(query):
    context = search(query)
    context_str = "\n".join(context)

    prompt = f"""
    You are a professional WhereWorks support assistant.

    Rules:
    - Answer ONLY from the given context
    - Give step-by-step answer
    - If not found say: "Not available in document"

    Context:
    {context_str}

    Question:
    {query}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/chat")
def chat(query: str):
    answer = generate_answer(query)
    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)