import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Futbol Analiz Bülteni",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Session State Değişkenleri
if "active_page" not in st.session_state:
    st.session_state.active_page = "bulten"  # "bulten" veya "detay"
if "selected_match_id" not in st.session_state:
    st.session_state.selected_match_id = None
if "coupon" not in st.session_state:
    st.session_state.coupon = []

# Bülten Veritabanı
matches_db = [
    {
        "id": 1,
        "league": "UEFA AVRUPA LİGİ, PLAYOFF",
        "time": "Bugün 19:00",
        "home": "J. Bialystok",
        "away": "Iberia 1999",
        "ms1": 1.23, "msx": 4.44, "ms2": 7.26, "alt": 1.91, "ust": 1.53, "kg_var": 1.70, "kg_yok": 1.85,
        "ev_pick": "2.5 Üst", "ev_val": "%9.2 +EV", "confidence": 76,
        "xg_home": 2.30, "xg_away": 0.65, "mc_1": "%71", "mc_x": "%18", "mc_2": "%11"
    },
    {
        "id": 2,
        "league": "UEFA AVRUPA LİGİ, PLAYOFF",
        "time": "Bugün 19:00",
        "home": "Mjallby",
        "away": "Salzburg",
        "ms1": 3.82, "msx": 3.63, "ms2": 1.57, "alt": 2.14, "ust": 1.41, "kg_var": 1.50, "kg_yok": 2.10,
        "ev_pick": "MS 2", "ev_val": "%7.8 +EV", "confidence": 72,
        "xg_home": 0.95, "xg_away": 2.10, "mc_1": "%19", "mc_x": "%23", "mc_2": "%58"
    },
    {
        "id": 3,
        "league": "UEFA KONFERANS LİGİ, PLAYOFF",
        "time": "Bugün 20:00",
        "home": "Nordsjælland",
        "away": "St. Gallen",
        "ms1": 1.37, "msx": 4.36, "ms2": 4.59, "alt": 2.15, "ust": 1.52, "kg_var": 1.48, "kg_yok": 2.10,
        "ev_pick": "MS 1 & 2.5 Üst", "ev_val": "%10.4 +EV", "confidence": 80,
        "xg_home": 2.45, "xg_away": 1.10, "mc_1": "%65", "mc_x": "%20", "mc_2": "%15"
    },
    {
        "id": 4,
        "league": "PORTEKİZ U23 NEXT GEN LİGİ",
        "time": "Bugün 19:00",
        "home": "Benfica U23",
        "away": "Rio Ave U23",
        "ms1": 1.96, "msx": 3.11, "ms2": 2.64, "alt": 1.84, "ust": 1.51, "kg_var": 1.55, "kg_yok": 2.05,
        "ev_pick": "KG Var", "ev_val": "%6.5 +EV", "confidence": 68,
        "xg_home": 1.60, "xg_away": 1.40, "mc_1": "%42", "mc_x": "%28", "mc_2": "%30"
    }
]

