import streamlit as st

st.set_page_config(page_title="OPHIA - Cradle Orchestrator", layout="wide")

# ── SESSION STATE ─────────────────────────────────────────────────────────────
for key in ["chk_match_1", "chk_match_2", "chk_match_3", "approved"]:
    if key not in st.session_state:
        st.session_state[key] = False

# ── MOCK DATA ─────────────────────────────────────────────────────────────────
MATCHES = [
    {
        "key": "chk_match_1",
        "startup": "DataShield",
        "mentor": "Ehtisham Raza",
        "synergy": 96,
        "insight": "NLP taxonomy match for 'Fraud Detection Models' and 'Security Protocols'.",
        "tags": ["'Fraud Detection'", "'AI Architecture'", "'AI Technology'"],
    },
    {
        "key": "chk_match_2",
        "startup": "GreenLedger",
        "mentor": "Leong Lai Fong",
        "synergy": 88,
        "insight": "Domain overlap in ESG compliance frameworks and RegTech automation pipelines.",
        "tags": ["'RegTech'", "'ESG Compliance'", "'Automation'"],
    },
    {
        "key": "chk_match_3",
        "startup": "MediCore AI",
        "mentor": "Weiyuan Liu",
        "synergy": 91,
        "insight": "Shared research background in predictive diagnostics and clinical ML models.",
        "tags": ["'Health AI'", "'ML Diagnostics'", "'Clinical Data'"],
    },
]

WORKSPACES = [
    {"name": "Project Alpha", "status": "In Progress", "active": True},
    {"name": "Project Nexus", "status": "In Progress", "active": True},
]

CHECKINS = [
    {"name": "Ehtisham Raza", "detail": "90-day Check-in — Complete"},
    {"name": "Leong Lai Fong",   "detail": "90-day Check-in — Complete"},
]

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }

.stApp {
    background: radial-gradient(circle at 90% 10%, #f2f4e8 0%, #f8f9f3 55%, #ffffff 100%) !important;
    color: #1c2b24 !important;
}

#MainMenu, footer, header, .stDeployButton { visibility: hidden; display: none; }

.block-container {
    padding: 0 2.5rem 3rem 2.5rem !important;
    max-width: 100% !important;
}

/* ── NAV ── */
.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.1rem 0 0.9rem 0;
    border-bottom: 1px solid rgba(28,43,36,0.1);
    margin-bottom: 0.2rem;
}
.brand {
    font-family: 'Playfair Display', serif;
    font-size: 1.55rem;
    font-weight: 800;
    color: #0b2416;
    letter-spacing: -0.3px;
}
.navlinks { display: flex; gap: 1.8rem; align-items: center; }
.navlinks span { font-size: 0.88rem; color: #5d6e65; cursor: pointer; }
.navlinks .active {
    color: #0b2416;
    font-weight: 700;
    border-bottom: 2px solid #0b2416;
    padding-bottom: 2px;
}
.pill-outline {
    border: 1px solid rgba(11,36,22,0.3);
    border-radius: 50px;
    padding: 5px 14px;
    font-size: 0.8rem;
    font-weight: 500;
    color: #1c2b24;
}
.pill-solid {
    border-radius: 50px;
    padding: 5px 14px;
    font-size: 0.8rem;
    font-weight: 600;
    color: #fff;
    background: #0b2416;
    cursor: pointer;
}

/* ── HERO ── */
.page-eyebrow {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #7a8c82;
    font-weight: 600;
    margin: 1.4rem 0 0.25rem;
}
.page-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.8rem !important;
    font-weight: 700 !important;
    color: #0b2416 !important;
    margin: 0 0 1.5rem !important;
    line-height: 1.1 !important;
}

