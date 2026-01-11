from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import os
from google import genai
from fast_langdetect import detect

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

TRANSCRIPTS: Dict[str, dict] = {}
TEMPLATES: Dict[str, dict] = {
    "interview_quality": {
        "id": "interview_quality",
        "name": "Interview quality review",
        "system_prompt": (
            "You are a qualitative methods assistant. "
            "Given this transcript, evaluate depth of probing, "
            "participant comfort, and ethics. "
            "Respond in JSON with keys: strengths, weaknesses, "
            "suggested_questions, flags."
        ),
    }
}

client = genai.Client()

def detect_lang(text: str) -> str:
    if not text.strip():
        return "unknown"
    result = detect(text, low_memory=False)
    lang = result.get("lang", "unknown")
    if lang.startswith("ar"):
        return "ar"
    if lang.startswith("en"):
        return "en"
    return lang

class AnalyzeRequest(BaseModel):
    transcript_id: str
    template_id: str
    language: str = "auto"

class ChatRequest(BaseModel):
    document_text: str
    question: str
    language: str = "auto"

@app.get("/templates")
def list_templates():
    return list(TEMPLATES.values())

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=415, detail="File must be audio")

    file_id = os.path.splitext(file.filename)[0]
    filepath = os.path.join(UPLOAD_DIR, file.filename)

    with open(filepath, "wb") as f:
        while chunk := await file.read(1024 * 1024):
            f.write(chunk)

    with open(filepath, "rb") as f:
        audio_bytes = f.read()

    resp = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[
            "Transcribe this audio (Arabic or English), then provide a short summary.",
            genai.types.Part.from_bytes(data=audio_bytes, mime_type=file.content_type),
        ],
    )

    transcript_text = resp.text
    lang = detect_lang(transcript_text)

    TRANSCRIPTS[file_id] = {
        "id": file_id,
        "filename": file.filename,
        "text": transcript_text,
        "summary": "Prototype summary; parse from resp if structured.",
        "language": lang,
    }
    return {"transcript_id": file_id, "text": transcript_text, "language": lang}

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    transcript = TRANSCRIPTS.get(req.transcript_id)
    template = TEMPLATES.get(req.template_id)
    if not transcript or not template:
        raise HTTPException(status_code=404, detail="Not found")

    lang = req.language
    if lang == "auto":
        lang = transcript.get("language", "en")

    prompt = (
        f"{template['system_prompt']}\n\n"
        f"Transcript (language={lang}):\n{transcript['text']}"
    )
    resp = client.models.generate_content(model="gemini-2.0-flash-exp", contents=[prompt])

    return {"feedback": resp.text}

@app.post("/chat")
def chat(req: ChatRequest):
    lang = req.language
    if lang == "auto":
        lang = detect_lang(req.document_text or req.question)

    prompt = (
        "You are an assistant for qualitative analysis. "
        "Answer ONLY from the provided document text. "
        f"Respond in the user language: {lang}.\n\n"
        f"Document:\n{req.document_text}\n\nQuestion:\n{req.question}"
    )
    resp = client.models.generate_content(model="gemini-2.0-flash-exp", contents=[prompt])
    return {"answer": resp.text}
