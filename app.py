import streamlit as st

st.set_page_config(layout="centered", initial_sidebar_state="collapsed", page_title="Futbol Analiz Masası")

if "user_preds" not in st.session_state: st.session_state.user_preds = {}
if "revealed" not in st.session_state: st.session_state.revealed = {}
if "cases" not in st.session_state: st.session_state.cases = []

st.markdown("""
<style>
    header, footer, #MainMenu, .stDeployButton, [data-testid="stDecoration"] { display: none !important; }
    .stApp { background: #0f172a; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .block-container { padding-top: 1rem; padding-bottom: 3rem; }
    
    .match-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-left: 4px solid #38bdf8;
        padding: 12px 14px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .badge-session { background: #3b82f6; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    .badge-tier { background: #0284c7; color: white; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: 600; }
    
    div[data-baseweb="input"] { background-color: #334155 !important; border-radius: 6px; }
    div[data-baseweb="input"] input { color: #ffffff !important; font-size: 14px; }
    div.stButton > button {
        background: #2563eb !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 6px !important;
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# 21 AĞUSTOS 2026 - SENİN SEÇTİĞİN BÜLTEN LİSTESİ
matches = [
    # GÜNDÜZ SEANSI
    {
        "id": 1, "session": "Gündüz Seansı", "time": "13:00", "league": "Japonya J-League",
        "match": "Kashiwa Reysol — V-Varen Nagasaki",
        "model_market": "Ev Sahibi 1.5 Üst & MS 1", "model_xg": "1.92 - 0.85",
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
        "id": 8, "session": "Gece Ana Seansı", "time": "22:00", "league": "İngiltere FA Cup / Lig Kupası",
        "match": "Arsenal — Coventry",
        "model_market": "Ev Sahibi 2.5 Üst (Tek Başına)", "model_xg": "2.85 - 0.40",
        "confidence": "%84", "score_pred": "3-0 / 4-0"
    },
    {
        "id": 9, "session": "Gece Ana Seansı", "time": "22:00", "league": "İspanya La Liga",
        "match": "Real Betis — Real Sociedad",
        "model_market": "KG Var (Karşılıklı Gol)", "model_xg": "1.45 - 1.30",
        "confidence": "%67", "score_pred": "1-1 / 2-1"
    }
]

tab1, tab2 = st.tabs(["🎯 Canlı İstişare Masası", "🔬 Vaka Analizi & Öğrenme"])

with tab1:
    st.markdown("### 📋 Günün Seçilmiş Maç Havuzu")
    st.caption("🔒 Kural: Önce kendi tahminini yaz ve kilitle. Ardından model raporunu açıp mutabakatı kontrol et.")

    current_session = ""
    for m in matches:
        m_id = m["id"]
        
        # Seans Başlığı
        if m["session"] != current_session:
            current_session = m["session"]
            st.markdown(f"<div style='margin-top:18px; margin-bottom:8px;'><span class='badge-session'>{current_session}</span></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="match-card">
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span class="badge-tier">{m['league']}</span>
                <span style="color:#94a3b8; font-size:12px;">{m['time']}</span>
            </div>
            <h4 style="margin:2px 0 0 0; color:#ffffff;">{m['match']}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Kullanıcı Tahmin Alanı
        user_val = st.text_input(
            "Senin Tahminin / Görüşün:",
            key=f"in_{m_id}",
            value=st.session_state.user_preds.get(m_id, ""),
            placeholder="Örn: Ev 1.5 Üst, 2.5 Üst & KG Var"
        )
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Tahminimi Kilitle 🔒", key=f"save_{m_id}"):
                st.session_state.user_preds[m_id] = user_val
                st.toast(f"{m['match']} tahminin kilitlendi!")
        with c2:
            if st.button("Model Raporunu Aç 📊", key=f"rev_{m_id}"):
                st.session_state.revealed[m_id] = True

        # Model Raporu (Sadece butona basınca)
        if st.session_state.revealed.get(m_id, False):
            st.markdown(f"""
            <div style="background:#0f172a; border:1px solid #334155; padding:10px; border-radius:6px; margin-top:8px;">
                <b>🤖 Model Sinyali:</b> <span style="color:#38bdf8; font-weight:bold;">{m['model_market']}</span><br>
                <small style="color:#94a3b8;">xG: {m['model_xg']} | Güven: {m['confidence']} | Skor Projeksiyonu: {m['score_pred']}</small>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.user_preds.get(m_id):
                u_text = st.session_state.user_preds[m_id].strip().lower()
                m_text = m['model_market'].strip().lower()
                is_match = u_text in m_text or m_text in u_text
                
                status_color = "#22c55e" if is_match else "#eab308"
                status_label = "🟢 Tam Mutabakat" if is_match else "🟡 Ayrışma / İstişare Gerekli"
                
                st.markdown(f"""
                <div style="margin-top:6px; padding:6px 10px; border-radius:4px; background:{status_color}18; border-left:3px solid {status_color};">
                    <span style="color:{status_color}; font-weight:bold; font-size:12px;">{status_label}</span><br>
                    <small>Sen: <b>{st.session_state.user_preds[m_id]}</b> | Model: <b>{m['model_market']}</b></small>
                </div>
                """, unsafe_allow_html=True)

        st.divider()

with tab2:
    st.markdown("### 📚 Biten Maç Vaka Analizi")
    st.caption("Biten maçların sonucunu ve taktiksel nedenlerini kaydederek model hafızasını besle.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        v_match = st.selectbox("Maç Seç:", [m["match"] for m in matches])
        v_source = st.selectbox("Tercih Kaynağı:", ["İnsan Sezgisi", "Model Sinyali", "Ortak Konsensüs"])
    with col_b:
        v_res = st.selectbox("Sonuç:", ["Başarılı", "Başarısız"])
        v_note = st.text_area("Taktiksel Çıkarım / Not:", placeholder="Örn: Erken gol tempoyu artırdı, deplasman direnci düştü...")

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
            <div style="background:#1e293b; border-left:4px solid {color}; padding:8px 12px; border-radius:6px; margin-bottom:8px;">
                <b>{c['match']}</b> — <span style="color:{color}; font-weight:bold;">{c['res']}</span> ({c['source']})<br>
                <small style="color:#cbd5e1;">{c['note']}</small>
            </div>
            """, unsafe_allow_html=True)