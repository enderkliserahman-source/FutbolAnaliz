import streamlit as st

st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

if "my_coupon" not in st.session_state: st.session_state.my_coupon = {}
if "active_page" not in st.session_state: st.session_state.active_page = "bulten"

# KESİN CSS: Tüm elementleri mobilde tek satırda tutan CSS
st.markdown("""
<style>
    /* 1. Tüm Streamlit elementlerini gizle */
    header, footer, #MainMenu, .stDeployButton, [data-testid="stDecoration"] { display: none !important; }
    
    /* 2. Ekranı tamamen sabitle */
    html, body, .stApp { overflow-x: hidden !important; background: #f1f5f9; }
    
    /* 3. Butonları yan yana kilitleyen CSS - Burası Kritik! */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* Asla alt alta atma */
        gap: 2px !important;
    }
    div[data-testid="column"] {
        flex: 1 1 0% !important;
        min-width: 0 !important;
    }
    
    /* 4. Butonları Nesine Tarzı Yap */
    div.stButton > button {
        background: #1e3a5f !important; color: white !important;
        border: none !important; border-radius: 4px !important;
        font-weight: 700 !important; font-size: 0.75rem !important;
        padding: 5px 2px !important; width: 100% !important;
        line-height: 1.1 !important;
    }
    
    /* 5. Kupon Kartı */
    .slip-box {
        background: white; border-radius: 10px; padding: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Bülten Verisi
matches_db = [
    {"id": 1, "league": "AVRUPA LİGİ", "home": "Mjallby", "away": "Salzburg", "ms1": 3.8, "msx": 3.6, "ms2": 1.5, "ust": 1.4, "kg": 1.5},
    {"id": 2, "league": "KONFERANS LİGİ", "home": "Nordsjaelland", "away": "St. Gallen", "ms1": 1.3, "msx": 4.3, "ms2": 4.5, "ust": 1.5, "kg": 1.4}
]

def add_bet(m_id, m_name, market, pick, odd):
    key = f"{m_id}_{market}"
    st.session_state.my_coupon[key] = {"match": m_name, "market": market, "pick": pick, "odd": odd}

# BÜLTEN EKRANI
if st.session_state.active_page == "bulten":
    st.markdown("<h3 style='text-align:center;'>⚽ GÜNÜN BÜLTENİ</h3>", unsafe_allow_html=True)
    for m in matches_db:
        st.markdown(f"<div style='background:#0f2438; color:white; padding:8px; border-radius:5px; margin-top:10px; font-weight:bold;'>{m['league']} | {m['home']} - {m['away']}</div>", unsafe_allow_html=True)
        # ORAN GRID (Sabit 5li)
        c1,c2,c3,c4,c5 = st.columns(5)
        if c1.button(f"1\n{m['ms1']}", key=f"b_{m['id']}_1"): add_bet(m['id'], f"{m['home']}-{m['away']}", "MS", "1", m['ms1'])
        if c2.button(f"X\n{m['msx']}", key=f"b_{m['id']}_X"): add_bet(m['id'], f"{m['home']}-{m['away']}", "MS", "X", m['msx'])
        if c3.button(f"2\n{m['ms2']}", key=f"b_{m['id']}_2"): add_bet(m['id'], f"{m['home']}-{m['away']}", "MS", "2", m['ms2'])
        if c4.button(f"Üst\n{m['ust']}", key=f"b_{m['id']}_U"): add_bet(m['id'], f"{m['home']}-{m['away']}", "Gol", "Üst", m['ust'])
        if c5.button(f"KG\n{m['kg']}", key=f"b_{m['id']}_K"): add_bet(m['id'], f"{m['home']}-{m['away']}", "KG", "Var", m['kg'])

# KUPON BÖLÜMÜ (Sabit Alt)
total_odd = 1.0
if st.session_state.my_coupon:
    st.markdown("---")
    st.markdown("### 📋 KUPONUM")
    for k, v in st.session_state.my_coupon.items():
        total_odd *= v['odd']
        col1, col2 = st.columns([3, 1])
        col1.write(f"{v['match']} -> {v['pick']}")
        if col2.button("Sil", key=f"del_{k}"):
            del st.session_state.my_coupon[k]
            st.rerun()
    st.subheader(f"Toplam Oran: {total_odd:.2f}")