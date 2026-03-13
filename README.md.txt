# Cyber Safety AI Moderation System

AI-powered system for detecting cyberbullying, NSFW images, and violent content.

## Features
- Text moderation using Toxic-BERT
- Image moderation using NSFW model
- Violence detection with CLIP
- Video frame analysis
- MongoDB logging
- Dashboard analytics

## Technologies
- FastAPI
- Transformers
- PyTorch
- OpenCV
- MongoDB

## Run the Project

1. Install dependencies
pip install -r requirements.txt

2. Run server
python -m uvicorn backend.main:app --reload