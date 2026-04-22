from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PDF Upload + Text Extraction
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    text = ""
    
    pdf_reader = PyPDF2.PdfReader(file.file)
    
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    return {"text": text}


# Simple Summarizer (basic version)
@app.post("/summarize")
async def summarize(data: dict):
    text = data.get("text", "")
    
    # VERY basic summary (first 3 lines)
    summary = " ".join(text.split()[:100])
    
    return {"summary": summary}


# Quiz Generator (basic)
@app.post("/quiz")
async def quiz(data: dict):
    text = data.get("text", "")
    
    words = text.split()[:5]
    
    questions = []
    for word in words:
        questions.append(f"What is {word}?")
    
    return {"quiz": questions}