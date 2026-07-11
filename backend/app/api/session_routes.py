from fastapi import APIRouter, File, UploadFile, Form, HTTPException
import shutil
import os
import json

from app.audio.transcribe import transcribe_audio
from app.audio.features import extract_delivery_metrics
from app.evaluation.content_score import evaluate_content
from app.database import save_session, get_all_sessions
from app.analytics import calculate_analytics

router = APIRouter()

@router.get("/sessions")
async def get_sessions():
    """Retrieves all interview sessions and analytics."""
    try:
        sessions = get_all_sessions()
        # Need to parse the JSON strings back into objects
        for s in sessions:
            s["scores"] = json.loads(s["scores_json"])
            s["metrics"] = json.loads(s["metrics_json"])
        
        analytics = calculate_analytics(sessions)
        
        return {
            "sessions": sessions,
            "analytics": analytics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving sessions: {str(e)}")

@router.post("/session/demo/answer")
async def process_answer(
    question: str = Form(...),
    audio: UploadFile = File(...)
):
    """
    The main endpoint for processing interview answers.
    """
    temp_dir = "temp_audio"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, audio.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
        
        # ML Pipeline with error handling
        try:
            transcript = transcribe_audio(file_path)
            delivery_metrics = extract_delivery_metrics(file_path, transcript)
            content_score = evaluate_content(question, transcript)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"ML Pipeline error: {str(e)}")
        
        save_session(question, transcript, content_score, delivery_metrics)
        
        return {
            "transcript": transcript,
            "delivery": delivery_metrics,
            "content": content_score
        }
        
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
