# seed_db.py
# ONE-TIME SCRIPT — run this once to load all data into Firestore
# DO NOT run this multiple times or you will get duplicates

import os
import sys
import json
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

CREDENTIALS_PATH = os.getenv(
    "FIREBASE_CREDENTIALS_PATH",
    "./ophia-data/credentials/firebase-adminsdk.json"
)

# Resolve the path relative to this script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(script_dir, '..', CREDENTIALS_PATH.replace('./', ''))


def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    return firestore.client()


def clear_collection(db, collection_name: str):
    """
    Deletes all documents in a collection before re-seeding.
    This prevents duplicates if you accidentally run this twice.
    """
    print(f"[seed_db] Clearing existing '{collection_name}' collection...")
    docs = db.collection(collection_name).stream()
    count = 0
    for doc in docs:
        doc.reference.delete()
        count += 1
    print(f"[seed_db] Deleted {count} existing documents from '{collection_name}'")


def seed_mentors(db):
    """
    Loads mentors.json and pushes to Firestore.
    """
    mentors_path = os.path.join(script_dir, 'data', 'mentors.json')

    print(f"[seed_db] Loading mentors from: {mentors_path}")

    with open(mentors_path, 'r') as f:
        mentors = json.load(f)

    clear_collection(db, "mentors")

    # Use Firestore batch writes for efficiency
    batch = db.batch()
    count = 0

    for mentor in mentors:
        # Create a document ID from the mentor's name
        doc_id = mentor["name"].lower().replace(" ", "_").replace(".", "")
        doc_ref = db.collection("mentors").document(doc_id)
        batch.set(doc_ref, mentor)
        count += 1
        print(f"  [seed_db] Queued mentor: {mentor['name']}")

        # Firestore batch limit is 500 — commit every 400 to be safe
        if count % 400 == 0:
            batch.commit()
            batch = db.batch()

    batch.commit()
    print(f"[seed_db] ✅ Seeded {count} mentors into Firestore")


def seed_startups(db, csv_path: str = None, limit: int = 50):
    """
    Loads the YC CSV and pushes startups to Firestore.
    
    If Isma has already provided embedding-enriched startups.json, use that instead.
    """
    
    # First check if Isma's enriched JSON exists
    enriched_path = os.path.join(script_dir, 'data', 'startups.json')
    
    if os.path.exists(enriched_path) and os.path.getsize(enriched_path) > 10:
        print(f"[seed_db] Found enriched startups.json from Isma — using that")
        with open(enriched_path, 'r') as f:
            startups = json.load(f)
    else:
        # Fall back to loading directly from the YC CSV
        if csv_path is None:
            # Look for the CSV in a few common locations
            possible_paths = [
                os.path.join(script_dir, '..', '2023-07-13-yc-companies.csv'),
                os.path.join(script_dir, '2023-07-13-yc-companies.csv'),
                '2023-07-13-yc-companies.csv'
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    csv_path = path
                    break
        
        if not csv_path or not os.path.exists(csv_path):
            print("[seed_db] ❌ ERROR: Cannot find CSV file. Put it in the repo root.")
            print("[seed_db] Seeding with sample startup data instead...")
            startups = get_sample_startups()
        else:
            print(f"[seed_db] Loading CSV from: {csv_path}")
            startups = load_startups_from_csv(csv_path, limit)

    clear_collection(db, "startups")

    batch = db.batch()
    count = 0

    for startup in startups:
        doc_id = startup.get("company_name", f"startup_{count}").lower()
        doc_id = doc_id.replace(" ", "_").replace("/", "_")[:50]
        doc_ref = db.collection("startups").document(doc_id)
        batch.set(doc_ref, startup)
        count += 1
        print(f"  [seed_db] Queued startup: {startup.get('company_name', 'Unknown')}")

        if count % 400 == 0:
            batch.commit()
            batch = db.batch()

    batch.commit()
    print(f"[seed_db] ✅ Seeded {count} startups into Firestore")


def load_startups_from_csv(csv_path: str, limit: int = 50) -> list:
    """
    Reads the YC CSV and converts rows into the startup schema format.
    """
    df = pd.read_csv(csv_path)
    
    print(f"[seed_db] CSV columns: {list(df.columns)}")
    
    df = df.dropna(subset=["company_name"])
    df = df.head(limit)

    startups = []

    for _, row in df.iterrows():
        # Handle different possible column names in the CSV
        description = str(row.get("short_description", row.get("description", "No description available"))).strip()
        tags_raw = str(row.get("tags", row.get("industry", ""))).strip()
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()] if tags_raw else []

        startup = {
            "company_name": str(row.get("company_name", "Unknown")).strip(),
            "description": description,
            "batch": str(row.get("batch", "Unknown")).strip(),
            "status": str(row.get("status", "Active")).strip(),
            "industry_tags": tags,
            "country": str(row.get("country", "Unknown")).strip(),
            "founders": [],
            "website": str(row.get("website", "")).strip() or None,
            "is_active": True,
            "description_embedding": None   # Isma fills this in later
        }
        startups.append(startup)

    return startups


def get_sample_startups() -> list:
    """
    Fallback sample startups if CSV isn't available.
    Matches the mock data already in Anna's UI.
    """
    return [
        {
            "company_name": "DataShield",
            "description": "AI-powered fraud detection and cybersecurity platform for fintech companies.",
            "batch": "W23",
            "status": "Active",
            "industry_tags": ["AI Security", "Fintech", "B2B"],
            "country": "Malaysia",
            "founders": [{"name": "Ahmad Faris", "bio": "Ex-Google security engineer"}],
            "website": None,
            "is_active": True,
            "description_embedding": None
        },
        {
            "company_name": "GreenLedger",
            "description": "ESG compliance and carbon tracking platform for enterprises in Southeast Asia.",
            "batch": "S23",
            "status": "Active",
            "industry_tags": ["ESG", "RegTech", "Climate Tech"],
            "country": "Singapore",
            "founders": [{"name": "Mei Lin Tan", "bio": "Former sustainability consultant"}],
            "website": None,
            "is_active": True,
            "description_embedding": None
        },
        {
            "company_name": "MediCore AI",
            "description": "Clinical ML platform that predicts patient outcomes using electronic health records.",
            "batch": "W23",
            "status": "Active",
            "industry_tags": ["Health AI", "MedTech", "Deep Learning"],
            "country": "Malaysia",
            "founders": [{"name": "Dr. Aisha Rahman", "bio": "Medical doctor turned AI researcher"}],
            "website": None,
            "is_active": True,
            "description_embedding": None
        }
    ]


# ═══════════════════════════════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("OPHIA — Firestore Database Seeder")
    print("=" * 60)
    print("WARNING: This will clear and re-seed your Firestore collections.")
    confirm = input("Type 'yes' to continue: ").strip().lower()

    if confirm != "yes":
        print("Cancelled.")
        sys.exit(0)

    db = init_firebase()
    print("[seed_db] ✅ Connected to Firestore")

    print("\n--- Seeding Mentors ---")
    seed_mentors(db)

    print("\n--- Seeding Startups ---")
    seed_startups(db, limit=30)

    print("\n" + "=" * 60)
    print("✅ Database seeded successfully!")
    print("Check your Firestore console to verify the data.")
    print("=" * 60)