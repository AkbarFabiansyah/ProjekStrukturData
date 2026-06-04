import streamlit as st
import os
import sys
import time


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
    page_title="Navigasi - Drone Delivery",
    page_icon="🗺️",
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

# Map Coordinates
BASE_COORDS = (250, 200)
DESTINATIONS = {
    "Kesambi": (150, 100),
    "Kejaksan": (350, 90),
    "Harjamukti": (130, 280),
    "Sumber": (90, 180),
    "Palimanan": (390, 290)
}

# =====================
# REALTIME ANIMATION LOOP
# =====================
# If there are active deliveries, run animation
if st.session_state.active_deliveries:
    run_sim = st.sidebar.toggle("Mulai Navigasi Otomatis", value=True)
    
    if run_sim:
        completed = []
        for i, delivery in enumerate(st.session_state.active_deliveries):
            # Advance progress
            delivery["progress"] += 10
            if delivery["progress"] >= 100:
                delivery["progress"] = 100
                completed.append(i)
        
        # Process completed deliveries
        if completed:
            for idx in sorted(completed, reverse=True):
                done = st.session_state.active_deliveries.pop(idx)
                
                # Reset drone status
                drone_id = done["drone_id"]
                for d in st.session_state.drones:
                    if d["id"] == drone_id:
                        d["status"] = "Ready"
                        d["current_job"] = None
                        d["battery"] = max(10, d["battery"] - 15)  # consume 15% battery
                        break
                
                # Add to history
                paket = done["paket"]
                paket["status"] = "Terkirim"
                st.session_state.history.append(paket)

            
        time.sleep(0.8)
        st.rerun()

# =====================
# MAIN CONTENT
# =====================
st.markdown("## 🗺️ Peta Navigasi Autopilot")
st.markdown("Visualisasi rute penerbangan dan posisi drone secara langsung.")
st.markdown("---")

container = st.container()

def generate_map_svg():
    svg_width = 500
    svg_height = 400
    
    # Grid lines & Radar circles
    svg_content = f"""
    <svg width='100%' height='400' viewBox='0 0 {svg_width} {svg_height}' style='background-color: #0c101d; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);'>
        <!-- Radial Radar Rings -->
        <circle cx='250' cy='200' r='120' stroke='rgba(0, 242, 254, 0.05)' stroke-width='1.5' fill='none' />
        <circle cx='250' cy='200' r='180' stroke='rgba(0, 242, 254, 0.05)' stroke-width='1.5' fill='none' />
    """
    
    # Draw Active Flight Tracks & Drones
    bx, by = BASE_COORDS
    for delivery in st.session_state.active_deliveries:
        dest_name = delivery["paket"]["tujuan"]
        if dest_name in DESTINATIONS:
            dx, dy = DESTINATIONS[dest_name]
            prog = delivery["progress"] / 100.0
            drone_x = bx + (dx - bx) * prog
            drone_y = by + (dy - by) * prog
            svg_content += f"""
            <line x1='{bx}' y1='{by}' x2='{drone_x}' y2='{drone_y}' stroke='url(#cyan-grad)' stroke-width='3' />
            <circle cx='{drone_x}' cy='{drone_y}' r='12' fill='rgba(0, 242, 254, 0.2)' />
            <circle cx='{drone_x}' cy='{drone_y}' r='6' fill='#00f2fe' />
            <text x='{drone_x + 10}' y='{drone_y - 10}' fill='#00f2fe' font-size='10' font-weight='bold'>{delivery["drone_id"]}</text>
            """
    
    # Draw Base Station Center Node
    svg_content += f"""
        <circle cx='{bx}' cy='{by}' r='12' fill='#090d16' stroke='#00f2fe' stroke-width='2.5' />
        <circle cx='{bx}' cy='{by}' r='5' fill='#00f2fe' />
        <text x='{bx - 18}' y='{by - 18}' fill='#00f2fe' font-size='12' font-weight='bold'>HQ BASE</text>
        
        <!-- Definitions for gradients -->
        <defs>
            <linearGradient id='cyan-grad' x1='0%' y1='0%' x2='100%' y2='100%'>
                <stop offset='0%' stop-color='#9d4edd' stop-opacity='0.2' />
                <stop offset='100%' stop-color='#00f2fe' stop-opacity='1' />
            </linearGradient>
        </defs>
    </svg>
    """
    return svg_content

with container:
    st.markdown("### 🗺️ Peta Taktis Real-Time")
    st.markdown(generate_map_svg(), unsafe_allow_html=True)


    st.markdown("### 📡 Status Pengiriman Aktif")
    
    if st.session_state.active_deliveries:
        for delivery in st.session_state.active_deliveries:
            paket = delivery["paket"]
            prog = delivery["progress"]
            
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 20px; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-weight: bold; color: #ffffff; font-size: 1.1rem;">🚁 {delivery['drone_id']}</span>
                    <span class="badge badge-sent" style="background: rgba(0, 242, 254, 0.1); color: #00f2fe; border: 1px solid rgba(0, 242, 254, 0.3);">{delivery['status']} {prog}%</span>
                </div>
                <div style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 12px;">
                    Paket: <b>{paket['paket']}</b><br>
                    Tujuan: <b>{paket['tujuan']}</b> (Penerima: {paket['penerima']})<br>
                    Prioritas: <b>{paket.get('priority', 'Regular')}</b>
                </div>
                <div style="width: 100%; background-color: rgba(255,255,255,0.05); height: 8px; border-radius: 4px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #9d4edd, #00f2fe); width: {prog}%; height: 100%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ Tidak ada drone yang sedang melakukan penerbangan aktif. Tugaskan drone pada menu 'Antrean Drone'.")
        
    st.markdown("### 📶 Informasi Sinyal & Cuaca")
    st.markdown("""
    <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 15px;">
        <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem; color: #94a3b8;">
            <tr>
                <td style="padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.03);">Satelit GPS</td>
                <td style="text-align: right; color: #10b981; font-weight: bold; padding: 6px 0;">12 Satelit (Kuat)</td>
            </tr>
            <tr>
                <td style="padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.03);">Kecepatan Angin</td>
                <td style="text-align: right; color: #10b981; font-weight: bold; padding: 6px 0;">8 km/h (Aman)</td>
            </tr>
            <tr>
                <td style="padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.03);">Kondisi Cuaca</td>
                <td style="text-align: right; color: #10b981; font-weight: bold; padding: 6px 0;">Cerah / Jelas</td>
            </tr>
            <tr>
                <td style="padding: 6px 0;">Status Transmiter</td>
                <td style="text-align: right; color: #10b981; font-weight: bold; padding: 6px 0;">Koneksi Stabil</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
