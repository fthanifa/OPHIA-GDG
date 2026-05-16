"""
embed_data.py — OPHIA Data Pipeline (Hybrid approach)

- Vertex AI (ADC) → embeddings (billed to GCP credits)
- Gemini API key  → mentor generation (free tier)

Run:
  $env:GOOGLE_APPLICATION_CREDENTIALS=""
  python embed_data.py
"""

import os
import json
import ast
import time
import pandas as pd
from google import genai
from google.genai import types

# ── CONFIG ────────────────────────────────────────────────────────────────────
SAMPLE_SIZE     = 50
EMBED_MODEL     = "text-embedding-004"
GEN_MODEL       = "gemini-2.0-flash"
CSV_PATH        = "data/raw/2023-07-13-yc-companies.csv"
OUT_STARTUPS    = "output/startups_embedded.json"
OUT_MENTORS     = "output/mentors_embedded.json"

# ── TWO CLIENTS ───────────────────────────────────────────────────────────────
# Client 1: Vertex AI for embeddings (uses GCP credits via ADC)
embed_client = genai.Client(
    vertexai=True,
    project="ophia-guard-2030",
    location="us-central1",
)

# Client 2: Gemini API for generation (free tier, no credits needed)
gen_client = genai.Client(api_key="AIzaSyClkGrknCtsuBaYmW6CkvhOhBrZActi0Lw")

print("✅ Initialized: Vertex AI (embeddings) + Gemini API (generation)")


# ── STEP 1: LOAD & CLEAN STARTUP CSV ─────────────────────────────────────────
def load_startups(csv_path: str, n: int = SAMPLE_SIZE) -> list[dict]:
    print(f"\n📂 Loading CSV from: {csv_path}")
    df = pd.read_csv(csv_path)

    df = df[
        (df["status"] == "Active") &
        (df["short_description"].notna()) &
        (df["country"].notna())
    ].copy()

    df = df.sample(n=min(n, len(df)), random_state=42).reset_index(drop=True)

    startups = []
    for _, row in df.iterrows():
        try:
            tags = ast.literal_eval(row["tags"]) if pd.notna(row["tags"]) else []
        except Exception:
            tags = []

        try:
            founder_names = ast.literal_eval(row["founders_names"]) if pd.notna(row["founders_names"]) else []
        except Exception:
            founder_names = []

        founders = [{"name": name, "bio": None, "linkedin": None, "twitter": None}
                    for name in founder_names]

        startup = {
            "company_name": str(row["company_name"]),
            "description": str(row["short_description"]),
            "batch": str(row["batch"]) if pd.notna(row["batch"]) else "Unknown",
            "status": str(row["status"]),
            "industry_tags": tags[:5],
            "country": str(row["country"]),
            "founders": founders,
            "website": str(row["website"]) if pd.notna(row["website"]) else None,
            "is_active": True,
            "description_embedding": None
        }
        startups.append(startup)

    print(f"✅ Loaded {len(startups)} startups")
    return startups


# ── STEP 2: GENERATE MENTOR VIA GEMINI API (free tier) ───────────────────────
MENTOR_GEN_PROMPT = """
You are generating a realistic mentor profile for an innovation ecosystem platform.

Given this startup:
- Name: {company_name}
- Description: {description}
- Industry Tags: {tags}
- Country: {country}

Generate ONE mentor who would be an excellent match. The mentor should have:
- Complementary industry expertise (not identical, but relevant)
- Real-sounding name and title
- A compelling 2-sentence bio mentioning their background and what they offer startups
- 3-5 specific skills relevant to this startup's stage and domain
- Availability of 4-10 hours per month

Respond ONLY with a valid JSON object with these exact keys:
{{
  "name": "string",
  "title": "string",
  "bio": "string (2 sentences)",
  "industry_tags": ["list", "of", "strings"],
  "skills": ["list", "of", "strings"],
  "availability_hours": integer,
  "linkedin": null,
  "status": "Available",
  "partnerships": 0,
  "bio_embedding": null
}}
Do not include any text outside the JSON object.
"""


def generate_mentor(startup: dict) -> dict:
    prompt = MENTOR_GEN_PROMPT.format(
        company_name=startup["company_name"],
        description=startup["description"],
        tags=", ".join(startup["industry_tags"]),
        country=startup["country"]
    )
    try:
        response = gen_client.models.generate_content(
            model=GEN_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.7,
            )
        )
        return json.loads(response.text.strip())
    except Exception as e:
        print(f"  ⚠️  Mentor gen failed for {startup['company_name']}: {e}")
        return {
            "name": "Alex Morgan",
            "title": "Senior Venture Advisor",
            "bio": "Former operator with 15 years across B2B SaaS and deep tech. Helps early-stage founders with go-to-market strategy and fundraising.",
            "industry_tags": startup["industry_tags"][:3],
            "skills": ["GTM Strategy", "Fundraising", "Product Market Fit"],
            "availability_hours": 6,
            "linkedin": None,
            "status": "Available",
            "partnerships": 0,
            "bio_embedding": None
        }


# ── STEP 3: EMBED TEXT VIA VERTEX AI (GCP credits) ──────────────────────────
def get_embedding(text: str) -> list[float]:
    try:
        result = embed_client.models.embed_content(
            model=EMBED_MODEL,
            contents=text,
        )
        return result.embeddings[0].values
    except Exception as e:
        print(f"  ⚠️  Embedding failed: {e}")
        return []


# ── MAIN PIPELINE ─────────────────────────────────────────────────────────────
def run_pipeline():
    os.makedirs("output", exist_ok=True)

    startups = load_startups(CSV_PATH)
    mentors = []

    print(f"\n🤖 Generating mentors + embeddings for {len(startups)} startups...")
    print("   (~3-5 minutes total, free tier = 15 req/min)\n")

    for i, startup in enumerate(startups):
        print(f"  [{i+1}/{len(startups)}] {startup['company_name']}")

        # Generation via Gemini API (free tier)
        mentor = generate_mentor(startup)
        mentors.append(mentor)

        # Embeddings via Vertex AI (GCP credits)
        print(f"    → Embedding startup description...")
        startup["description_embedding"] = get_embedding(startup["description"])

        print(f"    → Embedding mentor bio...")
        mentor["bio_embedding"] = get_embedding(mentor["bio"])

        # Rate limit: free tier = 15 req/min, so ~4 sec between iterations
        time.sleep(4)

    with open(OUT_STARTUPS, "w") as f:
        json.dump(startups, f, indent=2)
    print(f"\n✅ Saved: {OUT_STARTUPS}")

    with open(OUT_MENTORS, "w") as f:
        json.dump(mentors, f, indent=2)
    print(f"✅ Saved: {OUT_MENTORS}")

    print(f"\n🎉 Pipeline complete! Hand both JSON files to Fitri.")
    print(f"   Startups: {len(startups)} | Mentors: {len(mentors)}")


if __name__ == "__main__":
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(
            f"CSV not found at: {CSV_PATH}\n"
            f"Make sure the YC CSV is at ophia-nlp/data/raw/2023-07-13-yc-companies.csv"
        )
    run_pipeline()
