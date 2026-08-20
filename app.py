import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Futbol Analiz",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Açık Ferah Zemin, Lacivert/Mavi Nesine/Bilyoner Tarzı CSS
st.markdown("""
<style>
    /* Açık Buz Mavisi / Huzurlu Zemin */
    .stApp {
        background: #f0f4f9;
        color: #1e293b;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 4rem;
        padding-left: 0.6rem;
        padding-right: 0.6rem;
    }

    /* Başlık Alanı */
    .app-header {
        text-align: center;
        margin-bottom: 1rem;
    }
    .app-header h2 {
        color: #0f172a;
        font-weight: 800;
        font-size: 1.4rem;
        margin-bottom: 2px;
    }
    .app-header p {
        color: #2563eb;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* Maç Kartı (Temiz Beyaz & İnce Mavi Kenarlık) */
    .match-card {
        background: #ffffff;
        border: 1px solid #dbeafe;
        border-radius: 12px;
        padding: 10px 12px 6px 12px;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.06);
    }

    .card-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.72rem;
        color: #64748b;
        margin-bottom: 6px;
        font-weight: 600;
    }
    
    .team-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #0f172a;
        text-align: center;
        margin-bottom: 8px;
    }

    /* +EV Rozeti (Mavi Vurgulu) */
    .badge-ev {
        background: #eff6ff;
        color: #1d4ed8;
        border: 1px solid #bfdbfe;
        padding: 2px 7px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.72rem;
    }

    /* MOBİLDE SÜTUNLARIN YAN YANA KALMASINI ZORLAYAN SİHİRLİ KOD */
    div[data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
        padding: 0 2px !important;
    }
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 3px !important;
    }

    /* Lacivert/Mavi Nesine Tarzı Oran Butonları */
    div.stButton > button {
        background: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 6px !important;
        font-weight: 700 !important;
        font-size: 0.75rem !important;
        padding: 4px 1px !important;
        line-height: 1.1 !important;
        width: 100% !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03) !important;
    }
    
    div.stButton > button:hover {
        background: #1d4ed8 !important;
        color: #ffffff !important;
        border-color: #1d4ed8 !important;
    }
    
    div.stButton > button:active {
        background: #0f172a !important;
        color: #ffffff !important;
    }

    /* Akordiyon Menü Tasarımı */
    .streamlit-expanderHeader {
        background-color: #f8fafc !important;
        color: #1e3a8a !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 6px !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# Başlık
st.markdown("""
<div class="app-header">
    <h2>⚽ FUTBOL ANALİZ</h2>
    <p>Poisson Modeli • Değerli Oran Radarı (+EV)</p>
</div>
""", unsafe_allow_html=True)

# Örnek Maçlar
matches = [
    {
        "id": 1, "time": "20:00", "league": "Avrupa Ligi",
        "home": "Beşiktaş", "away": "Bodo Glimt",
        "ms1": "2.10", "msx": "3.40", "ms2": "2.80", "ust": "1.65", "kg": "1.55",
        "ev_pick": "MS 1 & 2.5 Üst", "ev_val": "%8.4 +EV",
        "confidence": 72, "probs": "1: %48 | X: %26 | 2: %26"
    },
    {
        "id": 2, "time": "20:00", "league": "Konferans Ligi",
        "home": "Trabzonspor", "away": "St. Gallen",
        "ms1": "1.75", "msx": "3.60", "ms2": "3.90", "ust": "1.70", "kg": "1.68",
        "ev_pick": "MS 1", "ev_val": "%6.2 +EV",
        "confidence": 68, "probs": "1: %54 | X: %24 | 2: %22"
    },
    {
        "id": 3, "time": "22:00", "league": "Şampiyonlar Ligi",
        "home": "Real Madrid", "away": "Atalanta",
        "ms1": "1.55", "msx": "4.20", "ms2": "5.10", "ust": "1.50", "kg": "1.60",
        "ev_pick": "2.5 Üst", "ev_val": "%11.0 +EV",
        "confidence": 81, "probs": "1: %62 | X: %21 | 2: %17"
    }
]

for m in matches:
    # Maç Kartı
    st.markdown(f"""
    <div class="match-card">
        <div class="card-top">
            <span>⏱ {m['time']} • {m['league']}</span>
            <span class="badge-ev">{m['ev_val']}</span>
        </div>
        <div class="team-title">{m['home']} - {m['away']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Kesin Olarak Mobilde Yan Yana 5 Oran Butonu
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.button(f"1\n{m['ms1']}", key=f"ms1_{m['id']}", use_container_width=True)
    with c2:
        st.button(f"X\n{m['msx']}", key=f"msx_{m['id']}", use_container_width=True)
    with c3:
        st.button(f"2\n{m['ms2']}", key=f"ms2_{m['id']}", use_container_width=True)
    with c4:
        st.button(f"Üst\n{m['ust']}", key=f"ust_{m['id']}", use_container_width=True)
    with c5:
        st.button(f"KG\n{m['kg']}", key=f"kg_{m['id']}", use_container_width=True)
        
    # Model Açılır Detay Menüsü
    with st.expander(f"📊 Analiz: {m['home']} vs {m['away']}"):
        st.markdown(f"**🎯 Model Tercihi:** `{m['ev_pick']}`")
        st.progress(m['confidence'], text=f"Güven Endeksi: %{m['confidence']}")
        st.caption(f"Dağılım: {m['probs']}")
    
    st.write("")