"""
VoiceShield-AI — Main Application Server (FastAPI)
AI-Powered Real-Time Detection & Prevention of Voice Cloning Impersonation Attacks (SIH26104)
Organization: AICTE - Cyber Security Cell | Theme: Blockchain & Cybersecurity
"""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .database.db import init_db
from .blockchain.ledger import blockchain
from .api.routes import router as api_router

# Initialize FastAPI App
app = FastAPI(
    title="VoiceShield-AI Core Engine",
    description="Real-Time Detection & Prevention of Voice Cloning Impersonation Attacks with Blockchain Forensics",
    version="2.0.0"
)

# Enable CORS for cross-origin integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup Hook
@app.on_event("startup")
async def startup_event():
    init_db()
    print("[OK] VoiceShield SQLite Database Initialized.")
    print("[OK] Blockchain Forensic Ledger Online (Genesis Verified).")
    print("[OK] AI Voice Cloning Acoustic & Biophysical Detection Engine Ready.")

# Include API and WebSocket Routes
app.include_router(api_router, prefix="/api")
app.include_router(api_router, prefix="")

# Static Files for Uploads and Frontend Dashboard
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")

os.makedirs(FRONTEND_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
