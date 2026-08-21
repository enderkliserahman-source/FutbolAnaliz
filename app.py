import streamlit as st
from datetime import datetime

st.set_page_config(layout="centered", initial_sidebar_state="collapsed", page_title="Futbol İstişare & Analiz Masası")

# Session State
if "user_preds" not in st.session_state: st.session_state.user_preds = {}
if "user_odds" not in st.session_state: st.session_state.user_odds = {}
if "revealed" not in st.session_state: st.session_state.revealed = {}
if "chat_logs" not in st.session_state: st.session_state.chat_logs = {}
if "live_stats" not in st.session_state: st.session_state.live_stats = {}
if "cases" not in st.session_state: st.session_state.cases = []

st.markdown("""
<style>
    /* Üst ve Alt Boşluklar / Genel Ayarlar */
    header, footer, #MainMenu, .stDeployButton, [data-testid="stDecoration"] { display: none !important; }
    .stApp { background-color: #111827 !important; color: #f9fafb !important; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .block-container { padding-top: 0.8rem; padding-bottom: 3rem; }
    
    /* Üst Sekmeler / Buton Menü Tasarımı */
    button[data-baseweb="tab"] {
        background-color: #1f2937 !important;
        color: #cbd5e1 !important;
        border-radius: 8px 8px 0px 0px !important;
        padding: 10px 16px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        border: 1px solid #374151 !important;
        border-bottom: none !important;
        margin-right: 6px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border-color: #3b82f6 !important;
    }
    div[data-testid="stTabs"] {
        border-bottom: 2px solid #2563eb !important;
        margin-bottom: 16px !important;
    }

    /* Maç Kartları */
    .match-card {
        background-color: #1f2937;
        border: 1px solid #374151;
        border-left: 5px solid #38bdf8;
        padding: 14px;
        border-radius: 10px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .badge-session { background: #3b82f6; color: #ffffff; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: bold; }
    .badge-tier { background: #0284c7; color: #ffffff; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }
    
    /* Form Alanları ve Etiketler */
    label p { color: #f3f4f6 !important; font-weight: 600 !important; font-size: 13px !important; }
    div[data-baseweb="select"] { background-color: #374151 !important; border-radius: 8px; border: 1px solid #4b5563 !important; }
    div[data-baseweb="select"] * { color: #ffffff !important; font-weight: 500; }
    div[data-baseweb="input"] { background-color: #374151 !important; border-radius: 8px; border: 1px solid #4b5563 !important; }
    div[data-baseweb="input"] input { color: #ffffff !important; font-size: 14px; }
    
    /* Butonlar */
    div.stButton > button {
        background: #2563eb !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        width: 100% !important;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        background: #1d4ed8 !important;
    }

    /* Expander Başlığı */
    .streamlit-expanderHeader {
        background-color: #1f2937 !important;
        color: #f3f4f6 !important;
        border-radius: 8px !important;
        border: 1px solid #374151 !important;
        font-weight: 600 !important;
    }

    /* Sohbet Baloncukları */
    .chat-bubble-user {
        background: #1e3a8a;
        padding: 8px 12px;
        border-radius: 8px 8px 0px 8px;
        margin-bottom: 6px;
        font-size: 13px;
        border: 1px solid #3b82f6;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# HAZIR MARKET SEÇENEKLERİ
PRESET_OPTIONS = [
    "Seçim Yapılmadı",
    "Ev Sahibi 1.5 Üst",
    "Deplasman 1.5 Üst",
    "2.5 Üst",
    "KG Var",
    "2.5 Üst & KG Var",
    "MS 1 & 1.5 Üst",
    "MS 2 & 1.5 Üst",
    "Ev Sahibi 2.5 Üst"
]

# 21 AĞUSTOS 2026 - BÜLTEN HAVUZU
matches = [
    # GÜNDÜZ SEANSI
    {
        "id": 1, "session": "Gündüz Seansı", "time": "13:00", "league": "Japonya J-League",
        "match": "Kashiwa Reysol — V-Varen Nagasaki",
        "model_market": "Ev Sahibi 1.5 Üst", "model_xg": "1.92 - 0.85",
        "confidence": "%76", "score_pred": "2-0 / 2-1"
    },
    {
        "id": 2, "session": "Gündüz Seansı", "time": "13:30", "league": "Japonya J-League",
        "match": "FC Tokyo — JEF United Chiba",
        "model_market": "2.5 Üst & KG Var", "model_xg": "1.68 - 1.15",
        "confidence": "%72", "score_pred": "2-1 / 1-2"
    },
    # AKŞAM ERKEN SEANS
    {
        "id": 3, "session": "Akşam Erken Seans", "time": "20:30", "league": "Avusturya Bundesliga",
        "match": "SV Ried — Grazer AK",
        "model_market": "2.5 Üst & KG Var", "model_xg": "1.75 - 1.35",
        "confidence": "%70", "score_pred": "2-1 / 2-2"
    },
    {
        "id": 4, "session": "Akşam Erken Seans", "time": "21:30", "league": "Trendyol Süper Lig",
        "match": "Erzurumspor — Galatasaray",
        "model_market": "Deplasman 1.5 Üst & MS 2", "model_xg": "0.65 - 2.10",
        "confidence": "%78", "score_pred": "0-2 / 1-3"
    },
    {
        "id": 5, "session": "Akşam Erken Seans", "time": "21:30", "league": "Trendyol 1. Lig",
        "match": "Fatih Karagümrük — Bursaspor",
        "model_market": "Ev Sahibi 1.5 Üst & KG Var", "model_xg": "1.80 - 1.20",
        "confidence": "%69", "score_pred": "2-1"
    },
    # GECE ANA SEANSI
    {
        "id": 6, "session": "Gece Ana Seansı", "time": "21:45", "league": "Fransa Ligue 1",
        "match": "Marsilya — Strasbourg",
        "model_market": "Ev Sahibi 1.5 Üst & 2.5 Üst", "model_xg": "2.30 - 0.90",
        "confidence": "%75", "score_pred": "2-1 / 3-1"
    },
    {
        "id": 7, "session": "Gece Ana Seansı", "time": "21:45", "league": "Belçika Pro League",
        "match": "Standard Liège — La Louvière",
        "model_market": "Ev Sahibi 1.5 Üst & MS 1", "model_xg": "2.05 - 0.70",
        "confidence": "%74", "score_pred": "2-0 / 3-0"
    },
    {
        "id": 8, "session": "Gece Ana Seansı", "time": "22:00", "league": "İngiltere Kupası",
        "match": "Arsenal — Coventry",
        "model_market": "Ev Sahibi 2.5 Üst", "model_xg": "2.85 - 0.40",
        "confidence": "%84", "score_pred": "3-0 / 4-0"
    },
    {
        "id": 9, "session": "Gece Ana Seansı", "time": "22:00", "league": "İspanya La Liga",
        "match": "Real Betis — Real Sociedad",
        "model_market": "KG Var", "model_xg": "1.45 - 1.30",
        "confidence": "%67", "score_pred": "1-1 / 2-1"
    }
]

tab1, tab2 = st.tabs(["🎯 Canlı İstişare Masası", "🔬 Vaka Analizi & Öğrenme"])

with tab1:
    st.markdown("### 📋 Günün Bülteni & Canlı İstişare")
    st.markdown("<p style='color:#94a3b8; font-size:13px;'>🔒 <b>Kural:</b> Tercihini ve oranını kilitle, ardından model raporunu açıp maç altındaki canlı sohbetle tartış.</p>", unsafe_allow_html=True)

    current_session = ""
    for m in matches:
        m_id = m["id"]
        
        if m["session"] != current_session:
            current_session = m["session"]
            st.markdown(f"<div style='margin-top:22px; margin-bottom:10px;'><span class='badge-session'>{current_session}</span></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="match-card">
            <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                <span class="badge-tier">{m['league']}</span>
                <span style="color:#cbd5e1; font-size:12px; font-weight:600;">{m['time']}</span>
            </div>
            <h3 style="margin:2px 0 0 0; color:#ffffff; font-size:17px;">{m['match']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # 1. Tahmin ve Oran Seçimi
        col_sel, col_odd = st.columns([2, 1])
        with col_sel:
            current_choice = st.session_state.user_preds.get(m_id, "Seçim Yapılmadı")
            idx = PRESET_OPTIONS.index(current_choice) if current_choice in PRESET_OPTIONS else 0
            user_choice = st.selectbox("Tahminin:", PRESET_OPTIONS, index=idx, key=f"sel_{m_id}")
        with col_odd:
            user_odd = st.number_input("İddaa Oranı:", min_value=1.00, max_value=20.00, value=st.session_state.user_odds.get(m_id, 1.50), step=0.05, key=f"odd_{m_id}")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Tahminimi Kilitle 🔒", key=f"save_{m_id}"):
                st.session_state.user_preds[m_id] = user_choice
                st.session_state.user_odds[m_id] = user_odd
                st.toast(f"{m['match']} ({user_choice} @ {user_odd}) kilitlendi!")
        with c2:
            if st.button("Model Raporunu Aç 📊", key=f"rev_{m_id}"):
                st.session_state.revealed[m_id] = True

        # Model Raporu Alanı
        if st.session_state.revealed.get(m_id, False):
            st.markdown(f"""
            <div style="background:#111827; border:1px solid #374151; padding:12px; border-radius:8px; margin-top:8px;">
                <b style="color:#ffffff;">🤖 Model Sinyali:</b> <span style="color:#38bdf8; font-weight:bold; font-size:15px;">{m['model_market']}</span><br>
                <div style="color:#cbd5e1; font-size:12px; margin-top:4px;">
                    <b>xG Projeksiyonu:</b> {m['model_xg']} &nbsp;|&nbsp; <b>Güven:</b> {m['confidence']} &nbsp;|&nbsp; <b>Skor:</b> {m['score_pred']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            saved_choice = st.session_state.user_preds.get(m_id, "Seçim Yapılmadı")
            if saved_choice != "Seçim Yapılmadı":
                u_text = saved_choice.strip().lower()
                m_text = m['model_market'].strip().lower()
                is_match = u_text in m_text or m_text in u_text
                
                status_color = "#22c55e" if is_match else "#eab308"
                status_label = "🟢 Tam Mutabakat (Ortak Karar)" if is_match else "🟡 Ayrışma / İstişare Masası"
                
                st.markdown(f"""
                <div style="margin-top:8px; padding:8px 12px; border-radius:6px; background:{status_color}1a; border-left:4px solid {status_color};">
                    <span style="color:{status_color}; font-weight:bold; font-size:13px;">{status_label}</span><br>
                    <small style="color:#f3f4f6;">Sen: <b>{saved_choice} (@{st.session_state.user_odds.get(m_id, '-')})</b> &nbsp;|&nbsp; Model: <b>{m['model_market']}</b></small>
                </div>
                """, unsafe_allow_html=True)

        # 2. Canlı Maçkolik & Saha İstatistik Paneli
        with st.expander("📊 Canlı Saha & İstatistik Masası (Mackolik Girişi)"):
            c_stat1, c_stat2, c_stat3 = st.columns(3)
            with c_stat1:
                st.text_input("Dakika:", key=f"min_{m_id}", placeholder="Örn: 34'")
            with c_stat2:
                st.text_input("Canlı Skor:", key=f"score_{m_id}", placeholder="Örn: 1-0")
            with c_stat3:
                st.text_input("Topla Oynama (%):", key=f"poss_{m_id}", placeholder="Örn: 58 - 42")
            
            c_xg1, c_xg2 = st.columns(2)
            with c_xg1:
                st.number_input("Ev Canlı xG:", min_value=0.0, max_value=10.0, step=0.05, key=f"xgh_{m_id}")
            with c_xg2:
                st.number_input("Dep Canlı xG:", min_value=0.0, max_value=10.0, step=0.05, key=f"xga_{m_id}")

        # 3. Maça Özel Canlı Sohbet
        with st.expander("💬 Bu Maç İçin Canlı Tartışma / Sohbet"):
            if m_id not in st.session_state.chat_logs:
                st.session_state.chat_logs[m_id] = []
            
            for chat in st.session_state.chat_logs[m_id]:
                st.markdown(f"""
                <div class="chat-bubble-user">
                    <b>Sen ({chat['time']}):</b> {chat['msg']}
                </div>
                """, unsafe_allow_html=True)
            
            col_msg, col_send = st.columns([3, 1])
            with col_msg:
                user_msg = st.text_input("Taktiksel Görüşünü Yaz:", key=f"chat_in_{m_id}", placeholder="Örn: Baskı çok arttı, gol an meselesi...")
            with col_send:
                if st.button("Gönder 💬", key=f"send_chat_{m_id}"):
                    if user_msg.strip():
                        now_str = datetime.now().strftime("%H:%M")
                        st.session_state.chat_logs[m_id].append({"time": now_str, "msg": user_msg})
                        st.rerun()

        st.divider()

with tab2:
    st.markdown("### 📚 Biten Maç Vaka Analizi")
    st.markdown("<p style='color:#94a3b8; font-size:13px;'>Biten maçların sonucunu ve taktiksel nedenlerini kaydederek model hafızasını besle.</p>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        v_match = st.selectbox("Maç Seç:", [m["match"] for m in matches])
        v_source = st.selectbox("Tercih Kaynağı:", ["İnsan Sezgisi", "Model Sinyali", "Ortak Konsensüs"])
    with col_b:
        v_res = st.selectbox("Sonuç:", ["Başarılı", "Başarısız"])
        v_note = st.text_area("Taktiksel Çıkarım / Not:", placeholder="Örn: Erken gol tempoyu artırdı...")

    if st.button("Vakayı Sisteme Kaydet 💾"):
        if v_match:
            st.session_state.cases.append({"match": v_match, "source": v_source, "res": v_res, "note": v_note})
            st.success("Vaka hafızaya işlendi!")

    st.markdown("---")
    st.markdown("#### 🗄️ Sistem Hafıza Kayıtları")
    if not st.session_state.cases:
        st.info("Henüz vaka kaydı girilmedi.")
    else:
        for c in reversed(st.session_state.cases):
            color = "#22c55e" if c['res'] == "Başarılı" else "#ef4444"
            st.markdown(f"""
            <div style="background:#1f2937; border-left:4px solid {color}; padding:10px 14px; border-radius:6px; margin-bottom:8px; border-top:1px solid #374151; border-right:1px solid #374151; border-bottom:1px solid #374151;">
                <b style="color:#ffffff;">{c['match']}</b> — <span style="color:{color}; font-weight:bold;">{c['res']}</span> <span style="color:#94a3b8;">({c['source']})</span><br>
                <small style="color:#cbd5e1; display:inline-block; margin-top:4px;">{c['note']}</small>
            </div>
            """, unsafe_allow_html=True)