import streamlit as st
import os
import sys

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
    page_title="Tambah Paket - Drone Delivery",
    page_icon="📦",
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

# =====================
# MAIN CONTENT
# =====================
st.markdown("## 📦 Tambah Paket Baru")
st.markdown("Daftarkan paket baru untuk masuk ke dalam antrean pengiriman autopilot drone.")
st.markdown("---")

col1, col2 = st.columns([2, 1.2])

with col1:
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    
    with st.form("tambah_paket_form", clear_on_submit=True):
        st.markdown("<h3 style='color: #00f2fe; margin-top: 0; margin-bottom: 20px;'>Form Input Pengiriman</h3>", unsafe_allow_html=True)
        
        penerima = st.text_input(
            "Nama Penerima",
            placeholder="Masukkan nama penerima..."
        )
        
        paket = st.text_input(
            "Nama/Jenis Paket",
            placeholder="Contoh: Dokumen Medis, Suku Cadang, Makanan..."
        )
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            tujuan = st.selectbox(
                "Tujuan Destinasi",
                ["Kesambi", "Kejaksan", "Harjamukti", "Sumber", "Palimanan"]
            )
            
        with col_b:
            priority = st.selectbox(
                "Prioritas Pengiriman",
                ["Regular", "Express"]
            )
            
        berat = st.slider(
            "Berat Paket (kg)",
            min_value=0.1,
            max_value=8.0,
            value=1.0,
            step=0.1
        )
        
        submit = st.form_submit_button("📥 Tambahkan Ke Antrean")
        
        if submit:
            if not penerima.strip() or not paket.strip():
                st.error("⚠️ Nama penerima dan nama paket tidak boleh kosong.")
            else:
                data = {
                    "penerima": penerima.strip(),
                    "paket": paket.strip(),
                    "tujuan": tujuan,
                    "priority": priority,
                    "berat": berat,
                    "status": "Pending"
                }
                
                # Enqueue into the Linked List
                st.session_state.queue.enqueue(data)
                
                st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 15px; margin-top: 15px;">
                    <h5 style="color: #10b981; margin: 0 0 5px 0;">🎉 Berhasil Ditambahkan!</h5>
                    <p style="color: #94a3b8; margin: 0; font-size: 0.9rem;">
                        Paket untuk <b>{penerima}</b> ({paket}) menuju <b>{tujuan}</b> telah terdaftar di antrean.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("### 📋 Antrean Saat Ini")
    
    current_queue = st.session_state.queue.get_all()
    
    if current_queue:
        st.markdown(f"Terdapat **{len(current_queue)}** paket dalam antrean.")
        
        # Display first few packages in the queue
        for i, item in enumerate(current_queue[:5]):
            badge_class = "badge-pending"
            st.markdown(f"""
            <div class="package-card">
                <div class="package-info">
                    <span class="package-name">{item['paket']}</span>
                    <span class="package-meta">Penerima: {item['penerima']} | Destinasi: {item['tujuan']}</span>
                    <span class="package-meta" style="color: #6366f1;">Berat: {item['berat']} kg | Prioritas: {item['priority']}</span>
                </div>
                <div>
                    <span class="badge {badge_class}">{item['status']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        if len(current_queue) > 5:
            st.caption(f"...dan {len(current_queue) - 5} paket lainnya.")
    else:
        st.info("ℹ️ Antrean kosong. Silakan tambahkan paket untuk memulai.")
