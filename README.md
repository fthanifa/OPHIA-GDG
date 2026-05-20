# OPHIA
**Ontology-driven Programmable Hub for Innovation Administration**

> *"We aren't a dating app for startups. We are the autonomous operating system for ecosystem administrators."*

Built for **GDG KL Build With AI 2026 KL — MyHack** in response to the Cradle Fund problem statement: *Automating Ecosystem Linkages Instead of Manual Coordination.*

---

## The Problem

Ecosystem administrators manually verify participants, guess mentor matches, send emails one by one, and start from scratch every programme cycle. Nothing is reusable. Nothing is tracked. Nothing improves.

## The Solution

OPHIA is an AI-powered orchestration platform built for programme administrators. It matches startups to mentors using Vertex AI embeddings, explains every match with a Gemini-generated insight, and automates everything after approval — intro email, Drive workspace, Calendar invite — in one click.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI on Cloud Run |
| AI / Embeddings | Vertex AI `text-embedding-004` |
| Language Model | Gemini 1.5 Flash |
| Database | Google Cloud Firestore |
| Automation | Gmail API, Google Drive API, Google Calendar API |

---

## Quick Start

```bash
git clone https://github.com/fthanifa/OPHIA-GDG
cd ophia/ophia-frontend
pip install streamlit
streamlit run app.py
```

No API keys needed for the mock demo. Opens at `localhost:8501`.

---

## Team

| Member | Role |
|---|---|
| Anna | Frontend & UI |
| Fitri | NLP Data Pipeline |
| Ismail | Backend & State Machine |
| Razin | Linkage Scoring & Data |