# CSS: Nesine / Bilyoner Tarzı Kusursuz Mobil Düzen
st.markdown("""
<style>
    html, body, [class*="css"], .stApp {
        overflow-x: hidden !important;
        background-color: #f1f5f9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .block-container {
        padding: 0.4rem 0.5rem 5.5rem 0.5rem !important;
    }

    /* Lig Başlığı Bandı */
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
    .league-title {
        color: #38bdf8;
    }

    /* Maç Seçim Butonu (Tıklanabilir Liste Elemanı) */
    div.match-row > button {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        padding: 10px !important;
        text-align: left !important;
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        width: 100% !important;
        margin-bottom: 4px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
        display: flex !important;
        justify-content: space-between !important;
    }
    div.match-row > button:hover {
        border-color: #2563eb !important;
        background: #f8fafc !important;
    }

    /* Sabit Alt Bar */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #0f2438;
        color: white;
        padding: 8px 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 2px solid #e63946;
        z-index: 999999;
        box-sizing: border-box;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 1. SAYFA: CANLI BÜLTEN LİSTESİ
# ==========================================
if st.session_state.active_page == "bulten":
    st.markdown("""
    <div style="text-align:center; padding: 6px 0 10px 0;">
        <h3 style="margin:0; color:#0f2438; font-weight:800;">⚽ CANLI BÜLTEN</h3>
        <span style="font-size:0.75rem; color:#64748b;">Detaylı model analizi ve oranlar için maça dokunun</span>
    </div>
    """, unsafe_allow_html=True)

    # Liglere Göre Grupla
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

        st.markdown('<div class="match-row">', unsafe_allow_html=True)
        if st.button(f"⭐  {m['home']}  —  {m['away']}  ➔", key=f"match_{m['id']}"):
            st.session_state.selected_match_id = m["id"]
            st.session_state.active_page = "detay"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 2. SAYFA: DETAYLI MAÇ ANALİZİ VE ORANLAR
# ==========================================
elif st.session_state.active_page == "detay":
    match = next((x for x in matches_db if x["id"] == st.session_state.selected_match_id), matches_db[0])

    # Geri Dön Butonu
    if st.button("⬅ Bültene Geri Dön", key="back_btn"):
        st.session_state.active_page = "bulten"
        st.rerun()

    # Maç Başlığı
    st.markdown(f"""
    <div style="background:#0f2438; color:white; padding:12px; border-radius:10px; text-align:center; margin:6px 0 10px 0;">
        <div style="font-size:0.75rem; color:#94a3b8;">{match['time']}</div>
        <div style="font-size:0.72rem; color:#38bdf8; font-weight:700; text-transform:uppercase;">{match['league']}</div>
        <div style="font-size:1.1rem; font-weight:800; margin-top:2px;">{match['home']} — {match['away']}</div>
    </div>
    """, unsafe_allow_html=True)

    t_oran, t_ist, t_sim = st.tabs(["📌 Oranlar", "📊 Model & xG", "🎲 Simülasyon"])

    with t_oran:
        # HTML Oran Grid Bloğu
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
            body {{ background-color: #f1f5f9; padding: 2px; }}
            .market-header {{
                background: #cfe2f3; color: #0f2438; font-size: 11px; font-weight: 800;
                padding: 5px 8px; border-radius: 5px; margin: 8px 0 4px 0; display: flex; align-items: center;
            }}
            .badge {{ background: #e63946; color: white; font-size: 10px; padding: 1px 4px; border-radius: 3px; margin-right: 5px; font-weight: bold; }}
            .row-card {{
                display: grid; grid-template-columns: 1.4fr 1fr 1fr 1fr; align-items: center;
                background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 5px 6px; margin-bottom: 4px; gap: 4px;
            }}
            .row-card-2 {{
                display: grid; grid-template-columns: 1.4fr 1.5fr 1.5fr; align-items: center;
                background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 5px 6px; margin-bottom: 4px; gap: 5px;
            }}
            .row-title {{ font-size: 12px; font-weight: 700; color: #1e293b; }}
            .btn-box {{
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                background: #1e3a5f; color: #ffffff; border-radius: 6px; padding: 4px 0; min-height: 36px;
                cursor: pointer; user-select: none;
            }}
            .btn-box .label {{ font-size: 9px; color: #94a3b8; font-weight: 600; margin-bottom: 2px; }}
            .btn-box .odd {{ font-size: 12px; font-weight: 800; }}
            .btn-box.selected {{ background: #e63946 !important; color: #ffffff !important; }}
            .btn-box.selected .label {{ color: #ffccd5 !important; }}
        </style>
        </head>
        <body>
            <div class="market-header"><span class="badge">1</span> MAÇ SONUCU</div>
            <div class="row-card">
                <div class="row-title">📌 Maç Sonucu</div>
                <div class="btn-box" onclick="this.classList.toggle('selected')"><span class="label">MS 1</span><span class="odd">{match['ms1']}</span></div>
                <div class="btn-box" onclick="this.classList.toggle('selected')"><span class="label">MS X</span><span class="odd">{match['msx']}</span></div>
                <div class="btn-box" onclick="this.classList.toggle('selected')"><span class="label">MS 2</span><span class="odd">{match['ms2']}</span></div>
            </div>

            <div class="market-header"><span class="badge">1</span> 2.5 ALT / ÜST</div>
            <div class="row-card-2">
                <div class="row-title">📌 2.5 Gol</div>
                <div class="btn-box" onclick="this.classList.toggle('selected')"><span class="label">Alt</span><span class="odd">{match['alt']}</span></div>
                <div class="btn-box" onclick="this.classList.toggle('selected')"><span class="label">Üst</span><span class="odd">{match['ust']}</span></div>
            </div>

            <div class="market-header"><span class="badge">1</span> KARŞILIKLI GOL</div>
            <div class="row-card-2">
                <div class="row-title">📌 KG Var/Yok</div>
                <div class="btn-box" onclick="this.classList.toggle('selected')"><span class="label">Var</span><span class="odd">{match['kg_var']}</span></div>
                <div class="btn-box" onclick="this.classList.toggle('selected')"><span class="label">Yok</span><span class="odd">{match['kg_yok']}</span></div>
            </div>
        </body>
        </html>
        """
        components.html(html_code, height=270, scrolling=False)

    with t_ist:
        st.info(f"🎯 **Model Önerisi:** `{match['ev_pick']}` ({match['ev_val']})")
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
# ALT SABİT KUPON DÜĞMESİ
# ==========================================
st.markdown("""
<div class="bottom-nav">
    <div>
        <span style="font-size:0.75rem; color:#94a3b8;">Kupon Masası</span><br>
        <span style="font-size:1.05rem; font-weight:800; color:#38bdf8;">Oran: 2.34</span>
    </div>
    <div style="background:#e63946; padding:6px 14px; border-radius:6px; font-weight:bold; font-size:0.85rem;">
        Kuponu Kaydet ➔
    </div>
</div>
""", unsafe_allow_html=True)