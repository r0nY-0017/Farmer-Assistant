# 🌾 AI Farmer Assistant

ফসলের ছবি দিলে OpenAI Vision (GPT-4o) দিয়ে রোগ চিহ্নিত করে **বাংলায়** চিকিৎসা ও পরামর্শ দেয়।

## ✅ Features
- ছবি আপলোড করে ফসলের রোগ detect
- বাংলায় রোগের নাম, কারণ, চিকিৎসা, প্রতিরোধ
- সুন্দর web UI দিয়ে local test
- Drag & drop image support
- FastAPI Swagger docs (`/docs`)

## 🚀 Local Setup

### 1. Clone / ফোল্ডার তৈরি করো
```bash
cd ai-farmer-assistant
```

### 2. Virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Dependencies install
```bash
pip install -r requirements.txt
```

### 4. .env ফাইল তৈরি করো
```bash
cp .env.example .env
```
`.env` ফাইল খুলে `OPENAI_API_KEY` এর জায়গায় তোমার API key বসাও:
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxx
```

### 5. Server চালু করো
```bash
uvicorn app.main:app --reload
```

### 6. Browser এ যাও
```
http://localhost:8000          → Web UI (ছবি আপলোড করে test করো)
http://localhost:8000/docs     → Swagger API docs
```

## 📁 Project Structure
```
ai-farmer-assistant/
├── app/
│   ├── api/
│   │   └── disease.py          # POST /disease/analyze endpoint
│   ├── services/
│   │   └── vision_service.py   # OpenAI Vision API wrapper
│   ├── core/
│   │   └── config.py           # Settings
│   └── main.py                 # FastAPI app + Web UI
├── uploads/                    # আপলোড করা ছবি সেভ হয় এখানে
├── requirements.txt
├── .env.example
└── README.md
```

## 🔌 API Usage (cURL)
```bash
curl -X POST http://localhost:8000/disease/analyze \
  -F "image=@/path/to/crop.jpg" \
  -F "crop_name=টমেটো"
```

## 📊 Sample Response
```json
{
  "success": true,
  "analysis": {
    "detected": true,
    "crop_name": "টমেটো",
    "disease_name": "আর্লি ব্লাইট (Early Blight)",
    "confidence": "high",
    "symptoms": ["পাতায় বাদামি দাগ", "দাগের চারপাশে হলুদ রিং"],
    "causes": "Alternaria solani ছত্রাকের আক্রমণ",
    "treatment": ["Mancozeb ছত্রাকনাশক স্প্রে করুন", "আক্রান্ত পাতা সরিয়ে ফেলুন"],
    "prevention": ["ফসল পর্যায়ক্রমে বদলান", "অতিরিক্ত পানি দেওয়া এড়িয়ে চলুন"],
    "urgency": "medium",
    "summary": "টমেটোতে আর্লি ব্লাইট রোগ দেখা যাচ্ছে। দ্রুত ব্যবস্থা নিন।"
  }
}
```

## 🔮 Next Steps (GitHub এ add করার পরে)
- [ ] PostgreSQL দিয়ে diagnosis history সেভ
- [ ] JWT Auth (farmer login)
- [ ] Weather API integration
- [ ] SMS alert (Twilio)
- [ ] Docker deployment
