import streamlit as st
import json

st.set_page_config(
    page_title="Futbol Analiz",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 1. State Yönetimi
if "active_page" not in st.session_state:
    st.session_state.active_page = "bulten"
if "selected_match_id" not in st.session_state:
    st.session_state.selected_match_id = 1
if "my_coupon" not in st.session_state:
    st.session_state.my_coupon = {}
if "show_slip" not in st.session_state:
    st.session_state.show_slip = False

# 2. Bülten Veritabanı
matches_db = [
    {
        "id": 1, "league": "UEFA AVRUPA LİGİ, PLAYOFF", "time": "19:00",
        "home": "J. Bialystok", "away": "Iberia 1999",
        "ms1": 1.23, "msx": 4.44, "ms2": 7.26, "alt": 1.91, "ust": 1.53, "kg_var": 1.70, "kg_yok": 1.85,
        "ev_pick": "2.5 Üst", "ev_val": "%9.2 +EV", "confidence": 76,
        "xg_home": 2.30, "xg_away": 0.65, "mc_1": "%71", "mc_x": "%18", "mc_2": "%11"
    },
    {
        "id": 2, "league": "UEFA AVRUPA LİGİ, PLAYOFF", "time": "19:00",
        "home": "Mjallby", "away": "Salzburg",
        "ms1": 3.82, "msx": 3.63, "ms2": 1.57, "alt": 2.14, "ust": 1.41, "kg_var": 1.50, "kg_yok": 2.10,
        "ev_pick": "MS 2", "ev_val": "%7.8 +EV", "confidence": 72,
        "xg_home": 0.95, "xg_away": 2.10, "mc_1": "%19", "mc_x": "%23", "mc_2": "%58"
    },
    {
        "id": 3, "league": "UEFA KONFERANS LİGİ, PLAYOFF", "time": "20:00",
        "home": "Nordsjælland", "away": "St. Gallen",
        "ms1": 1.37, "msx": 4.36, "ms2": 4.59, "alt": 2.15, "ust": 1.52, "kg_var": 1.48, "kg_yok": 2.10,
        "ev_pick": "MS 1 & 2.5 Üst", "ev_val": "%10.4 +EV", "confidence": 80,
        "xg_home": 2.45, "xg_away": 1.10, "mc_1": "%65", "mc_x": "%20", "mc_2": "%15"
    },
    {
        "id": 4, "league": "PORTEKİZ U23 NEXT GEN LİGİ", "time": "19:00",
        "home": "Benfica U23", "away": "Rio Ave U23",
        "ms1": 1.96, "msx": 3.11, "ms2": 2.64, "alt": 1.84, "ust": 1.51, "kg_var": 1.55, "kg_yok": 2.05,
        "ev_pick": "KG Var", "ev_val": "%6.5 +EV", "confidence": 68,
        "xg_home": 1.60, "xg_away": 1.40, "mc_1": "%42", "mc_x": "%28", "mc_2": "%30"
    }
]

# 3. İstenmeyen Logoları Yok Eden & Ekranı Kilitleyen CSS
st.markdown("""
<style>
    /* Üst menü, alt taç simgesi ve tüm Streamlit logolarını kesin kaldır */
    header, footer, #MainMenu, .stDeployButton, [data-testid="stDecoration"], div[class*="viewerBadge"], [data-testid="stStatusWidget"] {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
    }
    
    html, body, .stApp {
        overflow-x: hidden !important;
        background-color: #f1f5f9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 5.5rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 100% !important;
    }

    /* Lig Bandı */
    .league-banner {
        background: #0f2438;
        color: #e2e8f0;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 6px 10px;
        border-radius: 6px;
        margin-top: 6px;
        margin-bottom: 4px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        text-transform: uppercase;
    }
    .league-title { color: #38bdf8; }

    /* Buton Liste Elemanları */
    div.stButton > button {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        width: 100% !important;
        margin-bottom: 2px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 1. SAYFA: BÜLTEN
# ==========================================
if st.session_state.active_page == "bulten":
    st.markdown("""
    <div style="text-align:center; padding: 2px 0 8px 0;">
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

        if st.button(f"⭐  {m['home']}  —  {m['away']}  ➔", key=f"m_{m['id']}"):
            st.session_state.selected_match_id = m["id"]
            st.session_state.active_page = "detay"
            st.rerun()


# ==========================================
# 2. SAYFA: MAÇ DETAY & KUPONA EKLEME
# ==========================================
elif st.session_state.active_page == "detay":
    match = next((x for x in matches_db if x["id"] == st.session_state.selected_match_id), matches_db[0])
    match_title = f"{match['home']} - {match['away']}"

    c_b1, c_b2 = st.columns([1, 2])
    with c_b1:
        if st.button("⬅ Bülten", key="back_btn"):
            st.session_state.active_page = "bulten"
            st.rerun()

    st.markdown(f"""
    <div style="background:#0f2438; color:white; padding:10px; border-radius:8px; text-align:center; margin:4px 0 8px 0;">
        <div style="font-size:0.75rem; color:#94a3b8;">⏱ {match['time']} • {match['league']}</div>
        <div style="font-size:1.05rem; font-weight:800; margin-top:2px;">{match_title}</div>
    </div>
    """, unsafe_allow_html=True)

    t_oran, t_ist, t_sim = st.tabs(["📌 Oranlar", "📊 Model Analizi", "🎲 Simülasyon"])

    with t_oran:
        # Dinamik Kırmızı Renk Vurgusu
        active_keys = [k for k in st.session_state.my_coupon.keys() if str(match['id']) in k]
        red_css = ""
        for ak in active_keys:
            red_css += f"button[key='{ak}'] {{ background: #e63946 !important; color: white !important; }}\n"
        if red_css:
            st.markdown(f"<style>{red_css}</style>", unsafe_allow_html=True)

        def add_bet(key_name, market, pick, odd):
            if key_name in st.session_state.my_coupon:
                del st.session_state.my_coupon[key_name]
            else:
                st.session_state.my_coupon[key_name] = {
                    "match": match_title,
                    "market": market,
                    "pick": pick,
                    "odd": odd
                }
            st.rerun()

        # MAÇ SONUCU
        st.markdown('<div style="background:#cfe2f3; color:#0f2438; font-size:11px; font-weight:800; padding:4px 8px; border-radius:4px; margin:6px 0;">MAÇ SONUCU</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            k1 = f"b_{match['id']}_ms1"
            if st.button(f"MS 1\n{match['ms1']}", key=k1): add_bet(k1, "Maç Sonucu", "1", match['ms1'])
        with c2:
            kx = f"b_{match['id']}_msx"
            if st.button(f"MS X\n{match['msx']}", key=kx): add_bet(kx, "Maç Sonucu", "X", match['msx'])
        with c3:
            k2 = f"b_{match['id']}_ms2"
            if st.button(f"MS 2\n{match['ms2']}", key=k2): add_bet(k2, "Maç Sonucu", "2", match['ms2'])

        # 2.5 ALT / ÜST
        st.markdown('<div style="background:#cfe2f3; color:#0f2438; font-size:11px; font-weight:800; padding:4px 8px; border-radius:4px; margin:6px 0;">TOPLAM GOL (2.5)</div>', unsafe_allow_html=True)
        ca, cu = st.columns(2)
        with ca:
            ka = f"b_{match['id']}_alt"
            if st.button(f"2.5 Alt\n{match['alt']}", key=ka): add_bet(ka, "2.5 Gol", "Alt", match['alt'])
        with cu:
            ku = f"b_{match['id']}_ust"
            if st.button(f"2.5 Üst\n{match['ust']}", key=ku): add_bet(ku, "2.5 Gol", "Üst", match['ust'])

        # KARŞILIKLI GOL
        st.markdown('<div style="background:#cfe2f3; color:#0f2438; font-size:11px; font-weight:800; padding:4px 8px; border-radius:4px; margin:6px 0;">KARŞILIKLI GOL</div>', unsafe_allow_html=True)
        kv, ky = st.columns(2)
        with kv:
            kv_k = f"b_{match['id']}_kgv"
            if st.button(f"KG Var\n{match['kg_var']}", key=kv_k): add_bet(kv_k, "Karşılıklı Gol", "Var", match['kg_var'])
        with ky:
            ky_k = f"b_{match['id']}_kgy"
            if st.button(f"KG Yok\n{match['kg_yok']}", key=ky_k): add_bet(ky_k, "Karşılıklı Gol", "Yok", match['kg_yok'])

    with t_ist:
        st.info(f"🎯 **Model Önerisi:** `{match['ev_pick']}` ({match['ev_val']})")
        st.metric(f"Beklenen Gol (xG)", f"{match['home']}: {match['xg_home']} — {match['away']}: {match['xg_away']}")
        st.progress(match['confidence'], text=f"Güven Endeksi: %{match['confidence']}")

    with t_sim:
        st.write("🎲 **Monte Carlo 10.000 Maç Simülasyonu:**")
        c1, c2, c3 = st.columns(3)
        c1.metric("1 (Ev)", match['mc_1'])
        c2.metric("X (Ber)", match['mc_x'])
        c3.metric("2 (Dep)", match['mc_2'])


# ==========================================
# 3. KUPON ÇEKMECESİ (NESİNE / İDDAA TARZI)
# ==========================================
coupon_items = list(st.session_state.my_coupon.values())
bet_count = len(coupon_items)
total_odds = 1.0
for it in coupon_items:
    total_odds *= it["odd"]
odds_str = f"{total_odds:.2f}" if bet_count > 0 else "0.00"

st.divider()

# Kupon Başlığı ve Aç/Kapa Butonları
c_k1, c_k2, c_k3 = st.columns([2, 1.2, 1])
with c_k1:
    st.markdown(f"📋 **Kuponum ({bet_count} Maç)** | Oran: **{odds_str}**")
with c_k2:
    if st.button("Kuponu Gör 👁️" if not st.session_state.show_slip else "Gizle ✕", key="btn_slip_toggle"):
        st.session_state.show_slip = not st.session_state.show_slip
        st.rerun()
with c_k3:
    if st.button("Temizle 🗑️", key="btn_clear_all"):
        st.session_state.my_coupon = {}
        st.rerun()

# Kupon Detay Tablosu (Açıldığında Görünür)
if st.session_state.show_slip and bet_count > 0:
    st.markdown("""
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:8px; padding:8px; margin-top:6px;">
    """, unsafe_allow_html=True)
    for idx, b in enumerate(coupon_items):
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; border-bottom:1px solid #e2e8f0; padding:4px 0; font-size:12px;">
            <div>
                <b>{b['match']}</b><br>
                <span style="color:#64748b;">{b['market']} : <b style="color:#0f2438;">{b['pick']}</b></span>
            </div>
            <div style="font-weight:800; color:#e63946; font-size:14px; display:flex; align-items:center;">
                {b['odd']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)