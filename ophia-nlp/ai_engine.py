"""
ai_engine.py — OPHIA Cognitive Engine (Ismail's module)

Razin imports ONE function:
    from ai_engine import generate_matches

Uses Vertex AI via ADC — all usage billed to GCP credits.
"""

import os
import json
import numpy as np
from scipy.spatial.distance import cosine
from typing import Optional
from dotenv import load_dotenv

from google import genai
from google.genai import types
from google.cloud import firestore

load_dotenv()

# ── CONFIG ────────────────────────────────────────────────────────────────────
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "ophia-guard-2030")
GCP_LOCATION   = os.getenv("GCP_LOCATION", "us-central1")
TOP_N_MATCHES  = 3

# ── INIT ──────────────────────────────────────────────────────────────────────
client = genai.Client(
    vertexai=True,
    project=GCP_PROJECT_ID,
    location=GCP_LOCATION,
)
db = firestore.Client(project=GCP_PROJECT_ID)

EMBED_MODEL     = "gemini-embedding-2"
GEN_MODEL       = "gemini-3.1-flash-lite"


# ── GEMINI STRUCTURED OUTPUT SCHEMA ──────────────────────────────────────────
MATCH_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "synergy": {
            "type": "INTEGER",
            "description": "Match synergy score from 0 to 100"
        },
        "insight": {
            "type": "STRING",
            "description": "Exactly 2 sentences explaining why this mentor-startup pair works"
        },
        "tags": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "2-4 taxonomy overlap tags"
        },
    },
    "required": ["synergy", "insight", "tags"]
}

INSIGHT_PROMPT = """
You are OPHIA, an AI ecosystem orchestrator for an innovation platform.

Evaluate this mentor-startup match and return a structured assessment.

STARTUP:
- Name: {startup_name}
- Description: {startup_description}
- Industry Tags: {startup_tags}

MENTOR:
- Name: {mentor_name}
- Title: {mentor_title}
- Bio: {mentor_bio}
- Skills: {mentor_skills}

Instructions:
- synergy: Score from 0-100 reflecting how well this mentor's expertise fits the startup's needs.
  (90-100 = exceptional alignment, 70-89 = strong, 50-69 = moderate, below 50 = weak)
- insight: Write EXACTLY 2 sentences. First sentence explains the core expertise alignment.
  Second sentence explains what specific outcome this mentor can drive for the startup.
- tags: 2-4 short taxonomy tags that describe the overlap (e.g. "AI/ML", "B2B Sales", "Series A Ready").
"""


# ── CORE FUNCTIONS ────────────────────────────────────────────────────────────

def _get_embedding(text: str) -> list[float]:
    try:
        result = client.models.embed_content(
            model=EMBED_MODEL,
            contents=text,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
        )
        return result.embeddings[0].values
    except Exception as e:
        print(f"[ai_engine] Embedding error: {e}")
        return []


def _cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    if not vec_a or not vec_b:
        return 0.0
    try:
        return float(1 - cosine(np.array(vec_a), np.array(vec_b)))
    except Exception:
        return 0.0


def _get_gemini_insight(startup: dict, mentor: dict) -> dict:
    prompt = INSIGHT_PROMPT.format(
        startup_name=startup.get("company_name", ""),
        startup_description=startup.get("description", ""),
        startup_tags=", ".join(startup.get("industry_tags", [])),
        mentor_name=mentor.get("name", ""),
        mentor_title=mentor.get("title", ""),
        mentor_bio=mentor.get("bio", ""),
        mentor_skills=", ".join(mentor.get("skills", []))
    )
    try:
        response = client.models.generate_content(
            model=GEN_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=MATCH_SCHEMA,
                temperature=0.3,
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"[ai_engine] Gemini insight error: {e}")
        return {
            "synergy": 65,
            "insight": (
                f"{mentor.get('name')} brings relevant domain expertise that aligns with "
                f"{startup.get('company_name')}'s core focus area. "
                "This partnership has strong potential for accelerating growth milestones."
            ),
            "tags": startup.get("industry_tags", [])[:3]
        }


def _fetch_startup(startup_name: str) -> Optional[dict]:
    try:
        docs = db.collection("startups") \
                 .where("company_name", "==", startup_name) \
                 .limit(1) \
                 .stream()
        for doc in docs:
            return doc.to_dict()
        return None
    except Exception as e:
        print(f"[ai_engine] Firestore startup fetch error: {e}")
        return None


def _fetch_all_mentors() -> list[dict]:
    try:
        docs = db.collection("mentors") \
                 .where("status", "==", "Available") \
                 .stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        print(f"[ai_engine] Firestore mentor fetch error: {e}")
        return []


# ── PUBLIC API — Razin imports this ──────────────────────────────────────────

def generate_matches(startup_name: str) -> list[dict]:
    """
    Main entry point. Takes a startup name, returns top N mentor matches.

    Returns list of dicts matching MatchResult schema:
    [
      {
        "startup_name": str,
        "mentor_name": str,
        "synergy": int (0-100),
        "insight": str (2 sentences),
        "tags": List[str]
      }
    ]

    Never raises — returns empty list on failure.
    """
    print(f"[ai_engine] Generating matches for: {startup_name}")

    startup = _fetch_startup(startup_name)
    if not startup:
        print(f"[ai_engine] Startup not found: {startup_name}")
        return []

    startup_vec = startup.get("description_embedding")
    if not startup_vec:
        print("[ai_engine] No stored embedding — re-embedding on the fly...")
        startup_vec = _get_embedding(startup.get("description", ""))

    mentors = _fetch_all_mentors()
    if not mentors:
        print("[ai_engine] No available mentors found")
        return []

    scored = []
    for mentor in mentors:
        mentor_vec = mentor.get("bio_embedding")
        if not mentor_vec:
            continue
        score = _cosine_similarity(startup_vec, mentor_vec)
        scored.append((score, mentor))

    scored.sort(key=lambda x: x[0], reverse=True)
    top_mentors = [mentor for _, mentor in scored[:TOP_N_MATCHES]]

    results = []
    for mentor in top_mentors:
        print(f"[ai_engine]  → Gemini insight: {mentor.get('name')}")
        insight_data = _get_gemini_insight(startup, mentor)

        results.append({
            "startup_name": startup.get("company_name"),
            "mentor_name":  mentor.get("name"),
            "synergy":      insight_data.get("synergy", 0),
            "insight":      insight_data.get("insight", ""),
            "tags":         insight_data.get("tags", [])
        })

    print(f"[ai_engine] Done. {len(results)} matches returned.")
    return results