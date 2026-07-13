from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from .database import init_db, log_incident, get_incidents

app = FastAPI(title="Self-Healing Dashboard API")

# Initialize DB on startup
init_db()

# Enable CORS for local testing if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class IncidentPayload(BaseModel):
    app_name: str
    diagnostic: str
    proposed_fix: str
    pr_url: str | None = None
    status: str = "Resolved"

@app.post("/api/incidents")
def create_incident(payload: IncidentPayload):
    log_incident(
        payload.app_name, 
        payload.diagnostic, 
        payload.proposed_fix, 
        payload.pr_url, 
        payload.status
    )
    return {"message": "Incident logged successfully"}

@app.get("/api/incidents")
def fetch_incidents():
    incidents = get_incidents()
    return {"incidents": incidents}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "components": {"database": "ok", "api": "ok"}}

# Serve the frontend statically
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
