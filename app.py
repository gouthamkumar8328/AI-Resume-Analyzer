from fastapi import FastAPI, UploadFile, File
import shutil
import os
import json

from services.pdf_parser import extract_text
from services.summarizer import generate_summary

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "AI Resume Analyzer API is Running 🚀"
    }


@app.post("/summarize-pdf")
async def summarize_pdf(file: UploadFile = File(...)):

    # Save uploaded PDF
    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # Extract text from PDF
    text = extract_text(file_path)

    # Get AI analysis
    analysis = generate_summary(text)

    print("\n===== GROQ RESPONSE =====")
    print(analysis)
    print("=========================\n")

    try:
        cleaned = analysis.strip()

        if cleaned.startswith('"') and cleaned.endswith('"'):
            cleaned = json.loads(cleaned)

        data = json.loads(cleaned)

        data["filename"] = file.filename

        return data

    except Exception as e:
        return {
            "filename": file.filename,
            "error": str(e),
            "raw_response": analysis
    }