import streamlit as st
import pandas as pd
import numpy as np

# Mobil Sayfa Yapılandırması
st.set_page_config(
    page_title="Futbol Analiz Bülteni",
    page_icon="⚽",
    layout="centered", # Mobilde dikey odaklanma için centered
    initial_sidebar_state="collapsed"
)

# Nesine/Bilyoner Tarzı Özel Mobil CSS
st.markdown("""
<style>
    /* Ana gövde mobil boşluk ayarları */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 5rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }
    
    /* Maç Kartı Tasarımı */
    .match-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Oran Kutucukları */
    .odd-box {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 6px 4px;
        text-align: center;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 4px;
    }
    
    .odd-val {
        color: #0d6efd;
        font-size: 0.95rem;
    }
    
    .ev-badge {
        background-color: #d1e7dd;
        color: #0f5132;
        padding: 2px 6px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Üst Başlık & Bülten Filtresi
st.title("⚽ Canlı Bülten & Analiz")

# Mock Bülten Verisi (data_provider/bulletin_fetcher ile dinamikleşecek)
matches = [
    {
        "id": 1, "time": "20:00", "league": "Avrupa Ligi",
        "home": "Beşiktaş", "away": "Bodo Glimt",
        "ms1": 2.10, "msx": 3.40, "ms2": 2.80, "ust": 1.65, "kg_var": 1.55,
        "ev_pick": "MS 1 & 2.5 Üst", "ev_val": "%8.4 +EV"
    },
    {
        "id": 2, "time": "20:00", "league": "Konferans Ligi",
        "home": "Trabzonspor", "away": "St. Gallen",
        "ms1": 1.75, "msx": 3.60, "ms2": 3.90, "ust": 1.70, "kg_var": 1.68,
        "ev_pick": "MS 1", "ev_val": "%6.2 +EV"
    }
]

# Mobil Bülten Kartları Listesi
for m in matches:
    with st.container():
        st.markdown(f"""
        <div class="match-card">
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #6c757d; margin-bottom: 6px;">
                <span>⏱ {m['time']} • {m['league']}</span>
                <span class="ev-badge">{m['ev_val']} Fırsat</span>
            </div>
            <div style="font-size: 1.05rem; font-weight: bold; margin-bottom: 8px;">
                {m['home']} - {m['away']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Oran Butonları / Izgarası (Mobilde tam oturan 5 sütun)
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.button(f"1\n{m['ms1']}", key=f"ms1_{m['id']}", use_container_width=True)
        with c2:
            st.button(f"X\n{m['msx']}", key=f"msx_{m['id']}", use_container_width=True)
        with c3:
            st.button(f"2\n{m['ms2']}", key=f"ms2_{m['id']}", use_container_width=True)
        with c4:
            st.button(f"2.5 Ü\n{m['ust']}", key=f"ust_{m['id']}", use_container_width=True)
        with c5:
            st.button(f"KG\n{m['kg_var']}", key=f"kg_{m['id']}", use_container_width=True)
            
        # Maçın Detaylı Analiz Açılır Menüsü (Accordion)
        with st.expander(f"📊 {m['home']} vs {m['away']} Model İstatistikleri"):
            st.write(f"🎯 **Model Önerisi:** {m['ev_pick']}")
            st.progress(68, text="Model Güven Endeksi: %68")
            st.caption("Monte Carlo 10.000 Simülasyonu: Ev Sahibi Galibiyeti %48, Beraberlik %26, Deplasman %26")
        
        st.divider()