import streamlit as st
import os
import sys

# Ensure local imports work correctly regardless of how the app is started
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.logic import Queue

# =====================
# PATH RESOLUTION
# =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Resolve logo and CSS paths
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo.png")
DRONE_PATH = os.path.join(BASE_DIR, "assets", "drone.png")
CSS_PATH = os.path.join(BASE_DIR, "styles", "style.css")

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="Drone AutoPilot Delivery",
    page_icon="⋮",
    layout="wide",
    initial_sidebar_state="expanded"   
)


# =====================
# SESSION STATE INIT
# =====================
if "queue" not in st.session_state:
    st.session_state.queue = Queue()

if "history" not in st.session_state:
    st.session_state.history = []

if "drones" not in st.session_state:
    st.session_state.drones = [
        {"id": "DRN-01", "status": "Ready", "battery": 95, "speed": 60, "payload": 5, "current_job": None},
        {"id": "DRN-02", "status": "Ready", "battery": 88, "speed": 55, "payload": 5, "current_job": None},
        {"id": "DRN-03", "status": "Ready", "battery": 100, "speed": 65, "payload": 8, "current_job": None}
    ]

# =====================
# LOAD STYLES
# =====================
if os.path.exists(CSS_PATH):
    with open(CSS_PATH, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# =====================
# SIDEBAR
# =====================
with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=150)
    else:
        st.title("🚁 Drone Delivery")
    
    st.markdown('<style>,footer,header{visibility: hidden}</style>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Status Sistem")
    st.success("🟢 Online & Siap")
    
    total_antrean = len(st.session_state.queue.get_all())
    total_terkirim = len(st.session_state.history)
    
    st.metric(label="Total Antrean", value=total_antrean)
    st.metric(label="Paket Terkirim", value=total_terkirim)
    
    st.markdown("---")
    st.caption("© 2026 Drone AutoPilot. All rights reserved.")

# =====================
# MAIN LANDING PAGE
# =====================
# Features and Drone Image Section
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### Fitur Utama Sistem")
    
    # Feature 1
    st.markdown("""
    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 20px; margin-bottom: 15px;">
        <h4 style="color: #00f2fe; margin-top: 0;">🚀 Antrean Cerdas (FIFO Queue)</h4>
        <p style="color: #94a3b8; margin: 0; font-size: 0.95rem;">
            Menggunakan struktur data Queue (Linked List) untuk memproses paket secara berurutan sesuai kedatangan, menjamin keadilan pelayanan.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature 2
    st.markdown("""
    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 20px; margin-bottom: 15px;">
        <h4 style="color: #9d4edd; margin-top: 0;">🗺️ Navigasi Realtime</h4>
        <p style="color: #94a3b8; margin: 0; font-size: 0.95rem;">
            Pemetaan koordinat destinasi dan visualisasi lintasan terbang drone dari pangkalan ke lokasi penerima paket secara dinamis.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature 3
    st.markdown("""
    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 20px;">
        <h4 style="color: #10b981; margin-top: 0;">📊 Analitik & Riwayat</h4>
        <p style="color: #94a3b8; margin: 0; font-size: 0.95rem;">
            Pantau statistik performa pengiriman, efisiensi waktu, serta riwayat data paket yang telah sukses dikirim ke tujuan.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if os.path.exists(DRONE_PATH):
        st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
        st.image(DRONE_PATH, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Gambar drone dapat diletakkan di assets/drone.png")

# Active Drones Grid
st.markdown("### Armada Drone Aktif")
drones = st.session_state.drones
drone_cols = st.columns(len(drones))

for i, drone in enumerate(drones):
    with drone_cols[i]:
        battery_color = "#10b981" if drone["battery"] > 50 else ("#f59e0b" if drone["battery"] > 20 else "#ef4444")
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-title">{drone["id"]}</div>
            <div class="stat-value" style="font-size: 1.8rem; margin: 10px 0;">{drone["status"]}</div>
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #94a3b8; margin-top: 15px;">
                <span>Baterai: <b style="color: {battery_color};">{drone["battery"]}%</b></span>
                <span>Kapasitas: <b>{drone["payload"]} kg</b></span>
            </div>
            <div style="width: 100%; background-color: rgba(255,255,255,0.1); height: 6px; border-radius: 3px; margin-top: 8px; overflow: hidden;">
                <div style="background-color: {battery_color}; width: {drone["battery"]}%; height: 100%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Getting Started Call to Action
st.markdown("---")
st.markdown(
    "<div style='text-align: center; margin-top: 10px; color: #94a3b8;'>Silakan pilih menu di sidebar sebelah kiri untuk mulai mengelola pengiriman paket.</div>", 
    unsafe_allow_html=True
)
