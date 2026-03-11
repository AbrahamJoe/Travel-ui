import os
import streamlit as st
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Voyager — AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_BASE_URL = os.getenv("API_BASE_URL")

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e4d9;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] > .main { padding: 0 !important; }
[data-testid="stHeader"] { display: none; }
section[data-testid="stSidebar"] { display: none; }
[data-testid="stToolbar"] { display: none; }
footer { display: none; }

/* ── Hero banner ── */
.hero {
    position: relative;
    width: 100%;
    min-height: 340px;
    background:
        linear-gradient(160deg, rgba(10,10,15,0.0) 0%, rgba(10,10,15,0.85) 100%),
        url('https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=1600&q=80') center/cover no-repeat;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 2rem 3rem;
    overflow: hidden;
}

.hero::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 80px;
    background: linear-gradient(to bottom, transparent, #0a0a0f);
}

.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-weight: 400;
    font-size: 0.8rem;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: #c9a96e;
    margin-bottom: 1rem;
    animation: fadeUp 0.6s ease both;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(3rem, 7vw, 5.5rem);
    font-weight: 900;
    color: #f5f0e8;
    text-align: center;
    line-height: 1.05;
    margin: 0;
    animation: fadeUp 0.7s 0.1s ease both;
}

.hero-title span { color: #c9a96e; }

.hero-sub {
    margin-top: 1.2rem;
    font-size: 1.1rem;
    color: #b0a99a;
    font-weight: 300;
    text-align: center;
    animation: fadeUp 0.7s 0.2s ease both;
}

/* ── Status pill ── */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 1rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.02em;
    margin-bottom: 2rem;
    animation: fadeUp 0.7s 0.25s ease both;
}

.status-pill.online {
    background: rgba(74, 179, 120, 0.15);
    border: 1px solid rgba(74, 179, 120, 0.4);
    color: #4ab378;
}

.status-pill.offline {
    background: rgba(220, 80, 80, 0.15);
    border: 1px solid rgba(220, 80, 80, 0.4);
    color: #dc5050;
}

.status-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    animation: pulse 2s infinite;
}

