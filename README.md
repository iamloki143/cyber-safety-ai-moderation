# Cyber Safety AI Moderation System

An AI-powered content moderation system designed to detect **toxic text, NSFW images, and violent content in videos** using modern deep learning models.

---

# Features

## Text Moderation
- Detects toxic / abusive language
- Supports English + Tanglish (Tamil-English mix)
- Uses **Toxic-BERT + rule-based filtering**

## Image Moderation
- NSFW (adult content) detection
- Violence detection using CLIP
- Caption-based explainability (BLIP)

## Video Moderation
- Frame-by-frame analysis
- Uses image models on sampled frames
- Aggregated risk scoring

## Dashboard & Logging
- MongoDB-based logging
- Risk score calculation
- CSV export support

---

# Project Structure

cyber-safety-ai-moderation/
│
├── backend/
│   ├── routes/
│   │   ├── text.py
│   │   └── image.py
│   │
│   ├── schemas/
│   │   └── text_input.py
│   │
│   ├── db.py
│   └── moderation.py
│
├── models/
│   ├── text/
│   │   └── inference.py
│   │
│   ├── image/
│   │   ├── inference.py
│   │   ├── nsfw_model.py
│   │   ├── violence_model.py
│   │   └── caption.py
│   │
│   ├── video/
│   │   └── inference.py
│   │
│   └── utils/
│       └── reason_generator.py
│
├── frontend/
│   ├── index.html
│   └── dashboard.html
│
├── uploads/
├── main.py
└── README.md

---

# System Architecture

            User Input
                │
    ┌───────────┼───────────┐
    │           │           │
  Text        Image       Video
    │           │           │
predict_text   analyze_image   analyze_video
    │           │           │
    │     ┌─────┼─────┐     │
    │     │           │     │
    │   NSFW       Violence │
    │     │           │     │
    │     └─────┬─────┘     │
    │           │           │
    │     Caption (BLIP)    │
    │           │           │
    │     Reason Generator  │
    │           │           │
    └───────────┴───────────┘
                │
        Decision Layer
                │
        Risk Calculation
                │
           MongoDB Logs
                │
         API Response

---

# Tech Stack

- **Backend**: FastAPI  
- **AI Models**:
  - Toxic-BERT (text)
  - CLIP (violence detection)
  - NSFW model (image)
  - BLIP (captioning)
- **Database**: MongoDB  
- **Libraries**:
  - Transformers
  - PyTorch
  - OpenCV
  - PIL

---

# Workflow

## Text Flow
1. User sends text  
2. `predict_text()` analyzes toxicity  
3. Rule-based filtering applied  
4. Status determined (allowed / blocked)  
5. Logged in database  

## Image Flow
1. Image uploaded  
2. NSFW + Violence models run  
3. Caption generated  
4. Reason generated  
5. Decision + logging  

## Video Flow
1. Video uploaded  
2. Frames extracted (every 30th frame)  
3. Image model applied  
4. Confidence aggregated  
5. Final decision returned  

---

# Risk Score Logic

- **Blocked Content** → `risk = confidence`  
- **Safe Content** → `risk = 1 - confidence`  

---

# API Endpoints

## Text
POST /chat

## Image
POST /upload-image

## Video
POST /upload-video

## Logs
GET /logs

## Export Report
GET /export-report

---

# Example Response

{
  "status": "blocked",
  "category": "violence",
  "confidence": 0.82,
  "reason": "Detected harmful content"
}

---

# Setup Instructions

git clone <your-repo-url>  
cd cyber-safety-ai-moderation  
pip install -r requirements.txt  
uvicorn main:app --reload  

---

# Future Improvements

- Real-time WebSocket moderation  
- Multilingual support  
- Advanced dashboard analytics  
- Model optimization for speed  

---

# Summary

This project demonstrates a **multi-modal AI moderation system** combining NLP, computer vision, and explainable AI to ensure safer digital platforms.
