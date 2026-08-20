import streamlit as st
import pandas as pd
import numpy as np

# Mobil Sayfa Ayarı
st.set_page_config(
    page_title="Nesine Tarzı Maç Analiz",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Kupon Durumu (State) Yönetimi
if "selected_bets" not in st.session_state:
    st.session_state.selected_bets = {}

# Özel CSS: Nesine/Bilyoner Birebir Mimarisi & Mavi/Kırmızı Tema
st.markdown("""
<style>
    /* Genel Arka Plan */
    .stApp {
        background-color: #f1f5f9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 5.5rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }

    /* Üst Maç Başlık Alanı (Koyu Gece Mavisi) */
    .header-box {
        background: #0f2438;
        color: #ffffff;
        padding: 14px 12px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
    }
    .header-time {
        font-size: 0.8rem;
        color: #94a3b8;
        margin-bottom: 3px;
    }
    .header-league {
        font-size: 0.75rem;
        color: #38bdf8;
        font-weight: 600;
        margin-bottom: 6px;
        text-transform: uppercase;
    }
    .header-teams {
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: 0.3px;
    }

    /* Pazar / Kategori Şeridi */
    .market-header {
        background: #cfe2f3;
        color: #0f2438;
        font-size: 0.78rem;
        font-weight: 800;
        padding: 6px 10px;
        border-radius: 6px;
        margin-top: 10px;
        margin-bottom: 6px;
        text-transform: uppercase;
        display: flex;
        align-items: center;
    }
    .market-badge {
        background: #e63946;
        color: white;
        font-size: 0.65rem;
        padding: 1px 5px;
        border-radius: 3px;
        margin-right: 6px;
        font-weight: bold;
    }

    /* Satır Düzeni & Buton Yan Yana Kilidi */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: 4px !important;
        background: #ffffff;
        padding: 6px 6px;
        border-radius: 8px;
        margin-bottom: 4px;
        border: 1px solid #e2e8f0;
    }
    div[data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }

    /* Bahis Etiket Başlıkları (MS 1, MS X vb.) */
    .bet-label {
        font-size: 0.65rem;
        color: #64748b;
        text-align: center;
        font-weight: 700;
        margin-bottom: 2px;
        line-height: 1;
    }
    .market-title-col {
        font-size: 0.8rem;
        font-weight: 700;
        color: #1e293b;
        display: flex;
        align-items: center;
    }

    /* Buton Tasarımları (Varsayılan Koyu Mavi) */
    div.stButton > button {
        background: #1e3a5f !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 800 !important;
        font-size: 0.88rem !important;
        padding: 6px 2px !important;
        min-height: 38px !important;
        width: 100% !important;
    }

    /* Alt Sabit Kupon Çubuğu */
    .bottom-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #0f2438;
        color: white;
        padding: 10px 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 2px solid #e63946;
        z-index: 99999;
        box-shadow: 0 -3px 10px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Üst Başlık Kartı
st.markdown("""
<div class="header-box">
    <div class="header-time">Bugün 20:00</div>
    <div class="header-league">UEFA Avrupa Konferans Ligi, Playoff</div>
    <div class="header-teams">Nordsjælland — St. Gallen</div>
</div>
""", unsafe_allow_html=True)

# Üst Sekmeler
tab_oranlar, tab_istatistik, tab_simulasyon = st.tabs(["📌 Oranlar", "📊 Model İstatistikleri", "🎲 Monte Carlo"])

# Bahis Seçim Fonksiyonu
def toggle_bet(market, selection, odd):
    key = f"{market}_{selection}"
    if key in st.session_state.selected_bets:
        del st.session_state.selected_bets[key]
    else:
        st.session_state.selected_bets[key] = {"market": market, "pick": selection, "odd": odd}

# --- SEKME 1: NESİNE ORANLAR EKRANI ---
with tab_oranlar:
    # 1. Kategori: MAÇ SONUCU
    st.markdown('<div class="market-header"><span class="market-badge">1</span> MAÇ SONUCU</div>', unsafe_allow_html=True)
    
    c_title, c1, c2, c3 = st.columns([1.6, 1, 1, 1])
    with c_title:
        st.markdown('<div class="market-title-col">📌 Maç Sonucu</div>', unsafe_allow_html=True)
    with c1:
        st.markdown('<div class="bet-label">MS 1</div>', unsafe_allow_html=True)
        btn1 = st.button("1.37", key="btn_ms1", use_container_width=True)
        if btn1: toggle_bet("Maç Sonucu", "1", 1.37)
    with c2:
        st.markdown('<div class="bet-label">MS X</div>', unsafe_allow_html=True)
        btnX = st.button("4.36", key="btn_msx", use_container_width=True)
        if btnX: toggle_bet("Maç Sonucu", "X", 4.36)
    with c3:
        st.markdown('<div class="bet-label">MS 2</div>', unsafe_allow_html=True)
        btn2 = st.button("4.59", key="btn_ms2", use_container_width=True)
        if btn2: toggle_bet("Maç Sonucu", "2", 4.59)

    # 2. Kategori: ÇİFTE ŞANS
    st.markdown('<div class="market-header"><span class="market-badge">1</span> ÇİFTE ŞANS</div>', unsafe_allow_html=True)
    c_cs_t, c_cs1, c_cs2, c_cs3 = st.columns([1.6, 1, 1, 1])
    with c_cs_t:
        st.markdown('<div class="market-title-col">📌 Çifte Şans</div>', unsafe_allow_html=True)
    with c_cs1:
        st.markdown('<div class="bet-label">ÇŞ 1-X</div>', unsafe_allow_html=True)
        btn_cs1 = st.button("1.05", key="btn_cs1", use_container_width=True)
        if btn_cs1: toggle_bet("Çifte Şans", "1-X", 1.05)
    with c_cs2:
        st.markdown('<div class="bet-label">ÇŞ 1-2</div>', unsafe_allow_html=True)
        btn_cs2 = st.button("1.07", key="btn_cs2", use_container_width=True)
        if btn_cs2: toggle_bet("Çifte Şans", "1-2", 1.07)
    with c_cs3:
        st.markdown('<div class="bet-label">ÇŞ X-2</div>', unsafe_allow_html=True)
        btn_cs3 = st.button("2.17", key="btn_cs3", use_container_width=True)
        if btn_cs3: toggle_bet("Çifte Şans", "X-2", 2.17)

    # 3. Kategori: ALT / ÜST (2.5 GOL)
    st.markdown('<div class="market-header"><span class="market-badge">1</span> TOPLAM GOL (2.5)</div>', unsafe_allow_html=True)
    c_ou_t, c_ou1, c_ou2 = st.columns([1.6, 1.5, 1.5])
    with c_ou_t:
        st.markdown('<div class="market-title-col">📌 2.5 Alt/Üst</div>', unsafe_allow_html=True)
    with c_ou1:
        st.markdown('<div class="bet-label">Alt</div>', unsafe_allow_html=True)
        btn_alt = st.button("2.15", key="btn_alt", use_container_width=True)
        if btn_alt: toggle_bet("2.5 Gol", "Alt", 2.15)
    with c_ou2:
        st.markdown('<div class="bet-label">Üst</div>', unsafe_allow_html=True)
        btn_ust = st.button("1.52", key="btn_ust", use_container_width=True)
        if btn_ust: toggle_bet("2.5 Gol", "Üst", 1.52)

    # 4. Kategori: KARŞILIKLI GOL
    st.markdown('<div class="market-header"><span class="market-badge">1</span> KARŞILIKLI GOL</div>', unsafe_allow_html=True)
    c_kg_t, c_kg1, c_kg2 = st.columns([1.6, 1.5, 1.5])
    with c_kg_t:
        st.markdown('<div class="market-title-col">📌 KG Var/Yok</div>', unsafe_allow_html=True)
    with c_kg1:
        st.markdown('<div class="bet-label">Var</div>', unsafe_allow_html=True)
        btn_kgv = st.button("1.48", key="btn_kgv", use_container_width=True)
        if btn_kgv: toggle_bet("KG", "Var", 1.48)
    with c_kg2:
        st.markdown('<div class="bet-label">Yok</div>', unsafe_allow_html=True)
        btn_kgy = st.button("2.10", key="btn_kgy", use_container_width=True)
        if btn_kgy: toggle_bet("KG", "Yok", 2.10)

# --- SEKME 2: MODEL İSTATİSTİKLERİ ---
with tab_istatistik:
    st.info("🎯 **Model Tercihi:** MS 1 & 2.5 Üst (%9.4 +EV Avantajı)")
    st.metric("Beklenen Gol (xG)", "Nordsjælland: 2.14 — St. Gallen: 0.88")
    st.progress(74, text="Model Güven Skoru: %74")

# --- SEKME 3: MONTE CARLO SİMÜLASYONU ---
with tab_simulasyon:
    st.write("🎲 **10.000 Maç Simülasyon Çıktısı:**")
    sim_col1, sim_col2, sim_col3 = st.columns(3)
    sim_col1.metric("Ev Galibiyeti", "%64.2")
    sim_col2.metric("Beraberlik", "%20.5")
    sim_col3.metric("Dep Galibiyeti", "%15.3")

# --- SEÇİLİ KUPON CSS VURGUSU (KIRMIZI BUTON) ---
# Tıklanan butonları anında kırmızıya çeviren dinamik CSS
selected_css = ""
for k in st.session_state.selected_bets.keys():
    if k == "Maç Sonucu_1": selected_css += "div.stButton > button[key='btn_ms1'] { background: #e63946 !important; }"
    if k == "Maç Sonucu_X": selected_css += "div.stButton > button[key='btn_msx'] { background: #e63946 !important; }"
    if k == "Maç Sonucu_2": selected_css += "div.stButton > button[key='btn_ms2'] { background: #e63946 !important; }"
    if k == "Çifte Şans_1-X": selected_css += "div.stButton > button[key='btn_cs1'] { background: #e63946 !important; }"
    if k == "Çifte Şans_1-2": selected_css += "div.stButton > button[key='btn_cs2'] { background: #e63946 !important; }"
    if k == "Çifte Şans_X-2": selected_css += "div.stButton > button[key='btn_cs3'] { background: #e63946 !important; }"
    if k == "2.5 Gol_Alt": selected_css += "div.stButton > button[key='btn_alt'] { background: #e63946 !important; }"
    if k == "2.5 Gol_Üst": selected_css += "div.stButton > button[key='btn_ust'] { background: #e63946 !important; }"
    if k == "KG_Var": selected_css += "div.stButton > button[key='btn_kgv'] { background: #e63946 !important; }"
    if k == "KG_Yok": selected_css += "div.stButton > button[key='btn_kgy'] { background: #e63946 !important; }"

if selected_css:
    st.markdown(f"<style>{selected_css}</style>", unsafe_allow_html=True)

# --- ALT SABİT KUPON ÇUBUĞU (BOTTOM BAR) ---
total_odds = 1.0
bet_count = len(st.session_state.selected_bets)
for b in st.session_state.selected_bets.values():
    total_odds *= b["odd"]

odds_display = f"{total_odds:.2f}" if bet_count > 0 else "0.00"

st.markdown(f"""
<div class="bottom-bar">
    <div>
        <span style="font-size:0.75rem; color:#94a3b8;">Kuponum ({bet_count} Maç/Tercih)</span><br>
        <span style="font-size:1.1rem; font-weight:800; color:#38bdf8;">Oran: {odds_display}</span>
    </div>
    <div style="background:#e63946; padding:6px 14px; border-radius:6px; font-weight:bold; font-size:0.85rem;">
        Kuponu İncele ➔
    </div>
</div>
""", unsafe_allow_html=True)