.status-pill.online .status-dot { background: #4ab378; }
.status-pill.offline .status-dot { background: #dc5050; animation: none; }

/* ── Form container ── */
.form-shell {
    max-width: 1000px;
    margin: 0 auto;
    padding: 0 2rem 4rem;
}

.section-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #c9a96e;
    margin-bottom: 1.2rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(201,169,110,0.2);
}

/* ── Streamlit widget overrides ── */
[data-testid="stTextInput"] input,
[data-testid="stDateInput"] input,
[data-testid="stNumberInput"] input {
    background: #14141c !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #e8e4d9 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1rem !important;
    transition: border-color 0.2s ease !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stDateInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: rgba(201,169,110,0.6) !important;
    box-shadow: 0 0 0 3px rgba(201,169,110,0.08) !important;
    outline: none !important;
}

[data-testid="stTextInput"] label,
[data-testid="stDateInput"] label,
[data-testid="stNumberInput"] label {
    color: #9c958a !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.02em !important;
}

/* Number input arrows */
[data-testid="stNumberInput"] button {
    background: #1e1e2a !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #9c958a !important;
}

/* Date input calendar icon */
[data-testid="stDateInput"] svg { fill: #9c958a !important; }

/* ── Generate button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #c9a96e 0%, #a8834a 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #0a0a0f !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    padding: 0.85rem 2rem !important;
    width: 100% !important;
    transition: all 0.25s ease !important;
    cursor: pointer !important;
    box-shadow: 0 4px 20px rgba(201,169,110,0.25) !important;
}

[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(201,169,110,0.35) !important;
}

[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    border: 1px solid rgba(201,169,110,0.5) !important;
    border-radius: 10px !important;
    color: #c9a96e !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}

[data-testid="stDownloadButton"] > button:hover {
    background: rgba(201,169,110,0.08) !important;
    border-color: #c9a96e !important;
}

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.07) !important; }

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: #14141c !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
    padding: 1.2rem 1.5rem !important;
}

[data-testid="stMetricLabel"] { color: #9c958a !important; font-size: 0.78rem !important; }
[data-testid="stMetricValue"] {
    color: #f5f0e8 !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 1.6rem !important;
}

/* ── Expanders (Day cards) ── */
[data-testid="stExpander"] {
    background: #13131b !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
    margin-bottom: 0.6rem !important;
    overflow: hidden !important;
}

[data-testid="stExpander"] summary {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    color: #e8e4d9 !important;
    padding: 1rem 1.2rem !important;
}

[data-testid="stExpander"] summary:hover { background: rgba(255,255,255,0.03) !important; }

[data-testid="stExpanderDetails"] {
    padding: 0.5rem 1.2rem 1.2rem !important;
}

/* ── Info / Alert boxes ── */
[data-testid="stAlert"] {
    background: rgba(201,169,110,0.07) !important;
    border: 1px solid rgba(201,169,110,0.25) !important;
    border-radius: 10px !important;
    color: #c9a96e !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: #c9a96e !important; }

/* ── Error messages ── */
.stAlert[data-baseweb="notification"][kind="error"] {
    background: rgba(220,80,80,0.1) !important;
    border-color: rgba(220,80,80,0.3) !important;
}

/* ── Hotel card ── */
.hotel-card {
    background: #13131b;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.2s ease, transform 0.2s ease;
}
.hotel-card:hover {
    border-color: rgba(201,169,110,0.3);
    transform: translateY(-2px);
}
.hotel-name {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #f5f0e8;
    margin: 0 0 0.5rem;
}
.hotel-meta {
    font-size: 0.82rem;
    color: #9c958a;
    margin: 0 0 0.5rem;
    display: flex;
    gap: 1.2rem;
    flex-wrap: wrap;
}
.hotel-meta span { color: #c9a96e; font-weight: 500; }
.hotel-desc {
    font-size: 0.88rem;
    color: #7a7570;
    margin: 0;
    font-style: italic;
}

/* ── Activity item ── */
.act-row {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    padding: 0.45rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.act-row:last-child { border-bottom: none; }
.act-time {
    font-size: 0.76rem;
    font-weight: 600;
    color: #c9a96e;
    min-width: 45px;
    padding-top: 2px;
    letter-spacing: 0.03em;
}
.act-desc { font-size: 0.88rem; color: #ccc8bf; flex: 1; }
.act-cost {
    font-size: 0.76rem;
    color: #6a6560;
    white-space: nowrap;
    padding-top: 2px;
}

/* ── Slot header ── */
.slot-header {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #5a5450;
    padding: 0.8rem 0 0.4rem;
    margin-top: 0.4rem;
}

/* ── Day note ── */
.day-note {
    background: rgba(201,169,110,0.05);
    border-left: 2px solid rgba(201,169,110,0.4);
    border-radius: 0 8px 8px 0;
    padding: 0.6rem 0.9rem;
    margin-top: 0.8rem;
    font-size: 0.83rem;
    color: #9c958a;
    font-style: italic;
}

/* ── Success banner ── */
.success-banner {
    background: linear-gradient(135deg, rgba(74,179,120,0.1), rgba(74,179,120,0.05));
    border: 1px solid rgba(74,179,120,0.3);
    border-radius: 12px;
    padding: 1rem 1.4rem;
    color: #4ab378;
    font-weight: 500;
    font-size: 0.92rem;
    margin: 1rem 0;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

/* ── Section title ── */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #f5f0e8;
    margin: 2rem 0 0.3rem;
}

/* ── Route badge ── */
.route-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(201,169,110,0.08);
    border: 1px solid rgba(201,169,110,0.2);
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-size: 0.83rem;
    color: #c9a96e;
    margin-bottom: 1.5rem;
}

/* ── Animations ── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2a2a38; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── API health check ────────────────────────────────────────────────────────────
@st.cache_data(ttl=10)
def check_api_health():
    try:
        r = requests.get(f"{API_BASE_URL}/health", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


api_online = check_api_health()

# ── Hero section ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">AI-Powered Travel Planning</div>
    <h1 class="hero-title">Every Journey<br>Begins <span>Here</span></h1>
    <p class="hero-sub">Personalised itineraries, hotel picks & PDF exports — in seconds.</p>
</div>
""", unsafe_allow_html=True)

# API status pill (centred below hero)
_, pill_col, _ = st.columns([2, 1, 2])
with pill_col:
    if api_online:
        st.markdown(
            '<div class="status-pill online" style="margin:1.5rem auto 0;display:flex;justify-content:center;">'
            '<span class="status-dot"></span> API Connected</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="status-pill offline" style="margin:1.5rem auto 0;display:flex;justify-content:center;">'
            '<span class="status-dot"></span> API Offline</div>',
            unsafe_allow_html=True,
        )

st.markdown('<div style="height:2.5rem"></div>', unsafe_allow_html=True)

# ── Form ───────────────────────────────────────────────────────────────────────
with st.container():
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="section-label">Where are you going?</div>', unsafe_allow_html=True)
        start_location = st.text_input(
            "Departure City",
            placeholder="e.g., Mumbai, India",
            label_visibility="visible",
        )
        destination = st.text_input(
            "Destination",
            placeholder="e.g., Tokyo, Japan",
        )

    with right:
        st.markdown('<div class="section-label">When & How Much?</div>', unsafe_allow_html=True)
        today = datetime.now().date()
        d_col1, d_col2 = st.columns(2)
        with d_col1:
            start_date = st.date_input("Departure Date", value=today + timedelta(days=14), min_value=today)
        with d_col2:
            end_date = st.date_input("Return Date", value=today + timedelta(days=21), min_value=today)
        budget = st.number_input(
            "Total Budget (₹ INR)",
            min_value=1000, max_value=10_000_000,
            value=150_000, step=5_000,
        )

st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)

# ── Generate button ────────────────────────────────────────────────────────────
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    generate = st.button("✈️  Generate My Itinerary", use_container_width=True)

# ── Validation & API call ──────────────────────────────────────────────────────
if generate:
    errors = []
    if not start_location.strip():
        errors.append("Departure city is required.")
    if not destination.strip():
        errors.append("Destination is required.")
    if start_date >= end_date:
        errors.append("Return date must be after departure date.")
    if not api_online:
        errors.append("API is offline — please start the backend server.")

    if errors:
        for e in errors:
            st.error(f"⚠️  {e}")
    else:
        payload = {
            "destination":       destination.strip(),
            "startDate":         start_date.strftime("%Y-%m-%d"),
            "endDate":           end_date.strftime("%Y-%m-%d"),
            "budget":            str(int(budget)),
            "startLocationName": start_location.strip(),
        }

        with st.spinner("Crafting your itinerary…  This takes 30–60 seconds."):
            try:
                resp = requests.post(
                    f"{API_BASE_URL}/agent/metadata",
                    json=payload,
                    timeout=300,
                )
            except requests.exceptions.Timeout:
                st.error("⏱️  Request timed out. Please try again.")
                st.stop()
            except requests.exceptions.ConnectionError:
                st.error("🔌  Cannot reach the API. Make sure `main.py` is running.")
                st.stop()
            except Exception as exc:
                st.error(f"Unexpected error: {exc}")
                st.stop()

        if resp.status_code != 200:
            detail = resp.json().get("detail", "Unknown error")
            st.error(f"API error: {detail}")
            st.stop()

        data = resp.json()
        budget_info = data.get("budget", {})
        itinerary   = data.get("itinerary", {})
        hotels      = data.get("hotels", [])
        route_info  = data.get("route_info", {})

        # ── Success banner ──────────────────────────────────────────────────────
        st.markdown(
            '<div class="success-banner">✓ &nbsp; Itinerary generated successfully</div>',
            unsafe_allow_html=True,
        )

        # ── Route badge ─────────────────────────────────────────────────────────
        route = route_info.get("route_result", {})
        dist  = route.get("distance_km")
        hrs   = route.get("travel_time_hours")
        mode  = route.get("transport_mode", "")
        if dist and hrs:
            mode_icon = {"flight": "✈️", "drive": "🚗", "train": "🚆"}.get(mode, "🗺️")
            st.markdown(
                f'<div class="route-badge">{mode_icon} &nbsp;'
                f'{start_location.strip()} → {destination.strip()} &nbsp;·&nbsp; '
                f'~{dist:,.0f} km &nbsp;·&nbsp; ~{hrs:.1f} hrs</div>',
                unsafe_allow_html=True,
            )

        # ── Metrics ─────────────────────────────────────────────────────────────
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Duration", f"{budget_info.get('trip_days', '—')} days")
        with m2:
            curr = budget_info.get("converted_currency", "INR")
            val  = budget_info.get("converted_value", 0) or 0
            st.metric("Total Budget", f"{curr} {val:,.0f}")
        with m3:
            daily = budget_info.get("daily_budget_local", 0) or 0
            st.metric("Daily Budget", f"{curr} {daily:,.0f}")

        st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

        # ── Trip overview ────────────────────────────────────────────────────────
        if itinerary.get("summary"):
            st.markdown(
                f'<div class="day-note" style="border-left-color:#c9a96e;font-style:normal;'
                f'font-size:0.92rem;color:#b0a99a;margin-bottom:1rem;">'
                f'<b style="color:#c9a96e">Overview</b> &nbsp;{itinerary["summary"]}</div>',
                unsafe_allow_html=True,
            )

        # ── Daily itinerary ──────────────────────────────────────────────────────
        st.markdown('<div class="section-title">Day-by-Day Itinerary</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:0.6rem"></div>', unsafe_allow_html=True)

        for idx, day in enumerate(itinerary.get("days", []), 1):
            label = f"📍  Day {idx}  ·  {day.get('date', '')}"
            with st.expander(label, expanded=(idx == 1)):
                for slot_key, slot_icon, slot_name in [
                    ("morning",   "🌅", "MORNING"),
                    ("afternoon", "☀️", "AFTERNOON"),
                    ("evening",   "🌙", "EVENING"),
                ]:
                    acts = day.get(slot_key, [])
                    if acts:
                        st.markdown(f'<div class="slot-header">{slot_icon} {slot_name}</div>', unsafe_allow_html=True)
                        rows_html = ""
                        for act in acts:
                            cost_html = (
                                f'<span class="act-cost">{act.get("estimated_cost_local", "")}</span>'
                                if act.get("estimated_cost_local") else ""
                            )
                            rows_html += (
                                f'<div class="act-row">'
                                f'<span class="act-time">{act.get("time","")}</span>'
                                f'<span class="act-desc">{act.get("activity","")}</span>'
                                f'{cost_html}</div>'
                            )
                        st.markdown(rows_html, unsafe_allow_html=True)

                if day.get("notes"):
                    st.markdown(f'<div class="day-note">💡 {day["notes"]}</div>', unsafe_allow_html=True)

        # ── Hotels ───────────────────────────────────────────────────────────────
        if hotels:
            st.markdown('<div class="section-title">Recommended Hotels</div>', unsafe_allow_html=True)
            st.markdown('<div style="height:0.6rem"></div>', unsafe_allow_html=True)

            h_col1, h_col2 = st.columns(2, gap="medium")
            for i, hotel in enumerate(hotels[:6]):
                col = h_col1 if i % 2 == 0 else h_col2
                with col:
                    price = hotel.get("price_per_night_local", "N/A")
                    rating = hotel.get("rating", "N/A")
                    addr   = hotel.get("address", "")
                    desc   = hotel.get("description", "")
                    st.markdown(f"""
                    <div class="hotel-card">
                        <p class="hotel-name">{hotel.get('name','Hotel')}</p>
                        <div class="hotel-meta">
                            <span>⭐ {rating}</span>
                            <span>💰 {price} / night</span>
                        </div>
                        <p style="font-size:0.8rem;color:#6a6560;margin:0 0 0.4rem">📍 {addr}</p>
                        <p class="hotel-desc">{desc}</p>
                    </div>
                    """, unsafe_allow_html=True)

        # ── PDF download ──────────────────────────────────────────────────────────
        st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Export</div>', unsafe_allow_html=True)

        _, dl_col, _ = st.columns([1, 2, 1])
        with dl_col:
            with st.spinner("Preparing PDF…"):
                try:
                    pdf_resp = requests.post(
                        f"{API_BASE_URL}/agent",
                        json=payload,
                        timeout=300,
                    )
                except Exception:
                    pdf_resp = None

            if pdf_resp and pdf_resp.status_code == 200:
                ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_dst = destination.strip().replace(" ", "_").replace(",", "")
                fname    = f"itinerary_{safe_dst}_{ts}.pdf"
                st.download_button(
                    label="📥  Download PDF Itinerary",
                    data=pdf_resp.content,
                    file_name=fname,
                    mime="application/pdf",
                    use_container_width=True,
                )
            else:
                st.error("PDF generation failed. The metadata above is still available.")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown('<div style="height:3rem"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:2rem;border-top:1px solid rgba(255,255,255,0.06);
     color:#3a3830;font-size:0.78rem;letter-spacing:0.05em;">
    VOYAGER &nbsp;·&nbsp; Powered by Google Gemini &nbsp;·&nbsp; FastAPI &nbsp;·&nbsp; Streamlit
</div>
""", unsafe_allow_html=True)