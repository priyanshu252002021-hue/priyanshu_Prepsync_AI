import google.generativeai as genai
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2

#  Initialize app
app = FastAPI()

#  Configure Gemini
genai.configure(api_key="AIzaSyBIDNFiael-QwaMYZnofNVoExYJbjOrfP4")

model = genai.GenerativeModel("gemini-pro") 

#  CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Upload PDF
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file.file)

    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text()

    return {"text": text}


#  AI Summary (Gemini)
from transformers import pipeline

# load model once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.post("/summarize")
async def summarize(data: dict):
    text = data.get("text", "")

    if not text.strip():
        return {"summary": "No text found"}

    try:
        chunk_size = 500
        text_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

        summaries = []

        for chunk in text_chunks[:5]:
            result = summarizer(
                "summarize: " + chunk,
                max_length=120,
                min_length=40,
                do_sample=False
            )

            # depending on the pipeline/model, use the correct key
            piece = result[0].get("summary_text") or result[0].get("generated_text") or ""
            summaries.append(piece)

        final_summary = " ".join(summaries)
        return {"summary": final_summary}

    except Exception as e:
        return {"summary": f"Error: {str(e)}"}
#  AI Quiz (Gemini)
@app.post("/quiz")
async def quiz(data: dict):
    import re, random

    text = data.get("text", "")
    difficulty = data.get("difficulty", "medium")

    sentences = re.split(r'(?<=[.!?]) +', text)
    sentences = [s for s in sentences if len(s.split()) > 6][:10]

    quiz = []

    for s in sentences[:5]:
        words = s.split()

        # Difficulty logic
        if difficulty == "easy":
            keyword = words[len(words)//2]
        elif difficulty == "hard":
            keyword = max(words, key=len)
        else:
            keyword = random.choice(words)

        if len(keyword) < 4:
            continue

        question_text = s.replace(keyword, "_____")

        # Options
        all_words = list(set(text.split()))
        options = random.sample(all_words, min(3, len(all_words)))
        options.append(keyword)
        options = list(set(options))
        random.shuffle(options)

        quiz.append({
            "question": question_text,
            "options": options[:4],
            "answer": keyword,
            "explanation": f"The correct word is '{keyword}' because it completes the sentence meaningfully."
        })

    return {"quiz": quiz}

@app.post("/ask")
async def ask_question(data: dict):
    text = data.get("text", "")
    question = data.get("question", "").lower()

    # Simple rule-based answering
    sentences = text.split(".")

    relevant = []

    for s in sentences:
        if any(word in s.lower() for word in question.split()):
            relevant.append(s.strip())

    if not relevant:
        return {"answer": "Sorry, I could not find relevant information."}

    answer = ". ".join(relevant[:3])

    return {"answer": answer}