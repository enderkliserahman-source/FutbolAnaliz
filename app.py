import streamlit as st

st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

if "user_preds" not in st.session_state: st.session_state.user_preds = {}
if "revealed" not in st.session_state: st.session_state.revealed = {}
if "cases" not in st.session_state: st.session_state.cases = []

st.markdown("""
<style>
    header, footer, #MainMenu, .stDeployButton, [data-testid="stDecoration"] { display: none !important; }
    .stApp { background: #0f172a; color: #f8fafc; font-family: sans-serif; }
    .block-container { padding-top: 1rem; padding-bottom: 3rem; }
    
    .match-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-left: 4px solid #38bdf8;
        padding: 14px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    .badge-tier1 { background: #0284c7; color: white; padding: 2px 7px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    .badge-tier2 { background: #d97706; color: white; padding: 2px 7px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    .badge-season { background: #64748b; color: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 10px; }
    
    div[data-baseweb="input"] { background-color: #334155 !important; border-radius: 6px; }
    div[data-baseweb="input"] input { color: #ffffff !important; }
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

# 21 AĞUSTOS CUMA BÜLTEN HAVUZU (SADECE POZİTİF GOL MARKETLERİ)
current_pool = [
    {
        "id": 1, "tier": "Tier-1", "time": "21:30", "league": "Almanya Bundesliga",
        "match": "Bayern Münih — RB Leipzig",
        "model_market": "2.5 Üst & KG Var",
        "model_xg": "2.35 - 1.40",
        "confidence": "%78 (Sezon Başı Düzeltmeli)",
        "score_pred": "2-1 / 3-1"
    },
    {
        "id": 2, "tier": "Tier-1", "time": "21:45", "league": "Fransa Ligue 1",
        "match": "PSG — Montpellier",
        "model_market": "Ev Sahibi 1.5 Üst & 2.5 Üst",
        "model_xg": "2.65 - 0.75",
        "confidence": "%80 (Sezon Başı Düzeltmeli)",
        "score_pred": "3-0 / 3-1"
    },
    {
        "id": 3, "tier": "Tier-2", "time": "22:00", "league": "İspanya La Liga",
        "match": "Celta Vigo — Valencia",
        "model_market": "KG Var",
        "model_xg": "1.55 - 1.30",
        "confidence": "%68 (Sezon Başı Düzeltmeli)",
        "score_pred": "1-1 / 2-1"
    },
    {
        "id": 4, "tier": "Tier-2", "time": "21:00", "league": "Hollanda Eredivisie",
        "match": "NEC Nijmegen — PEC Zwolle",
        "model_market": "2.5 Üst",
        "model_xg": "1.80 - 1.25",
        "confidence": "%71 (Sezon Başı Düzeltmeli)",
        "score_pred": "2-1 / 2-2"
    }
]

tab1, tab2 = st.tabs(["🎯 İstişare Masası (21 Ağustos)", "🔬 Vaka Analizi (Arşiv)"])

with tab1:
    st.markdown("### 📋 Günün Gol Odaklı Bülteni")
    st.caption("Kural: Önce kendi bağımsız tahminini gir ve kaydet. Ardından model raporunu aç.")

    for m in current_pool:
        m_id = m["id"]
        t_class = "badge-tier1" if m["tier"] == "Tier-1" else "badge-tier2"
        
        st.markdown(f"""
        <div class="match-card">
            <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                <div>
                    <span class="{t_class}">{m['tier']}</span>
                    <span class="badge-season">Ağustos Filtresi Aktif</span>
                </div>
                <span style="color:#94a3b8; font-size:12px;">{m['time']} • {m['league']}</span>
            </div>
            <h3 style="margin:0; color:#ffffff;">{m['match']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Kullanıcı Bağımsız Tahmin Alanı
        user_val = st.text_input(
            "Senin Bağımsız Analizin / Tercihin:",
            key=f"in_{m_id}",
            value=st.session_state.user_preds.get(m_id, ""),
            placeholder="Örn: KG Var, 2.5 Üst, Ev 1.5 Üst"
        )
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Tahminimi Kitle 🔒", key=f"save_{m_id}"):
                st.session_state.user_preds[m_id] = user_val
                st.toast(f"{m['match']} tahminin kilitlendi!")
        with c2:
            if st.button("Model Raporunu Aç 📊", key=f"rev_{m_id}"):
                st.session_state.revealed[m_id] = True

        # Model Raporu
        if st.session_state.revealed.get(m_id, False):
            st.markdown(f"""
            <div style="background:#0f172a; border:1px solid #334155; padding:10px; border-radius:6px; margin-top:8px;">
                <b>🤖 Model Önerisi:</b> <span style="color:#38bdf8;">{m['model_market']}</span><br>
                <small style="color:#94a3b8;">xG Projeksiyonu: {m['model_xg']} | Güven: {m['confidence']} | Skor: {m['score_pred']}</small>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.user_preds.get(m_id):
                user_text = st.session_state.user_preds[m_id].strip().lower()
                model_text = m['model_market'].strip().lower()
                is_match = user_text in model_text or model_text in user_text
                
                status_color = "#22c55e" if is_match else "#eab308"
                status_label = "Tam Konsensüs (Ortak Görüş)" if is_match else "Ayrışma / İstişare Gerekli"
                
                st.markdown(f"""
                <div style="margin-top:6px; padding:6px 10px; border-radius:4px; background:{status_color}22; border-left:3px solid {status_color};">
                    <span style="color:{status_color}; font-weight:bold;">{status_label}</span><br>
                    <small>Sen: <b>{st.session_state.user_preds[m_id]}</b> | Model: <b>{m['model_market']}</b></small>
                </div>
                """, unsafe_allow_html=True)

        st.divider()

with tab2:
    st.markdown("### 📚 Vaka Analizi & Öğrenen Sistem")
    
    col_a, col_b = st.columns(2)
    with col_a:
        v_match = st.text_input("Maç Adı:", placeholder="Örn: Bayern - Leipzig")
        v_source = st.selectbox("Kaynak:", ["İnsan Sezgisi", "Model Sinyali", "Ortak Konsensüs"])
    with col_b:
        v_res = st.selectbox("Sonuç:", ["Başarılı", "Başarısız"])
        v_note = st.text_area("Taktiksel Not:", placeholder="Örn: Erken gol tempoyu artırdı, model xG projeksiyonu tam oturdu.")

    if st.button("Vakayı Sisteme Kaydet 💾"):
        if v_match:
            st.session_state.cases.append({"match": v_match, "source": v_source, "res": v_res, "note": v_note})
            st.success("Vaka arşivlendi!")

    st.markdown("---")
    st.markdown("#### 🗄️ Sistem Hafızası")
    if not st.session_state.cases:
        st.info("Kayıtlı vaka bulunmuyor.")
    else:
        for c in reversed(st.session_state.cases):
            color = "#22c55e" if c['res'] == "Başarılı" else "#ef4444"
            st.markdown(f"""
            <div style="background:#1e293b; border-left:4px solid {color}; padding:8px 12px; border-radius:6px; margin-bottom:8px;">
                <b>{c['match']}</b> — <span style="color:{color}; font-weight:bold;">{c['res']}</span> ({c['source']})<br>
                <small style="color:#cbd5e1;">{c['note']}</small>
            </div>
            """, unsafe_allow_html=True)