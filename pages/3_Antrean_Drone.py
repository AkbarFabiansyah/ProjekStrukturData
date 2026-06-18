import streamlit as st
import os
import sys
import time
# Path configurations
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.logic import Queue
from backend.drone_service import mark_package_delivered_by_index, process_active_deliveries, dispatch_next

# Resolve logo and CSS paths
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo.png")
CSS_PATH = os.path.join(BASE_DIR, "styles", "style.css")

# =====================
# PAGE CONFIG & CSS
# =====================
st.set_page_config(
    page_title="Antrean Drone - Drone Delivery",
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

if "active_deliveries" not in st.session_state:
    st.session_state.active_deliveries = []

# Ensure active deliveries are processed via backend service (no Streamlit usage in backend)
process_active_deliveries(st.session_state.drones, st.session_state.active_deliveries, st.session_state.history)

# =====================
# MAIN CONTENT
# =====================
st.markdown("## 🚀 Antrean & Pengiriman Drone")
st.markdown("Kelola antrean paket dan tugaskan armada drone untuk melakukan pengiriman autopilot.")
st.markdown("---")

col1, col2 = st.columns([1.5, 1])
with col1:
    header_col1, header_col2 = st.columns([2, 1])
    with header_col1:
        st.markdown("### 📋 Daftar Antrean Paket (FIFO)")
    
    queue_data = st.session_state.queue.get_all()

    with header_col2:
        if queue_data:
            if st.button("🚀 Kirim Paket Terdepan", use_container_width=True):
                # Remove the first item from the queue (FIFO logic)
                removed = mark_package_delivered_by_index(st.session_state.queue, 0, st.session_state.history)
                if removed:
                    st.success(f"Paket '{removed.get('paket')}' diproses dan masuk ke Riwayat.")
                    process_active_deliveries(st.session_state.drones, st.session_state.active_deliveries, st.session_state.history)
                    st.rerun()

    if queue_data:
        st.markdown(f"Terdapat **{len(queue_data)}** paket dalam antrean. Paket paling atas akan diproses terlebih dahulu.")

        for i, item in enumerate(queue_data):
            badge_class = "badge-pending"
            priority_color = "#ef4444" if item.get('priority') == "Express" else "#3b82f6"
            # Render package card without individual buttons
            st.markdown(f"""
            <div class="package-card" style="border-left: 4px solid {priority_color};">
                <div class="package-info">
                    <span class="package-name">#{i+1} {item['paket']}</span>
                    <span class="package-meta">Penerima: <b>{item['penerima']}</b> | Tujuan: <b>{item['tujuan']}</b></span>
                    <span class="package-meta" style="color: #94a3b8;">
                        Berat: {item['berat']} kg | 
                        Prioritas: <span style="color: {priority_color}; font-weight: bold;">{item.get('priority', 'Regular')}</span>
                    </span>
                </div>
                <div>
                    <span class="badge {badge_class}">{item['status']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ Tidak ada paket dalam antrean saat ini. Silakan tambahkan paket di halaman 'Tambah Paket'.")

with col2:
    st.markdown("### ⚙️ Pusat Kontrol Pengiriman")
    
    # Check if there is an available drone
    ready_drones = [d for d in st.session_state.drones if d["status"] == "Ready"]
    
    st.markdown(f"**Drone Siap Operasi:** {len(ready_drones)} drone")
    
    for d in st.session_state.drones:
        status_color = "#10b981" if d["status"] == "Ready" else "#f59e0b"
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: bold; color: #ffffff;">{d['id']}</span>
            <span style="color: {status_color}; font-weight: bold;">{d['status']}</span>
            <span style="font-size: 0.85rem; color: #94a3b8;">🔋 {d['battery']}%</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Instruction: info on processing packages
    st.markdown("---")
    if queue_data:
        st.info("Gunakan tombol '🚀 Kirim Paket Terdepan' di atas untuk memproses paket dengan urutan FIFO (First In First Out) dan memindahkannya ke Riwayat.")
    else:
        st.info("💡 Tambahkan paket ke antrean untuk melihat opsi pengiriman.")


