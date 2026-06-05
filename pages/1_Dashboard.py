import streamlit as st
import os
import sys
import pandas as pd

# Path configurations
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.logic import Queue

# Resolve logo and CSS paths
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo.png")
CSS_PATH = os.path.join(BASE_DIR, "styles", "style.css")

# =====================
# PAGE CONFIG & CSS
# =====================
st.set_page_config(
    page_title="Dashboard - Drone Delivery",
    page_icon="⋮",
    layout="wide"
)

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
    
    st.markdown("---")
    st.markdown("### Status Sistem")
    st.success("🟢 Online & Siap")

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
# METRICS COMPUTATION
# =====================
total_antrean = len(st.session_state.queue.get_all())
total_terkirim = len(st.session_state.history)

ready_drones = sum(1 for d in st.session_state.drones if d["status"] == "Ready")
avg_battery = int(sum(d["battery"] for d in st.session_state.drones) / len(st.session_state.drones))

# =====================
# RENDER METRICS
# =====================
st.markdown("## 📊 Dashboard Pemantauan")
st.markdown("---")

st.markdown(f"""
<div class="cards-grid">
    <div class="stat-card">
        <div class="stat-title">Paket Antrean</div>
        <div class="stat-value">{total_antrean}</div>
        <div style="margin-top: 10px; font-size: 0.85rem; color: #94a3b8;">Menunggu penugasan drone</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">Paket Terkirim</div>
        <div class="stat-value" style="color: #10b981;">{total_terkirim}</div>
        <div style="margin-top: 10px; font-size: 0.85rem; color: #94a3b8;">Sukses diantar ke tujuan</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">Drone Siap</div>
        <div class="stat-value" style="color: #00f2fe;">{ready_drones} / {len(st.session_state.drones)}</div>
        <div style="margin-top: 10px; font-size: 0.85rem; color: #94a3b8;">Status operasional standby</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">Rata-rata Baterai</div>
        <div class="stat-value" style="color: #9d4edd;">{avg_battery}%</div>
        <div style="margin-top: 10px; font-size: 0.85rem; color: #94a3b8;">Daya baterai armada saat ini</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================
# CHARTS & DETAILED STATS
# =====================
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📈 Statistik Pengiriman per Destinasi")
    if st.session_state.history:
        # Generate chart from history data
        dest_counts = {}
        for item in st.session_state.history:
            dest = item.get("tujuan", "Unknown")
            dest_counts[dest] = dest_counts.get(dest, 0) + 1
            
        chart_data = pd.DataFrame(list(dest_counts.items()), columns=["Destinasi", "Jumlah Paket"])
        st.bar_chart(chart_data.set_index("Destinasi"), use_container_width=True)
    else:
        st.info("ℹ️ Belum ada pengiriman untuk dianalisis. Kirim beberapa paket terlebih dahulu.")

with col2:
    st.markdown("### 🚁 Status Detail Armada Drone")
    
    drones_df = pd.DataFrame(st.session_state.drones)
    # Rename columns for prettier table
    drones_df.columns = ["ID Drone", "Status", "Baterai (%)", "Kec. Maks (km/h)", "Beban Maks (kg)", "Pekerjaan Saat Ini"]
    
    st.dataframe(
        drones_df,
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")
# Quick tips
st.markdown("""
<div style="background: rgba(157, 78, 221, 0.05); border: 1px solid rgba(157, 78, 221, 0.2); border-radius: 10px; padding: 15px;">
    <h5 style="color: #9d4edd; margin-top: 0; margin-bottom: 5px;">💡 Tips Operasional:</h5>
    <ul style="color: #94a3b8; font-size: 0.9rem; margin: 0; padding-left: 20px;">
        <li>Gunakan menu <b>Tambah Paket</b> untuk mendaftarkan paket baru ke antrean sistem.</li>
        <li>Buka menu <b>Antrean Drone</b> untuk menugaskan drone dan menerbangkannya ke lokasi.</li>
        <li>Lihat status dan riwayat pengiriman di menu <b>Riwayat</b>.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
