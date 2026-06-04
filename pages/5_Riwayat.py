import streamlit as st
import os
import sys
import pandas as pd

# Path configurations
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from logic import Queue

# Resolve logo and CSS paths
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo.png")
CSS_PATH = os.path.join(BASE_DIR, "styles", "style.css")

# =====================
# PAGE CONFIG & CSS
# =====================
st.set_page_config(
    page_title="Riwayat - Drone Delivery",
    page_icon="📜",
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

# =====================
# MAIN CONTENT
# =====================
st.markdown("## 📜 Riwayat Pengiriman")
st.markdown("Daftar lengkap paket yang telah sukses dikirimkan ke lokasi penerima.")
st.markdown("---")


if st.session_state.history:
    # Summary stats
    total_delivered = len(st.session_state.history)
    avg_weight = sum(item.get("berat", 0) for item in st.session_state.history) / total_delivered
    express_pct = (sum(1 for item in st.session_state.history if item.get("priority") == "Express") / total_delivered) * 100
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-title">Total Terkirim</div>
            <div class="stat-value" style="color: #10b981;">{total_delivered} Paket</div>
        </div>
        """, unsafe_allow_html=True)
    with col_stat2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-title">Rata-rata Berat</div>
            <div class="stat-value" style="color: #00f2fe;">{avg_weight:.2f} Kg</div>
        </div>
        """, unsafe_allow_html=True)
    with col_stat3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-title">Rasio Express</div>
            <div class="stat-value" style="color: #9d4edd;">{express_pct:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Filter and Search section
    col_f1, col_f2, col_f3 = st.columns([1.5, 1, 1])
    
    with col_f1:
        search_query = st.text_input("🔍 Cari Penerima / Paket", placeholder="Tulis nama...")
    with col_f2:
        dest_filter = st.selectbox("📍 Filter Destinasi", ["Semua", "Kesambi", "Kejaksan", "Harjamukti", "Sumber", "Palimanan"])
    with col_f3:
        prio_filter = st.selectbox("⚡ Filter Prioritas", ["Semua", "Regular", "Express"])
        
    # Apply filtering
    filtered_history = st.session_state.history
    
    if search_query:
        filtered_history = [
            item for item in filtered_history 
            if search_query.lower() in item.get("penerima", "").lower() 
            or search_query.lower() in item.get("paket", "").lower()
        ]
        
    if dest_filter != "Semua":
        filtered_history = [item for item in filtered_history if item.get("tujuan") == dest_filter]
        
    if prio_filter != "Semua":
        filtered_history = [item for item in filtered_history if item.get("priority") == prio_filter]
        
    st.markdown("---")
    
    # Render table
    if filtered_history:
        # Build dataframe for clean representation
        df = pd.DataFrame(filtered_history)
        # Reorder and rename columns for display
        df.columns = ["Nama Penerima", "Nama Paket", "Tujuan", "Prioritas", "Berat (kg)", "Status"]
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Clear history button
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Hapus Semua Riwayat"):
            st.session_state.history = []
            st.success("Riwayat pengiriman berhasil dibersihkan.")
            st.rerun()
    else:
        st.info("ℹ️ Tidak ada data yang cocok dengan kriteria pencarian/filter.")
else:
    st.info("ℹ️ Belum ada paket terkirim. Kirim paket melalui menu 'Antrean Drone' terlebih dahulu.")
