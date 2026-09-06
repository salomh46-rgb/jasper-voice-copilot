import os
import io
import base64
import sqlite3
import asyncio
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import edge_tts

from server.command_engine import JasperVoiceCommandEngine
from server.system_actions import SystemActionExecutor

app = FastAPI(
    title="Jasper AI — Live Voice Copilot Desktop & Web Engine",
    version="2.0.0",
    description="Live Uzbek Voice-Controlled Desktop Assistant with Neural Human-like Speech and Zero-Click Continuous Listening."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = JasperVoiceCommandEngine()
executor = SystemActionExecutor()
DB_FILE = os.path.join(os.path.dirname(__file__), "copilot_history.db")
CLIENT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "client")

DEFAULT_VOICE = "uz-UZ-SardorNeural"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS voice_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voice_text TEXT,
            intent TEXT,
            action TEXT,
            speech_response TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

async def generate_neural_tts_bytes(text: str, voice: str = DEFAULT_VOICE) -> bytes:
    try:
        communicate = edge_tts.Communicate(text, voice)
        chunks = []
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                chunks.append(chunk["data"])
        return b"".join(chunks)
    except Exception as e:
        print(f"TTS generation error: {e}")
        return b""

class VoiceInputRequest(BaseModel):
    text: str
    language: Optional[str] = "uz-UZ"
    voice: Optional[str] = DEFAULT_VOICE

@app.get("/")
def serve_index():
    index_path = os.path.join(CLIENT_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "status": "active",
        "service": "Jasper AI — Live Voice Copilot 2.0"
    }

@app.post("/api/voice/process")
async def process_voice_command(req: VoiceInputRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Voice text is empty")

    res = engine.parse_and_execute(req.text)
    speech_text = res["speech_response"]
    
    # Generate ultra-realistic neural human speech
    voice_name = req.voice or DEFAULT_VOICE
    audio_bytes = await generate_neural_tts_bytes(speech_text, voice_name)
    audio_base64 = base64.b64encode(audio_bytes).decode("utf-8") if audio_bytes else ""

    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO voice_logs (voice_text, intent, action, speech_response, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (req.text, res["intent"], res["action"], speech_text, datetime.now(timezone.utc).isoformat()))
        conn.commit()
        conn.close()
    except Exception:
        pass

    return {
        "success": True,
        "input_text": req.text,
        "intent": res["intent"],
        "action": res["action"],
        "speech_response": speech_text,
        "audio_base64": audio_base64,
        "voice_used": voice_name,
        "details": res["details"]
    }

@app.get("/api/voice/tts")
async def get_tts_stream(text: str = Query(..., min_length=1), voice: str = Query(DEFAULT_VOICE)):
    audio_bytes = await generate_neural_tts_bytes(text, voice)
    if not audio_bytes:
        raise HTTPException(status_code=500, detail="Could not generate TTS audio")
    return StreamingResponse(io.BytesIO(audio_bytes), media_type="audio/mpeg")

@app.get("/api/system/status")
def get_system_status():
    disks = executor.get_disk_stats()
    projects = executor.list_projects()
    return {
        "status": "ONLINE 🟢",
        "disks": disks,
        "total_projects": len(projects),
        "projects_sample": projects[:6]
    }

@app.get("/api/projects")
def get_all_projects():
    projects = executor.list_projects()
    return {"total": len(projects), "projects": projects}

@app.get("/api/history")
def get_history(limit: int = 30):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, voice_text, intent, action, speech_response, created_at FROM voice_logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()

    history = []
    for r in rows:
        history.append({
            "id": r[0],
            "voice_text": r[1],
            "intent": r[2],
            "action": r[3],
            "speech_response": r[4],
            "created_at": r[5]
        })
    return {"total": len(history), "logs": history}
