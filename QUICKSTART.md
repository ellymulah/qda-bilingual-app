# Quick Start Guide

## Running the App with Docker (Recommended)

### Prerequisites
- Docker and Docker Compose installed
- Google Gemini API key

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/ellymulah/qda-bilingual-app.git
cd qda-bilingual-app
```

2. **Set up environment variables**
```bash
# Create .env file in the root directory
echo "GOOGLE_API_KEY=AIzaSyCcMfEt0APQ" > .env
```

3. **Run with Docker Compose**
```bash
docker-compose up --build
```

4. **Access the application**
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

## Running Without Docker

### Backend

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export GOOGLE_API_KEY=AIzaSyCcMfEt0APQ

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
# Navigate to frontend (in a new terminal)
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## Testing the API

### Check Health
```bash
curl http://localhost:8000/
```

### List Templates
```bash
curl http://localhost:8000/templates
```

### Test Language Detection
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"transcript_id": "test", "template_id": "interview_quality"}'
```

## Features Available

✅ Audio upload and transcription
✅ Bilingual support (Arabic/English)
✅ AI-powered analysis with Gemini
✅ Template-based analysis
✅ Document interaction
✅ Language detection

## Troubleshooting

**Port already in use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Docker issues:**
```bash
# Clean up and rebuild
docker-compose down -v
docker-compose up --build
```

## Next Steps

- See [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md) for production deployment
- Check [ARABIC_COPILOT.md](ARABIC_COPILOT.md) for Arabic features
- Review API documentation at http://localhost:8000/docs