/* ── METRICS ── */
.metric-box {
    border: 1px solid rgba(11,36,22,0.18);
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    background: rgba(255,255,255,0.7);
    display: flex;
    align-items: center;
    gap: 1rem;
    backdrop-filter: blur(4px);
    transition: border-color 0.2s, box-shadow 0.2s;
}
.metric-box:hover {
    border-color: rgba(46,204,113,0.5);
    box-shadow: 0 4px 20px rgba(46,204,113,0.08);
}
.metric-icon-wrap {
    width: 44px; height: 44px;
    background: #eef4ef;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem; flex-shrink: 0;
}
.metric-num { font-size: 1.9rem; font-weight: 700; color: #0b2416; line-height: 1; }
.metric-lbl { font-size: 0.78rem; color: #5d6e65; margin-top: 3px; }

/* ── SECTION ── */
.section-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.55rem !important;
    font-weight: 700 !important;
    color: #0b2416 !important;
    margin: 0 !important;
    padding-top: 4px !important;
}

/* ── APPROVE BUTTON ── */
div.stButton > button {
    background: #ffffff !important;
    color: #0b2416 !important;
    border: 1.5px solid #2ecc71 !important;
    border-radius: 50px !important;
    padding: 0.6rem 1.6rem !important;
    font-weight: 600 !important;
    font-size: 0.83rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    box-shadow: 0 0 14px rgba(46,204,113,0.22) !important;
    transition: all 0.25s !important;
    white-space: nowrap !important;
    width: 100% !important;
}
div.stButton > button:hover {
    background: #2ecc71 !important;
    color: #ffffff !important;
    box-shadow: 0 0 24px rgba(46,204,113,0.4) !important;
}

/* ── TAGS ── */
.tags-row { display: flex; gap: 0.4rem; flex-wrap: wrap; margin: 0.4rem 0 0.8rem; }
.tag-pill {
    border: 1px solid rgba(28,43,36,0.16);
    border-radius: 50px;
    padding: 2px 11px;
    font-size: 0.71rem;
    color: #43534c;
    background: transparent;
    white-space: nowrap;
}

/* ── MATCH CARDS ── */
.match-card {
    border: 1px solid rgba(11,36,22,0.16);
    border-radius: 16px;
    padding: 1.1rem 1.3rem 0.9rem;
    background: rgba(255,255,255,0.6);
    margin-bottom: 0.9rem;
    backdrop-filter: blur(2px);
    transition: border-color 0.2s, box-shadow 0.2s;
}
.match-card:hover {
    border-color: #2ecc71;
    box-shadow: 0 4px 22px rgba(46,204,113,0.1);
}
.entity-role { font-size: 0.7rem; color: #7a8c82; letter-spacing: 0.3px; }
.entity-name { font-size: 1.05rem; font-weight: 700; color: #0b2416; }
.synergy-circle {
    border: 2px solid #2ecc71;
    border-radius: 50%;
    width: 62px; height: 62px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    font-weight: 700; font-size: 1rem;
    color: #0b2416;
    background: radial-gradient(circle, rgba(46,204,113,0.1) 0%, transparent 70%);
    box-shadow: 0 0 12px rgba(46,204,113,0.18);
    margin: auto;
}
.synergy-sub { font-size: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px; color: #5d6e65; }
.synergy-badge {
    background: #2ecc71;
    color: #0b2416;
    font-weight: 700;
    font-size: 0.75rem;
    padding: 5px 13px;
    border-radius: 50px;
    white-space: nowrap;
}
.insight-text { font-size: 0.8rem; color: #5d6e65; margin: 0.5rem 0; line-height: 1.5; }
.insight-text strong { color: #1c2b24; font-weight: 600; }

/* ── SIDEBAR CARDS ── */
.sb-card {
    border: 1px solid rgba(11,36,22,0.12);
    border-radius: 14px;
    padding: 1rem 1.1rem;
    background: rgba(255,255,255,0.75);
    margin-bottom: 0.75rem;
    backdrop-filter: blur(2px);
}
.sb-section-label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #7a8c82;
    font-weight: 600;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.35rem;
}
.sb-entry-name { font-size: 0.85rem; font-weight: 600; color: #0b2416; }
.sb-entry-sub  { font-size: 0.74rem; color: #7a8c82; }
.sb-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #2ecc71;
    display: inline-block;
    margin-right: 6px;
    box-shadow: 0 0 5px rgba(46,204,113,0.5);
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# TOPBAR
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="topbar">
    <div style="display:flex; align-items:center; gap:2.5rem;">
        <div class="brand">OPHIA</div>
        <div class="navlinks">
            <span class="active">Dashboard</span>
            <span>Mentors</span>
            <span>Contact</span>
        </div>
    </div>
    <div style="display:flex; gap:0.7rem; align-items:center;">
        <div class="pill-outline">Admin: Vaza</div>
        <div style="position:relative; width:34px; height:34px; border:1px solid rgba(28,43,36,0.22);
                    border-radius:50%; display:flex; align-items:center; justify-content:center; cursor:pointer; font-size:0.95rem;">
            🔔
            <span style="position:absolute; top:6px; right:6px; width:6px; height:6px;
                         background:#2ecc71; border-radius:50%; border:1.5px solid #f8f9f3;
                         box-shadow:0 0 5px rgba(46,204,113,0.7);"></span>
        </div>
        <div class="pill-solid">Sign in ▾</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="page-eyebrow">Orchestrator Home</div>', unsafe_allow_html=True)
st.markdown('<h1 class="page-title">Cradle Orchestrator</h1>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# METRICS
# ══════════════════════════════════════════════════════════════════════
m1, m2, m3, spacer = st.columns([3, 3, 3, 0.6])
metrics = [
    (m1, "🚀", "124", "New Startups"),
    (m2, "👥", "45",  "Mentors Available"),
    (m3, "📅", "8",   "Active Programmes"),
]
for col, icon, num, label in metrics:
    with col:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-icon-wrap">{icon}</div>
            <div>
                <div class="metric-num">{num}</div>
                <div class="metric-lbl">{label}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with spacer:
    st.markdown("""
    <div style="display:flex; justify-content:flex-end; align-items:center; height:100%; padding-top:2px;">
        <div style="border:1px solid rgba(11,36,22,0.18); border-radius:10px; padding:8px 10px;
                    cursor:pointer; font-size:1.05rem; background:rgba(255,255,255,0.7);">📊</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# MAIN + SIDEBAR COLUMNS
# ══════════════════════════════════════════════════════════════════════
left_col, right_col = st.columns([7, 3], gap="large")


# ──────────────────────────────────────────────────────────────────────
# LEFT: PENDING AI LINKAGES
# ──────────────────────────────────────────────────────────────────────
with left_col:
    hdr_l, hdr_r = st.columns([5, 5])
    with hdr_l:
        st.markdown('<h2 class="section-title">⚡ Pending AI Linkages</h2>', unsafe_allow_html=True)
    with hdr_r:
        if st.button("Approve Selected & Generate Programmable Entities"):
            selected = [m["startup"] for m in MATCHES if st.session_state.get(m["key"], False)]
            if selected:
                st.session_state.approved = True
            else:
                st.markdown("""
                <div style="
                    background: #fff8e6;
                    border: 1.5px solid #f0a500;
                    border-radius: 14px;
                    padding: 0.85rem 1.3rem;
                    margin: 0.8rem 0 0.5rem 0;
                    display: flex;
                    align-items: center;
                    gap: 0.8rem;
                ">
                    <div style="font-size:1.3rem;">⚠️</div>
                    <div style="font-size:0.85rem; font-weight:600; color:#7a4f00;">
                        Please select at least one match before approving.
                    </div>
                </div>
                """, unsafe_allow_html=True)

    if st.session_state.approved:
        st.markdown("""
        <div style="
            background: #0b2416;
            border: 1.5px solid #2ecc71;
            border-radius: 14px;
            padding: 1rem 1.4rem;
            margin: 0.8rem 0 1rem 0;
            display: flex;
            align-items: center;
            gap: 1rem;
            box-shadow: 0 0 24px rgba(46,204,113,0.2);
        ">
            <div style="font-size:1.6rem;">✅</div>
            <div>
                <div style="font-size:0.95rem; font-weight:700; color:#2ecc71; margin-bottom:2px;">
                    Approved Successfully!
                </div>
                <div style="font-size:0.8rem; color:#a8c4b0;">
                    Programmable entities have been generated and are now active.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:0.78rem; font-weight:600; color:#5d6e65; margin:0.9rem 0 0.4rem;">AI match tags</div>
    <div class="tags-row">
        <span class="tag-pill">'Fraud Detection'</span>
        <span class="tag-pill">'Fraud Detection'</span>
        <span class="tag-pill">'AI Architecture'</span>
        <span class="tag-pill">'AI Architecture'</span>
        <span class="tag-pill">'AI Techniiology'</span>
    </div>
    """, unsafe_allow_html=True)

    for match in MATCHES:
        st.markdown('<div class="match-card">', unsafe_allow_html=True)

        c_chk, c_entity, c_synergy, c_badge = st.columns([0.45, 5.55, 2, 2])

        with c_chk:
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            st.checkbox("Select", key=match["key"], label_visibility="collapsed")

        with c_entity:
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:0.6rem; flex-wrap:wrap; margin-top:5px;">
                <div>
                    <div class="entity-role">Startup:</div>
                    <div class="entity-name">{match['startup']}</div>
                </div>
                <div style="color:#0b2416; font-size:1rem; margin-top:14px; letter-spacing:1px;">————&gt;</div>
                <div>
                    <div class="entity-role">Mentor:</div>
                    <div class="entity-name">{match['mentor']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c_synergy:
            st.markdown(f"""
            <div style="display:flex; justify-content:center; padding-top:3px;">
                <div class="synergy-circle">
                    {match['synergy']}%
                    <div class="synergy-sub">Synergy</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c_badge:
            st.markdown(f"""
            <div style="display:flex; justify-content:flex-end; align-items:center; height:100%; padding-top:5px;">
                <span class="synergy-badge">{match['synergy']}% Synergy</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="insight-text"><strong>AI Insight:</strong> {match['insight']}</div>
        <div class="tags-row">{''.join(f'<span class="tag-pill">{t}</span>' for t in match["tags"])}</div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────
# RIGHT: SIDEBAR — rendered using pure Streamlit widgets, no raw HTML
# ──────────────────────────────────────────────────────────────────────
with right_col:

    st.markdown("""
    <div style="border-left: 1px solid rgba(28,43,36,0.1); padding-left: 1.4rem;">
    """, unsafe_allow_html=True)

    # Title
    st.markdown("""
    <div style="font-family:'Playfair Display',serif; font-size:1.05rem; font-weight:700;
                color:#0b2416; margin-bottom:0.2rem;">⚙️ Active Programmable Entities</div>
    <div style="font-size:0.75rem; color:#7a8c82; margin-bottom:1.2rem;">(Live Tracking)</div>
    """, unsafe_allow_html=True)

    # ── Active Workspaces card ──
    st.markdown("""
    <div class="sb-card">
        <div class="sb-section-label">📁 Active Workspaces</div>
    """, unsafe_allow_html=True)

    for ws in WORKSPACES:
        st.markdown(f"""
        <div style="margin-bottom:0.5rem;">
            <div class="sb-entry-name"><span class="sb-dot"></span>{ws['name']}</div>
            <div class="sb-entry-sub" style="padding-left:13px;">Status: {ws['status']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── 90-day Check-ins card ──
    st.markdown("""
    <div class="sb-card">
        <div class="sb-section-label">✅ Completed 90-day Check-ins</div>
    """, unsafe_allow_html=True)

    for ci in CHECKINS:
        st.markdown(f"""
        <div style="margin-bottom:0.5rem;">
            <div class="sb-entry-name">{ci['name']}</div>
            <div class="sb-entry-sub">{ci['detail']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Sparkline card ──
    st.markdown("""
    <div class="sb-card">
        <div class="sb-section-label">📈 Synergy Trend</div>
        <svg viewBox="0 0 280 52" width="100%" height="52" preserveAspectRatio="none">
            <path d="M0,44 Q25,28 50,36 T100,14 T155,38 T210,18 T280,24"
                  fill="none" stroke="#2ecc71" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M0,44 Q25,28 50,36 T100,14 T155,38 T210,18 T280,24 L280,52 L0,52 Z"
                  fill="rgba(46,204,113,0.07)"/>
            <circle cx="100" cy="14" r="3" fill="#2ecc71"/>
            <circle cx="210" cy="18" r="3" fill="#2ecc71"/>
        </svg>
        <div style="font-size:0.7rem; color:#7a8c82; margin-top:0.3rem;">Match quality improving over time</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Quick stats ──
    st.markdown("""
    <div class="sb-card">
        <div class="sb-section-label">📊 Quick Stats</div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.6rem;">
            <div style="text-align:center; padding:0.5rem; background:rgba(46,204,113,0.06); border-radius:10px;">
                <div style="font-size:1.2rem; font-weight:700; color:#0b2416;">3</div>
                <div style="font-size:0.68rem; color:#7a8c82;">Pending</div>
            </div>
            <div style="text-align:center; padding:0.5rem; background:rgba(46,204,113,0.06); border-radius:10px;">
                <div style="font-size:1.2rem; font-weight:700; color:#0b2416;">91%</div>
                <div style="font-size:0.68rem; color:#7a8c82;">Avg Synergy</div>
            </div>
            <div style="text-align:center; padding:0.5rem; background:rgba(46,204,113,0.06); border-radius:10px;">
                <div style="font-size:1.2rem; font-weight:700; color:#0b2416;">2</div>
                <div style="font-size:0.68rem; color:#7a8c82;">Workspaces</div>
            </div>
            <div style="text-align:center; padding:0.5rem; background:rgba(46,204,113,0.06); border-radius:10px;">
                <div style="font-size:1.2rem; font-weight:700; color:#0b2416;">2</div>
                <div style="font-size:0.68rem; color:#7a8c82;">Check-ins</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
