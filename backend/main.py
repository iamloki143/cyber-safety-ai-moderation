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

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure uploads folder exists
os.makedirs("uploads", exist_ok=True)

# Mount static folders
app.mount("/static", StaticFiles(directory="frontend"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(text.router)
app.include_router(image.router)


# ---------------------------
# HEALTH CHECK
# ---------------------------
@app.get("/health")
def health_check():
    return {"status": "system running"}


# ---------------------------
# CHAT PAGE
# ---------------------------
@app.get("/")
def home():
    return FileResponse("frontend/index.html")


# ---------------------------
# DASHBOARD PAGE
# ---------------------------
@app.get("/dashboard")
def dashboard():
    return FileResponse("frontend/dashboard.html")


# ---------------------------
# GET MODERATION LOGS
# ---------------------------
@app.get("/logs")
def get_logs():

    logs = list(moderation_logs.find({}, {"_id": 0}))

    return logs


# ---------------------------
# SYSTEM STATISTICS
# ---------------------------
@app.get("/stats")
def get_stats():

    total = moderation_logs.count_documents({})

    text_count = moderation_logs.count_documents({"type": "text"})
    image_count = moderation_logs.count_documents({"type": "image"})
    video_count = moderation_logs.count_documents({"type": "video"})

    blocked = moderation_logs.count_documents({"status": "blocked"})

    return {
        "total_logs": total,
        "text_messages": text_count,
        "image_uploads": image_count,
        "video_uploads": video_count,
        "blocked_content": blocked
    }


# ---------------------------
# EXPORT REPORT (CSV)
# ---------------------------
@app.get("/export-report")
def export_report():

    logs = list(moderation_logs.find({}, {"_id": 0}))

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Type",
        "Content",
        "Category",
        "Status",
        "Confidence",
        "Reason",
        "Timestamp"
    ])

    for log in logs:
        writer.writerow([
            log.get("type"),
            log.get("content"),
            log.get("category"),
            log.get("status"),
            log.get("confidence"),
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
# TEXT MESSAGE MODERATION
# ---------------------------
@app.post("/chat")
def chat(message: dict):

    text_msg = message["text"]

    result = predict_text(text_msg)

    status = "allowed"
    reason = "Safe message"

    if result["category"] == "Bullying":
        status = "blocked"
        reason = "Toxic abusive language detected"

    log = {
        "type": "text",
        "content": text_msg,
        "category": result["category"],
        "confidence": result["confidence"],
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

    status = "safe"

    if result["status"] == "unsafe":
        status = "blocked"

    log = {
        "type": "image",
        "content": file.filename,
        "category": result["category"],
        "confidence": result["confidence"],
        "status": status,
        "timestamp": datetime.utcnow()
    }

    moderation_logs.insert_one(log)

    if status == "blocked":
        return {
            "status": "blocked",
            "reason": result["category"]
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

    status = "safe"

    if result["status"] == "unsafe":
        status = "blocked"

    log = {
        "type": "video",
        "content": file.filename,
        "category": result["category"],
        "confidence": result["confidence"],
        "status": status,
        "timestamp": datetime.utcnow()
    }

    moderation_logs.insert_one(log)

    if status == "blocked":
        return {
            "status": "blocked",
            "reason": result["category"]
        }

    return {
        "status": "safe",
        "video_path": f"/uploads/{file.filename}"
    }