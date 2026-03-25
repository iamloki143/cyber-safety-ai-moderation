from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import shutil
import os
from datetime import datetime
import csv
import io

from backend.routes import text
from backend.routes import image
from backend.db import moderation_logs

from models.text.inference import predict_text
from models.image.inference import analyze_image
from models.video.inference import analyze_video


# ---------------------------
# CREATE FASTAPI APP
# ---------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)

app.mount("/static", StaticFiles(directory="frontend"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(text.router)
app.include_router(image.router)


# ---------------------------
# HEALTH CHECK
# ---------------------------
@app.get("/health")
def health_check():
    return {"status": "system running"}


# ---------------------------
# PAGES
# ---------------------------
@app.get("/")
def home():
    return FileResponse("frontend/index.html")


@app.get("/dashboard")
def dashboard():
    return FileResponse("frontend/dashboard.html")


# ---------------------------
# GET LOGS
# ---------------------------
@app.get("/logs")
def get_logs():
    logs = list(moderation_logs.find({}, {"_id": 0}))
    return logs


# ---------------------------
# EXPORT CSV
# ---------------------------
@app.get("/export-report")
def export_report():

    logs = list(moderation_logs.find({}, {"_id": 0}))

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Type", "Content", "Category",
        "Status", "Confidence", "Risk",
        "Reason", "Timestamp"
    ])

    for log in logs:
        writer.writerow([
            log.get("type"),
            log.get("content"),
            log.get("category"),
            log.get("status"),
            log.get("confidence"),
            log.get("risk"),
            log.get("reason"),
            log.get("timestamp")
        ])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=moderation_report.csv"
        }
    )


# ---------------------------
# TEXT MODERATION
# ---------------------------
@app.post("/chat")
def chat(message: dict):

    text_msg = message["text"]
    result = predict_text(text_msg)

    confidence = result["confidence"]

    status = "allowed"
    reason = "Safe message"

    if result["category"] == "Bullying":
        status = "blocked"
        reason = "Toxic abusive language detected"

    # 🔥 RISK FIX
    if status == "blocked":
        risk = confidence
    else:
        risk = 1 - confidence

    log = {
        "type": "text",
        "content": text_msg,
        "category": result["category"],
        "confidence": confidence,
        "risk": risk,
        "status": status,
        "reason": reason,
        "timestamp": datetime.utcnow()
    }

    moderation_logs.insert_one(log)

    if status == "blocked":
        return {"reply": "⚠ Message blocked due to abusive language"}

    return {"reply": text_msg}


# ---------------------------
# IMAGE MODERATION
# ---------------------------
@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):

    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        return {"status": "error", "message": "Invalid image format"}

    path = f"uploads/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_image(path)

    confidence = result["confidence"]

    status = "safe"
    if result["status"] == "unsafe":
        status = "blocked"

    # 🔥 RISK FIX
    if status == "blocked":
        risk = confidence
    else:
        risk = 1 - confidence

    reason = result.get("description", "Image moderation result")

    log = {
        "type": "image",
        "content": file.filename,
        "path": f"/uploads/{file.filename}",
        "category": result["category"],
        "confidence": confidence,
        "risk": risk,
        "status": status,
        "reason": reason,
        "timestamp": datetime.utcnow()
    }

    moderation_logs.insert_one(log)

    if status == "blocked":
        return {
            "status": "blocked",
            "reason": reason
        }

    return {
        "status": "safe",
        "image_path": f"/uploads/{file.filename}"
    }


# ---------------------------
# VIDEO MODERATION
# ---------------------------
@app.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):

    if not file.filename.lower().endswith((".mp4", ".mov", ".avi")):
        return {"status": "error", "message": "Invalid video format"}

    path = f"uploads/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_video(path)

    confidence = result["confidence"]

    status = "safe"
    if result["status"] == "unsafe":
        status = "blocked"

    # 🔥 RISK FIX
    if status == "blocked":
        risk = confidence
    else:
        risk = 1 - confidence

    reason = result.get("description", "Video moderation result")

    log = {
        "type": "video",
        "content": file.filename,
        "path": f"/uploads/{file.filename}",
        "category": result["category"],
        "confidence": confidence,
        "risk": risk,
        "status": status,
        "reason": reason,
        "timestamp": datetime.utcnow()
    }

    moderation_logs.insert_one(log)

    if status == "blocked":
        return {
            "status": "blocked",
            "reason": reason
        }

    return {
        "status": "safe",
        "video_path": f"/uploads/{file.filename}"
    }