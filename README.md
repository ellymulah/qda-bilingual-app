# QDA Bilingual App

A bilingual (Arabic/English) Qualitative Data Analysis application inspired by ATLAS.ti, featuring audio transcription, AI-powered analysis, and interactive document review.

## Features

- **Bilingual Support**: Full Arabic and English language support with automatic detection
- **Audio Transcription**: Upload audio files and automatically transcribe using Gemini AI
- **Template-Based Analysis**: Pre-defined analysis templates for qualitative research
- **Interactive Document Chat**: Ask questions about your documents and transcripts
- **Modern UI**: React-based responsive interface with RTL support for Arabic
- **FastAPI Backend**: High-performance Python backend

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Google Gemini API key

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
export GOOGLE_API_KEY="your_key_here"
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Project Structure
```
qda-bilingual-app/
├── backend/          # FastAPI application
│   ├── app/
│   │   ├── main.py   # API endpoints
│   │   └── models.py
│   ├── requirements.txt
│   └── Dockerfile
└── frontend/         # React application
    ├── src/
    │   ├── App.jsx
    │   └── main.jsx
    └── package.json
```

## License
MIT License
