# mock_data.py
# All mock data for OPHIA demo
# No real APIs, no real DB — pure demo data

import random
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════════════════════════
# PENDING AI MATCHES (what the AI "computed")
# ═══════════════════════════════════════════════════════════════════════

PENDING_MATCHES = [
    {
        "key": "chk_match_1",
        "startup": "DataShield",
        "startup_desc": "AI-powered fraud detection and cybersecurity for fintech platforms.",
        "startup_batch": "W23",
        "startup_country": "Malaysia",
        "mentor": "Ehtisham Raza",
        "mentor_title": "AI Security Architect & Serial Founder",
        "synergy": 96,
        "insight": "NLP taxonomy match for 'Fraud Detection Models' and 'Security Protocols'. Semantic overlap score of 0.94 on AI Security domain vectors.",
        "tags": ["'Fraud Detection'", "'AI Architecture'", "'AI Technology'"],
        "taxonomy_node": "AI_Security",
        "semantic_score": 0.94,
        "taxonomy_score": 0.91,
    },
    {
        "key": "chk_match_2",
        "startup": "GreenLedger",
        "startup_desc": "ESG compliance and carbon tracking platform for Southeast Asian enterprises.",
        "startup_batch": "S23",
        "startup_country": "Singapore",
        "mentor": "Leong Lai Fong",
        "mentor_title": "RegTech Advisor & Former Bank Negara Regulatory Lead",
        "synergy": 88,
        "insight": "Domain overlap in ESG compliance frameworks and RegTech automation pipelines. Mentor's regulatory background directly addresses startup's compliance gaps.",
        "tags": ["'RegTech'", "'ESG Compliance'", "'Automation'"],
        "taxonomy_node": "Financial_Services",
        "semantic_score": 0.87,
        "taxonomy_score": 0.89,
    },
    {
        "key": "chk_match_3",
        "startup": "MediCore AI",
        "startup_desc": "Clinical ML platform predicting patient outcomes from electronic health records.",
        "startup_batch": "W23",
        "startup_country": "Malaysia",
        "mentor": "Weiyuan Liu",
        "mentor_title": "Health AI Researcher & Investor",
        "synergy": 91,
        "insight": "Shared research background in predictive diagnostics and clinical ML models. Vector embedding similarity of 0.91 on Health AI taxonomy cluster.",
        "tags": ["'Health AI'", "'ML Diagnostics'", "'Clinical Data'"],
        "taxonomy_node": "Health_AI",
        "semantic_score": 0.91,
        "taxonomy_score": 0.88,
    },
    {
        "key": "chk_match_4",
        "startup": "SupplySync",
        "startup_desc": "B2B supply chain automation platform for SMEs in Southeast Asia.",
        "startup_batch": "S22",
        "startup_country": "Malaysia",
        "mentor": "Faiz Hassan",
        "mentor_title": "B2B SaaS Growth Lead",
        "synergy": 83,
        "insight": "Strong alignment on B2B SaaS scaling playbooks. Mentor's ASEAN market expertise maps directly to startup's regional expansion goals.",
        "tags": ["'B2B Enterprise'", "'Automation'", "'Supply Chain'"],
        "taxonomy_node": "B2B_Enterprise",
        "semantic_score": 0.82,
        "taxonomy_score": 0.85,
    },
    {
        "key": "chk_match_5",
        "startup": "LeafGrid",
        "startup_desc": "Clean energy marketplace connecting solar panel owners with grid operators.",
        "startup_batch": "W24",
        "startup_country": "Indonesia",
        "mentor": "Sarah Chen",
        "mentor_title": "Climate Tech Investor",
        "synergy": 79,
        "insight": "Climate taxonomy overlap on renewable energy and carbon market domains. Mentor has directly invested in 3 comparable energy marketplace models.",
        "tags": ["'Climate Tech'", "'Sustainability'", "'ESG'"],
        "taxonomy_node": "Climate_Sustainability",
        "semantic_score": 0.78,
        "taxonomy_score": 0.81,
    },
]


# ═══════════════════════════════════════════════════════════════════════
# INITIAL ACTIVE WORKSPACES (already approved before demo)
# ═══════════════════════════════════════════════════════════════════════

