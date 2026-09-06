import os
import sqlite3
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from server.command_engine import JasperVoiceCommandEngine
from server.system_actions import SystemActionExecutor

app = FastAPI(
    title="Jasper AI — Live Voice Copilot Desktop & Web Engine",
    version="1.0.0",
    description="Live Uzbek Voice-Controlled Desktop Assistant that executes computer commands in real-time."
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

class VoiceInputRequest(BaseModel):
    text: str
    language: Optional[str] = "uz-UZ"

@app.get("/")
def read_root():
    return {
        "status": "active",
        "service": "Jasper AI — Live Voice Copilot",
        "version": "1.0.0",
        "developer": "Javohirbek Asqarov (Jasper)",
        "mode": "ELEVATED_ADMIN_VOICE_COPILOT"
    }

@app.post("/api/voice/process")
def process_voice_command(req: VoiceInputRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Voice text is empty")

    res = engine.parse_and_execute(req.text)

    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO voice_logs (voice_text, intent, action, speech_response, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (req.text, res["intent"], res["action"], res["speech_response"], datetime.now(timezone.utc).isoformat()))
        conn.commit()
        conn.close()
    except Exception:
        pass

    return {
        "success": True,
        "input_text": req.text,
        "intent": res["intent"],
        "action": res["action"],
        "speech_response": res["speech_response"],
        "details": res["details"]
    }

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
