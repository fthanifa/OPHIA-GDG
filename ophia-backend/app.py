from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import datetime

app = FastAPI(title="OPHIA Core Orchestration Engine")

class ApprovalPayload(BaseModel):
    startup: str
    mentor: str
    synergy: int

@app.get("/api/linkages")
def fetch_pending_linkages():
    """Returns mock data until Fitri's engine.py is ready"""
    return [
        {
            "key": "chk_match_1",
            "startup": "DataShield",
            "mentor": "Dr. A. Rahman",
            "synergy": 96,
            "insight": "NLP taxonomy match for Fraud Detection and AI Architecture.",
            "tags": ["'Fraud Detection'", "'AI Architecture'"]
        },
        {
            "key": "chk_match_2",
            "startup": "PayKraft",
            "mentor": "Ehtisham Raza",
            "synergy": 89,
            "insight": "Strong alignment on fintech infrastructure and payment security.",
            "tags": ["'Fintech'", "'Security Protocols'"]
        }
    ]

@app.post("/api/linkages/approve")
def approve_programmable_entities(payloads: List[ApprovalPayload]):
    """Creates 90-day workspace — will write to Firestore once Razin sets it up"""
    created_workspaces = []

    for item in payloads:
        workspace_id = f"wsp_{int(datetime.datetime.now().timestamp())}_{item.startup.lower()}"
        workspace_data = {
            "workspace_id": workspace_id,
            "workspace_name": f"Project {item.startup} x {item.mentor}",
            "startup_name": item.startup,
            "mentor_name": item.mentor,
            "synergy_score": item.synergy,
            "status": "In Progress",
            "lifecycle_start": datetime.datetime.utcnow().isoformat(),
            "lifecycle_end": (datetime.datetime.utcnow() + datetime.timedelta(days=90)).isoformat(),
            "active": True,
            "milestones": [
                {"day": 30, "objective": "Establish Architectural Objectives & Tech Stack Realignment", "completed": False},
                {"day": 60, "objective": "Mid-term Integrity Inspection & Model Execution Check", "completed": False},
                {"day": 90, "objective": "Final Capability Evaluation & Core Performance Audit", "completed": False}
            ]
        }
        created_workspaces.append(workspace_data["workspace_name"])
        print(f"WORKSPACE CREATED: {workspace_id}")

    return {"message": "Success", "provisioned_entities": created_workspaces}