INITIAL_WORKSPACES = [
    {
        "name": "Project Alpha",
        "startup": "NeuralPay",
        "mentor": "Yuda Adi Pratama",
        "status": "In Progress",
        "day": 45,
        "synergy": 89,
        "drive_url": "https://drive.google.com/folders/ophia-neuralpay-alpha",
        "calendar_id": "ophia_cal_alpha_001",
    },
    {
        "name": "Project Nexus",
        "startup": "AgriSense",
        "mentor": "Dr. Poo Kuan Hoong",
        "status": "In Progress",
        "day": 62,
        "synergy": 84,
        "drive_url": "https://drive.google.com/folders/ophia-agrisense-nexus",
        "calendar_id": "ophia_cal_nexus_002",
    },
]

INITIAL_CHECKINS = [
    {"name": "Yuda Adi Pratama", "detail": "90-day Check-in — Complete"},
    {"name": "Dr. Poo Kuan Hoong", "detail": "90-day Check-in — Complete"},
]


# ═══════════════════════════════════════════════════════════════════════
# MENTOR DIRECTORY
# ═══════════════════════════════════════════════════════════════════════

MENTORS = [
    {
        "name": "Ehtisham Raza",
        "title": "AI Security Architect & Serial Founder",
        "expertise": ["Fraud Detection", "AI Architecture", "Security Protocols"],
        "bio": "15 years building AI-powered fraud detection systems for fintech companies across Southeast Asia. Has scaled 3 startups to Series B.",
        "status": "Active",
        "partnerships": 3,
        "availability_hours": 8,
        "country": "Malaysia",
    },
    {
        "name": "Leong Lai Fong",
        "title": "RegTech Advisor & Former Bank Negara Lead",
        "expertise": ["RegTech", "ESG Compliance", "Automation"],
        "bio": "Former regulatory advisor with deep expertise in ESG compliance frameworks and RegTech automation across ASEAN financial markets.",
        "status": "Active",
        "partnerships": 2,
        "availability_hours": 6,
        "country": "Malaysia",
    },
    {
        "name": "Weiyuan Liu",
        "title": "Clinical ML Research Lead",
        "expertise": ["Health AI", "ML Diagnostics", "Clinical Data"],
        "bio": "AI researcher turned investor. Background in predictive diagnostics, clinical machine learning models, and health data infrastructure.",
        "status": "Active",
        "partnerships": 4,
        "availability_hours": 5,
        "country": "Singapore",
    },
    {
        "name": "Faiz Hassan",
        "title": "B2B SaaS Growth Lead",
        "expertise": ["B2B", "SaaS", "Developer Tools", "Cloud Infrastructure"],
        "bio": "Ecosystem builder with deep expertise in B2B SaaS scaling and cloud infrastructure for Southeast Asian markets.",
        "status": "Available",
        "partnerships": 1,
        "availability_hours": 10,
        "country": "Malaysia",
    },
    {
        "name": "Sarah Chen",
        "title": "Climate Tech Investor",
        "expertise": ["Climate Tech", "Sustainability", "ESG", "Green Energy"],
        "bio": "Deep tech investor with expertise in climate tech, sustainability metrics, and green energy startup scaling across ASEAN.",
        "status": "Available",
        "partnerships": 0,
        "availability_hours": 4,
        "country": "Singapore",
    },
    {
        "name": "Vriraj Singh",
        "title": "Senior AI Infrastructure Scientist",
        "expertise": ["Fraud Detection", "AI Architecture", "Security Protocols"],
        "bio": "Senior AI scientist with a track record in building enterprise-grade machine learning infrastructure and adversarial AI systems.",
        "status": "Active",
        "partnerships": 3,
        "availability_hours": 6,
        "country": "India",
    },
    {
        "name": "Saurabh Mishra",
        "title": "RegTech & Compliance Director",
        "expertise": ["RegTech", "ESG Compliance", "Automation", "Policy"],
        "bio": "Director-level compliance expert with regulatory experience across India, Singapore, and Malaysia's central banking frameworks.",
        "status": "Active",
        "partnerships": 2,
        "availability_hours": 8,
        "country": "Singapore",
    },
    {
        "name": "Esther Tan",
        "title": "Health AI Product Strategist",
        "expertise": ["Health AI", "ML Diagnostics", "Clinical Data", "MedTech"],
        "bio": "Product strategist who has launched three clinical AI products into regulated healthcare markets in ASEAN and Australia.",
        "status": "Active",
        "partnerships": 4,
        "availability_hours": 5,
        "country": "Malaysia",
    },
    {
        "name": "Dr. L. Wong",
        "title": "Blockchain & DeFi Architect",
        "expertise": ["DeFi", "Smart Contracts", "Web3 Security", "Blockchain"],
        "bio": "Former academic turned blockchain architect. Advised on DeFi protocol design for 5 fintech startups with combined TVL of $200M.",
        "status": "Available",
        "partnerships": 1,
        "availability_hours": 6,
        "country": "Hong Kong",
    },
    {
        "name": "Dr. Poo Kuan Hoong",
        "title": "Sustainability & ESG Strategist",
        "expertise": ["ESG Reporting", "Carbon Markets", "Sustainability", "Policy"],
        "bio": "ESG strategist with 20 years in sustainability consulting. Helped 12 companies achieve carbon neutrality certification in ASEAN.",
        "status": "Active",
        "partnerships": 2,
        "availability_hours": 7,
        "country": "Malaysia",
    },
    {
        "name": "Hernando Cruz",
        "title": "Cybersecurity & Zero-Trust Architect",
        "expertise": ["Zero-Trust", "Penetration Testing", "Cloud Security"],
        "bio": "Zero-trust architect who has designed security frameworks for 3 unicorn startups. Previously red-teamed for a Fortune 500 financial institution.",
        "status": "Available",
        "partnerships": 0,
        "availability_hours": 8,
        "country": "Philippines",
    },
    {
        "name": "Razif Kamaruddin",
        "title": "ML Infrastructure Lead, ex-Google Brain",
        "expertise": ["AI/ML", "NLP", "LLM Deployment", "Deep Learning"],
        "bio": "CTO background in machine learning infrastructure and LLM deployment at enterprise scale. Previously contributed to Google Brain research teams.",
        "status": "Available",
        "partnerships": 0,
        "availability_hours": 6,
        "country": "Malaysia",
    },
]


