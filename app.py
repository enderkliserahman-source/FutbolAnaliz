import streamlit as st
import pandas as pd
import numpy as np

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Futbol Analiz Pro",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Gece Mavisi, Lacivert & Elektrik Mavisi Özel Mobil CSS
st.markdown("""
<style>
    /* Koyu Lacivert Arka Plan & Temel Yazı Rengi */
    .stApp {
        background: linear-gradient(135deg, #0b132b 0%, #1c2541 100%);
        color: #f0f3f8;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 5rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    /* Başlık Alanı */
    .app-header {
        text-align: center;
        margin-bottom: 1.2rem;
    }
    .app-header h2 {
        color: #ffffff;
        font-weight: 800;
        font-size: 1.5rem;
        margin-bottom: 0.2rem;
    }
    .app-header p {
        color: #48cae4;
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* Yatay Maç Kartı */
    .match-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 12px;
        margin-bottom: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .match-card:hover {
        border-color: #00b4d8;
    }

    /* Maç Bilgi Başlığı */
    .card-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.75rem;
        color: #94a3b8;
        margin-bottom: 8px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        padding-bottom: 4px;
    }
    
    .team-title {
        font-size: 1.02rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 10px;
        text-align: center;
        letter-spacing: 0.3px;
    }

    /* Değer / +EV Rozeti (Neon Cyan) */
    .badge-ev {
        background: rgba(0, 180, 216, 0.15);
        color: #00f0ff;
        border: 1px solid rgba(0, 240, 255, 0.3);
        padding: 2px 8px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.75rem;
        text-shadow: 0 0 8px rgba(0, 240, 255, 0.4);
    }

    /* Streamlit Butonlarını Lacivert/Mavi Şık Oran Kutularına Çevirme */
    div.stButton > button {
        background: linear-gradient(180deg, #1e3a5f 0%, #112240 100%) !important;
        color: #e2e8f0 !important;
        border: 1px solid #2563eb !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
        padding: 6px 2px !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(180deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        border-color: #60a5fa !important;
        box-shadow: 0 0 10px rgba(37, 99, 235, 0.5) !important;
    }

    /* Expander (Detay Menü) Koyu Tema Uyumu */
    .streamlit-expanderHeader {
        background-color: #162032 !important;
        color: #93c5fd !important;
        border-radius: 8px !important;
        font-size: 0.85rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Başlık
st.markdown("""
<div class="app-header">
    <h2>⚽ FUTBOL ANALİZ PRO</h2>
    <p>Poisson Dağılımı • Monte Carlo Simülasyonu • +EV Radar</p>
</div>
""", unsafe_allow_html=True)

# Örnek Bülten Verisi
matches = [
    {
        "id": 1, "time": "20:00", "league": "Avrupa Ligi",
        "home": "Beşiktaş", "away": "Bodo Glimt",
        "ms1": 2.10, "msx": 3.40, "ms2": 2.80, "ust": 1.65, "kg_var": 1.55,
        "ev_pick": "MS 1 & 2.5 Üst", "ev_val": "%8.4 +EV",
        "confidence": 72, "home_prob": "%48", "draw_prob": "%26", "away_prob": "%26"
    },
    {
        "id": 2, "time": "20:00", "league": "Konferans Ligi",
        "home": "Trabzonspor", "away": "St. Gallen",
        "ms1": 1.75, "msx": 3.60, "ms2": 3.90, "ust": 1.70, "kg_var": 1.68,
        "ev_pick": "MS 1", "ev_val": "%6.2 +EV",
        "confidence": 68, "home_prob": "%54", "draw_prob": "%24", "away_prob": "%22"
    },
    {
        "id": 3, "time": "22:00", "league": "Şampiyonlar Ligi",
        "home": "Real Madrid", "away": "Atalanta",
        "ms1": 1.55, "msx": 4.20, "ms2": 5.10, "ust": 1.50, "kg_var": 1.60,
        "ev_pick": "2.5 Üst", "ev_val": "%11.0 +EV",
        "confidence": 81, "home_prob": "%62", "draw_prob": "%21", "away_prob": "%17"
    },
    {
        "id": 4, "time": "22:00", "league": "Premier Lig",
        "home": "Chelsea", "away": "Newcastle",
        "ms1": 1.95, "msx": 3.75, "ms2": 3.30, "ust": 1.58, "kg_var": 1.52,
        "ev_pick": "KG Var", "ev_val": "%7.5 +EV",
        "confidence": 75, "home_prob": "%46", "draw_prob": "%26", "away_prob": "%28"
    }
]

# Maçları 2'şerli Sütunlarda Yan Yana Gösterme Grid'i
for i in range(0, len(matches), 2):
    cols = st.columns(2)
    for col_idx, match_idx in enumerate([i, i+1]):
        if match_idx < len(matches):
            m = matches[match_idx]
            with cols[col_idx]:
                # Kart Gövdesi
                st.markdown(f"""
                <div class="match-card">
                    <div class="card-top">
                        <span>⏱ {m['time']} • {m['league']}</span>
                        <span class="badge-ev">{m['ev_val']}</span>
                    </div>
                    <div class="team-title">{m['home']} - {m['away']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Oran Butonları Izgarası (5'li yan yana)
                b1, b2, b3, b4, b5 = st.columns(5)
                with b1:
                    st.button(f"1\n{m['ms1']}", key=f"ms1_{m['id']}", use_container_width=True)
                with b2:
                    st.button(f"X\n{m['msx']}", key=f"msx_{m['id']}", use_container_width=True)
                with b3:
                    st.button(f"2\n{m['ms2']}", key=f"ms2_{m['id']}", use_container_width=True)
                with b4:
                    st.button(f"Üst\n{m['ust']}", key=f"ust_{m['id']}", use_container_width=True)
                with b5:
                    st.button(f"KG\n{m['kg_var']}", key=f"kg_{m['id']}", use_container_width=True)
                
                # Akıllı Açılır Analiz Kutusu
                with st.expander(f"📊 Model Detayı ({m['home']} - {m['away']})"):
                    st.markdown(f"**🎯 Öneri:** `{m['ev_pick']}`")
                    st.progress(m['confidence'], text=f"Güven Endeksi: %{m['confidence']}")
                    st.caption(f"Monte Carlo: 1: {m['home_prob']} | X: {m['draw_prob']} | 2: {m['away_prob']}")
                
                st.write("") # Dikey hafif boşluk