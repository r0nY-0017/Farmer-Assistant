# 🌾 AI Farmer Assistant

Analyzes crop images using OpenAI Vision (GPT-4o) to detect diseases and provides treatment and advice in **Bengali**.

## ✅ Features
- Crop disease detection by uploading images
- Disease name, causes, treatment, and prevention in Bengali
- Beautiful web UI for local testing
- Drag & drop image support
- FastAPI Swagger docs (`/docs`)

## 🚀 Local Setup

### 1. Clone / Create Folder
```bash
cd ai-farmer-assistant
```

### 2. Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create .env File
```bash
cp .env.example .env
```
Open the `.env` file and replace `OPENAI_API_KEY` with your actual API key:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxx
```

### 5. Start the Server
```bash
uvicorn app.main:app --reload
```

### 6. Open in Browser
```
http://localhost:8000          → Web UI (Test by uploading an image)
http://localhost:8000/docs     → Swagger API docs
```

## 📁 Project Structure
```text
ai-farmer-assistant/
├── app/
│   ├── api/
│   │   └── disease.py          # POST /disease/analyze endpoint
│   ├── services/
│   │   └── vision_service.py   # OpenAI Vision API wrapper
│   ├── core/
│   │   └── config.py           # Settings
│   └── main.py                 # FastAPI app + Web UI
├── uploads/                    # Uploaded images are saved here
├── requirements.txt
├── .env.example
└── README.md
```

## 🔌 API Usage (cURL)
```bash
curl -X POST http://localhost:8000/disease/analyze \
  -F "image=@/path/to/crop.jpg" \
  -F "crop_name=Tomato"
```

## 📊 Sample Response
```json
{
  "success": true,
  "analysis": {
    "detected": true,
    "crop_name": "Tomato",
    "disease_name": "Early Blight",
    "confidence": "high",
    "symptoms": ["Brown spots on leaves", "Yellow rings around the spots"],
    "causes": "Alternaria solani fungus attack",
    "treatment": ["Spray Mancozeb fungicide", "Remove infected leaves"],
    "prevention": ["Rotate crops periodically", "Avoid excessive watering"],
    "urgency": "medium",
    "summary": "Early blight disease is visible on the tomato. Take immediate action."
  }
}
```

## 🔮 Next Steps (After pushing to GitHub)
- [ ] Save diagnosis history using PostgreSQL
- [ ] JWT Auth (farmer login)
- [ ] Weather API integration
- [ ] SMS alert (Twilio)
- [ ] Docker deployment