# ═══════════════════════════════════════════════════════════════════════
# MOCK WORKSPACE GENERATION
# (Called when approve button is clicked)
# ═══════════════════════════════════════════════════════════════════════

def generate_workspace_entity(startup: str, mentor: str, synergy: int) -> dict:
    """
    Returns a fake workspace entity dict.
    Simulates what the real Firestore + Workspace API would return.
    """
    startup_slug = startup.lower().replace(" ", "-")
    mentor_slug = mentor.split()[0].lower()
    ts = datetime.now().strftime("%Y%m%d%H%M%S")

    workspace_names = ["Project Horizon", "Project Vector", "Project Atlas",
                       "Project Meridian", "Project Zenith", "Project Apex",
                       "Project Catalyst", "Project Summit"]
    name = random.choice(workspace_names)

    return {
        "name": name,
        "startup": startup,
        "mentor": mentor,
        "status": "In Progress",
        "day": 0,
        "synergy": synergy,
        "drive_url": f"https://drive.google.com/folders/ophia-{startup_slug}-{ts}",
        "calendar_id": f"ophia_cal_{mentor_slug}_{ts}",
        "created_at": datetime.now().strftime("%d %b %Y, %H:%M MYT"),
        "lifecycle_end": (datetime.now() + timedelta(days=90)).strftime("%d %b %Y"),
        "email_sent_to": f"team@{startup_slug}.io",
        "milestones": [
            {"day": 30, "label": "Establish goals & align on tech stack", "done": False},
            {"day": 60, "label": "Mid-term audit & course correction", "done": False},
            {"day": 90, "label": "Final evaluation & programme sign-off", "done": False},
        ]
    }


# ═══════════════════════════════════════════════════════════════════════
# MOCK SYNERGY TREND DATA
# ═══════════════════════════════════════════════════════════════════════

SYNERGY_TREND = [72, 74, 71, 78, 80, 82, 85, 83, 88, 91]

# ═══════════════════════════════════════════════════════════════════════
# MOCK AI PIPELINE STEPS
# (Shown during the "approve" animation)
# ═══════════════════════════════════════════════════════════════════════

PIPELINE_STEPS = [
    ("🧠", "Fetching startup profiles from Firestore...", 0.4),
    ("📐", "Running Vertex AI text embeddings...", 0.6),
    ("🔗", "Computing cosine similarity on 768-dimension vectors...", 0.75),
    ("🏷️", "Mapping taxonomy nodes via NLP ontology...", 0.85),
    ("📁", "Provisioning Google Drive workspace folder...", 0.90),
    ("📧", "Dispatching introduction email via Gmail API...", 0.95),
    ("📅", "Generating Google Calendar event + Meet link...", 0.98),
    ("✅", "Programmable entity committed to Firestore.", 1.0),
]