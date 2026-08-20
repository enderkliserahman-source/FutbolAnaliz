import streamlit as st
import pandas as pd
import numpy as np

# Sayfa Ayarları
st.set_page_config(
    page_title="Futbol Analiz Pro",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 1. Kupon ve Sayfa Hafızası (Session State)
if "active_page" not in st.session_state:
    st.session_state.active_page = "bulten"
if "selected_match_id" not in st.session_state:
    st.session_state.selected_match_id = None
if "my_coupon" not in st.session_state:
    st.session_state.my_coupon = {}

# 2. Canlı Bülten Veritabanı
matches_db = [
    {
        "id": 1,
        "league": "UEFA AVRUPA LİGİ, PLAYOFF",
        "time": "19:00",
        "home": "J. Bialystok",
        "away": "Iberia 1999",
        "ms1": 1.23, "msx": 4.44, "ms2": 7.26, "alt": 1.91, "ust": 1.53, "kg_var": 1.70, "kg_yok": 1.85,
        "ev_pick": "2.5 Üst", "ev_val": "%9.2 +EV", "confidence": 76,
        "xg_home": 2.30, "xg_away": 0.65, "mc_1": "%71", "mc_x": "%18", "mc_2": "%11"
    },
    {
        "id": 2,
        "league": "UEFA AVRUPA LİGİ, PLAYOFF",
        "time": "19:00",
        "home": "Mjallby",
        "away": "Salzburg",
        "ms1": 3.82, "msx": 3.63, "ms2": 1.57, "alt": 2.14, "ust": 1.41, "kg_var": 1.50, "kg_yok": 2.10,
        "ev_pick": "MS 2", "ev_val": "%7.8 +EV", "confidence": 72,
        "xg_home": 0.95, "xg_away": 2.10, "mc_1": "%19", "mc_x": "%23", "mc_2": "%58"
    },
    {
        "id": 3,
        "league": "UEFA KONFERANS LİGİ, PLAYOFF",
        "time": "20:00",
        "home": "Nordsjælland",
        "away": "St. Gallen",
        "ms1": 1.37, "msx": 4.36, "ms2": 4.59, "alt": 2.15, "ust": 1.52, "kg_var": 1.48, "kg_yok": 2.10,
        "ev_pick": "MS 1 & 2.5 Üst", "ev_val": "%10.4 +EV", "confidence": 80,
        "xg_home": 2.45, "xg_away": 1.10, "mc_1": "%65", "mc_x": "%20", "mc_2": "%15"
    },
    {
        "id": 4,
        "league": "PORTEKİZ U23 NEXT GEN LİGİ",
        "time": "19:00",
        "home": "Benfica U23",
        "away": "Rio Ave U23",
        "ms1": 1.96, "msx": 3.11, "ms2": 2.64, "alt": 1.84, "ust": 1.51, "kg_var": 1.55, "kg_yok": 2.05,
        "ev_pick": "KG Var", "ev_val": "%6.5 +EV", "confidence": 68,
        "xg_home": 1.60, "xg_away": 1.40, "mc_1": "%42", "mc_x": "%28", "mc_2": "%30"
    }
]

# 3. İstenmeyen Elementleri Gizleme & Mobil Güvenli Alan CSS
st.markdown("""
<style>
    /* ÜSTTEKİ FORK, GITHUB, HEADER VE ALTTARZ TAÇ LOGOLARINI GİZLE */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    footer {
        display: none !important;
    }
    #MainMenu {
        visibility: hidden !important;
    }
    .stDeployButton {
        display: none !important;
    }
    div[class*="viewerBadge"] {
        display: none !important;
    }

    /* Genel Sayfa ve Kaydırma Ayarları */
    html, body, [class*="css"], .stApp {
        overflow-x: hidden !important;
        background-color: #f1f5f9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Üstten ve alttan güvenli pay bırakma */
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 6.5rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }

    /* Lig Bandı */
    .league-banner {
        background: #0f2438;
        color: #e2e8f0;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 6px 10px;
        border-radius: 6px;
        margin-top: 8px;
        margin-bottom: 4px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        text-transform: uppercase;
    }
    .league-title { color: #38bdf8; }

    /* Pazar Başlığı */
    .market-header {
        background: #cfe2f3;
        color: #0f2438;
        font-size: 11px;
        font-weight: 800;
        padding: 5px 8px;
        border-radius: 5px;
        margin: 8px 0 4px 0;
        display: flex;
        align-items: center;
    }
    .badge {
        background: #e63946;
        color: white;
        font-size: 10px;
        padding: 1px 4px;
        border-radius: 3px;
        margin-right: 5px;
        font-weight: bold;
    }

    /* Yan Yana Buton Izgarası */
    div[data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0px !important;
        padding: 0 1px !important;
    }
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: 3px !important;
        background: #ffffff;
        padding: 4px 4px;
        border-radius: 8px;
        margin-bottom: 4px;
        border: 1px solid #cbd5e1;
    }

    /* Buton Tasarımları */
    div.stButton > button {
        background: #1e3a5f !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 800 !important;
        font-size: 0.78rem !important;
        padding: 6px 1px !important;
        min-height: 36px !important;
        width: 100% !important;
        line-height: 1.1 !important;
    }

    /* Alt Sabit Bar (Genişletilmiş ve Yukarı Kaldırılmış) */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #0f2438;
        color: white;
        padding: 8px 14px 14px 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 2px solid #e63946;
        z-index: 999999;
        box-sizing: border-box;
    }
</style>
""", unsafe_allow_html=True)

# Bahis Seçim Fonksiyonu
def toggle_selection(match_id, match_name, pick_type, odd):
    key = f"{match_id}_{pick_type}"
    if key in st.session_state.my_coupon:
        del st.session_state.my_coupon[key]
    else:
        st.session_state.my_coupon[key] = {
            "match_id": match_id,
            "match": match_name,
            "pick": pick_type,
            "odd": odd
        }

# ==========================================
# 1. SAYFA: CANLI BÜLTEN LİSTESİ
# ==========================================
if st.session_state.active_page == "bulten":
    st.markdown("""
    <div style="text-align:center; padding: 4px 0 10px 0;">
        <h3 style="margin:0; color:#0f2438; font-weight:800; font-size:1.3rem;">⚽ GÜNÜN BÜLTENİ</h3>
        <span style="font-size:0.75rem; color:#64748b;">Oranlar ve Model Analizi İçin Maça Dokunun</span>
    </div>
    """, unsafe_allow_html=True)

    current_league = ""
    for m in matches_db:
        if m["league"] != current_league:
            current_league = m["league"]
            st.markdown(f"""
            <div class="league-banner">
                <span class="league-title">🏆 {current_league}</span>
                <span>⏱ {m['time']}</span>
            </div>
            """, unsafe_allow_html=True)

        if st.button(f"⭐ {m['home']} — {m['away']}  ➔", key=f"match_{m['id']}", use_container_width=True):
            st.session_state.selected_match_id = m["id"]
            st.session_state.active_page = "detay"
            st.rerun()

# ==========================================
# 2. SAYFA: DETAYLI MAÇ ANALİZİ VE ORANLAR
# ==========================================
elif st.session_state.active_page == "detay":
    match = next((x for x in matches_db if x["id"] == st.session_state.selected_match_id), matches_db[0])
    match_title = f"{match['home']} - {match['away']}"

    if st.button("⬅ Bültene Geri Dön", key="back_btn"):
        st.session_state.active_page = "bulten"
        st.rerun()

    st.markdown(f"""
    <div style="background:#0f2438; color:white; padding:10px; border-radius:10px; text-align:center; margin:4px 0 8px 0;">
        <div style="font-size:0.75rem; color:#94a3b8;">⏱ {match['time']} • {match['league']}</div>
        <div style="font-size:1.05rem; font-weight:800; margin-top:2px;">{match_title}</div>
    </div>
    """, unsafe_allow_html=True)

    t_oran, t_ist, t_sim = st.tabs(["📌 Oranlar", "📊 Model & xG", "🎲 Simülasyon"])

    with t_oran:
        # Dinamik Kırmızı Vurgu
        custom_red_css = ""
        for k in st.session_state.my_coupon.keys():
            custom_red_css += f"div.stButton > button[key='btn_{k}'] {{ background: #e63946 !important; border: 1px solid #ffccd5 !important; }}\n"
        if custom_red_css:
            st.markdown(f"<style>{custom_red_css}</style>", unsafe_allow_html=True)

        # 1. MAÇ SONUCU
        st.markdown('<div class="market-header"><span class="badge">1</span> MAÇ SONUCU</div>', unsafe_allow_html=True)
        c_title, c1, c2, c3 = st.columns([1.5, 1, 1, 1])
        c_title.markdown('<div style="font-size:12px; font-weight:700; color:#1e293b; padding-top:6px;">Maç Sonucu</div>', unsafe_allow_html=True)
        with c1:
            if st.button(f"1\n{match['ms1']}", key=f"btn_{match['id']}_MS1"):
                toggle_selection(match['id'], match_title, "MS1", match['ms1'])
                st.rerun()
        with c2:
            if st.button(f"X\n{match['msx']}", key=f"btn_{match['id']}_MSX"):
                toggle_selection(match['id'], match_title, "MSX", match['msx'])
                st.rerun()
        with c3:
            if st.button(f"2\n{match['ms2']}", key=f"btn_{match['id']}_MS2"):
                toggle_selection(match['id'], match_title, "MS2", match['ms2'])
                st.rerun()

        # 2. 2.5 ALT / ÜST
        st.markdown('<div class="market-header"><span class="badge">1</span> 2.5 ALT / ÜST</div>', unsafe_allow_html=True)
        c_ou_t, c_ou1, c_ou2 = st.columns([1.5, 1.5, 1.5])
        c_ou_t.markdown('<div style="font-size:12px; font-weight:700; color:#1e293b; padding-top:6px;">2.5 Gol</div>', unsafe_allow_html=True)
        with c_ou1:
            if st.button(f"Alt\n{match['alt']}", key=f"btn_{match['id']}_Alt"):
                toggle_selection(match['id'], match_title, "Alt", match['alt'])
                st.rerun()
        with c_ou2:
            if st.button(f"Üst\n{match['ust']}", key=f"btn_{match['id']}_Ust"):
                toggle_selection(match['id'], match_title, "Ust", match['ust'])
                st.rerun()

        # 3. KARŞILIKLI GOL
        st.markdown('<div class="market-header"><span class="badge">1</span> KARŞILIKLI GOL</div>', unsafe_allow_html=True)
        c_kg_t, c_kg1, c_kg2 = st.columns([1.5, 1.5, 1.5])
        c_kg_t.markdown('<div style="font-size:12px; font-weight:700; color:#1e293b; padding-top:6px;">KG Var/Yok</div>', unsafe_allow_html=True)
        with c_kg1:
            if st.button(f"Var\n{match['kg_var']}", key=f"btn_{match['id']}_KGVar"):
                toggle_selection(match['id'], match_title, "KGVar", match['kg_var'])
                st.rerun()
        with c_kg2:
            if st.button(f"Yok\n{match['kg_yok']}", key=f"btn_{match['id']}_KGYok"):
                toggle_selection(match['id'], match_title, "KGYok", match['kg_yok'])
                st.rerun()

    with t_ist:
        st.info(f"🎯 **Model Tercihi:** `{match['ev_pick']}` ({match['ev_val']})")
        c_x1, c_x2 = st.columns(2)
        c_x1.metric(f"xG ({match['home']})", match['xg_home'])
        c_x2.metric(f"xG ({match['away']})", match['xg_away'])
        st.progress(match['confidence'], text=f"Model Güven Endeksi: %{match['confidence']}")

    with t_sim:
        st.write("🎲 **Monte Carlo 10.000 Maç Simülasyonu:**")
        c1, c2, c3 = st.columns(3)
        c1.metric("1 (Ev)", match['mc_1'])
        c2.metric("X (Ber)", match['mc_x'])
        c3.metric("2 (Dep)", match['mc_2'])

# ==========================================
# ALT SABİT KUPON BAR
# ==========================================
coupon_items = list(st.session_state.my_coupon.values())
bet_count = len(coupon_items)
total_odds = 1.0

if bet_count > 0:
    for item in coupon_items:
        total_odds *= item["odd"]
    odds_str = f"{total_odds:.2f}"
else:
    odds_str = "0.00"

st.markdown(f"""
<div class="bottom-nav">
    <div>
        <span style="font-size:0.75rem; color:#94a3b8;">Kuponum ({bet_count} Seçim)</span><br>
        <span style="font-size:1.15rem; font-weight:800; color:#38bdf8;">Toplam: {odds_str}</span>
    </div>
    <div style="background:#e63946; padding:6px 12px; border-radius:6px; font-weight:bold; font-size:0.8rem; cursor:pointer;">
        Kuponu İncele ➔
    </div>
</div>
""", unsafe_allow_html=True)