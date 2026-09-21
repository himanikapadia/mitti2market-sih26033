import os
import platform
import subprocess
import time
import pandas as pd
import streamlit as st
from gtts import gTTS

# --- 1. Set Page Title and Layout ---
st.set_page_config(
    page_title="Mitti2Market: Disintermediation Protocol",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 2. Custom CSS Styles ---
st.markdown(
    """
    <style>
    div[data-testid="stMetricValue"] {
        font-size: 1.85rem !important;
        font-weight: 700;
        color: #10B981;
    }
    .nokia-bezel {
        background-color: #2D3748;
        border: 4px solid #1A202C;
        border-radius: 28px;
        padding: 24px;
        color: #FFFFFF;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        max-width: 420px;
        margin: 0 auto;
    }
    .nokia-screen {
        background-color: #718096;
        color: #0F172A;
        font-family: 'Courier New', monospace;
        padding: 16px;
        border-radius: 12px;
        border: 3px inset #4A5568;
        min-height: 140px;
        margin-bottom: 20px;
        font-weight: bold;
    }
    .status-badge-approved {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- 3. Hardware Audio Playback Function ---
def trigger_os_audio(file_path: str):
    """Plays MP3 directly through the computer's sound driver."""
    current_os = platform.system()
    try:
        if current_os == "Windows":
            os.system(f'start "" "{file_path}"')
        elif current_os == "Darwin":  # macOS
            subprocess.Popen(
                ["afplay", file_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        elif current_os == "Linux":
            subprocess.Popen(
                ["xdg-open", file_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
    except Exception as e:
        st.warning(f"Audio playback bypassed: {e}")

# --- 4. Database & Session State Engine ---
def init_data_infrastructure():
    # Mock Surat Farmer Database
    if "farmers_df" not in st.session_state:
        st.session_state.farmers_df = pd.DataFrame(
            [
                {
                    "farmer_id": "FARM-001",
                    "name": "Rameshbhai Patel",
                    "village": "Olpad",
                    "phone": "+91 98250 11221",
                    "lat": 21.3314,
                    "lon": 72.7533,
                    "crop": "Bhinda (Okra)",
                    "capacity_kg": 500,
                    "status": "Available",
                    "verified_kg": 0.0,
                    "payout_70": 0.0,
                    "hold_30": 0.0,
                },
                {
                    "farmer_id": "FARM-002",
                    "name": "Sureshbhai Ahir",
                    "village": "Kamrej",
                    "phone": "+91 98250 33442",
                    "lat": 21.2687,
                    "lon": 72.9599,
                    "crop": "Bhinda (Okra)",
                    "capacity_kg": 300,
                    "status": "Available",
                    "verified_kg": 0.0,
                    "payout_70": 0.0,
                    "hold_30": 0.0,
                },
                {
                    "farmer_id": "FARM-003",
                    "name": "Nareshbhai Vasava",
                    "village": "Bardoli",
                    "phone": "+91 98250 55663",
                    "lat": 21.1189,
                    "lon": 73.1126,
                    "crop": "Tomato",
                    "capacity_kg": 400,
                    "status": "Available",
                    "verified_kg": 0.0,
                    "payout_70": 0.0,
                    "hold_30": 0.0,
                },
                {
                    "farmer_id": "FARM-004",
                    "name": "Dineshbhai Gamit",
                    "village": "Mahuva",
                    "phone": "+91 98250 77884",
                    "lat": 20.9577,
                    "lon": 73.1558,
                    "crop": "Onion",
                    "capacity_kg": 250,
                    "status": "Available",
                    "verified_kg": 0.0,
                    "payout_70": 0.0,
                    "hold_30": 0.0,
                },
            ]
        )

# Global State Keys
    defaults = {
        "buyer_escrow_hold": 0.0,
        "demand_bhinda": 0,
        "demand_tomato": 0,
        "demand_onion": 0,
        "fair_rate_bhinda": 25.0,  # ₹25/kg
        "fair_rate_tomato": 20.0,  # ₹20/kg
        "fair_rate_onion": 22.0,  # ₹22/kg
        "escrow_locked": False,
        "ivr_accepted": False,
        "ivr_triggered": False,
        "surplus_holding_cleared": False,
        "driver_dispatched": False,
        "route_completed": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


# Run the initialization
init_data_infrastructure()

# --- 5. Sidebar Navigation & Global Escrow Status ---
st.sidebar.title("🌱 Mitti2Market Core")
st.sidebar.markdown(
    "**SIH 2026 Problem ID: SIH26033**  \n*Direct Farm-to-Enterprise Supply Architecture*"
)
st.sidebar.markdown("---")

role = st.sidebar.selectbox(
    "Switch Simulation Persona:",
    [
        "🏢 Corporate Buyer Portal",
        "🌾 Rural Farmer IVR Simulator",
        "🚛 Logistics Driver App",
        "📊 System Audit & Reset",
    ],
)

st.sidebar.markdown("---")
st.sidebar.subheader("🔒 Escrow Health Pool")
st.sidebar.metric(
    "Locked Capital", f"₹ {st.session_state.buyer_escrow_hold:,.2f}"
)

if st.session_state.escrow_locked:
    st.sidebar.success("Escrow Smart Contract: ACTIVE")
else:
    st.sidebar.info("Escrow: IDLE (Awaiting Demand)")