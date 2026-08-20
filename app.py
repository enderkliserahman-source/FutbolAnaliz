import streamlit as st

st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

if "user_preds" not in st.session_state: st.session_state.user_preds = {}
if "revealed" not in st.session_state: st.session_state.revealed = {}
if "cases" not in st.session_state: st.session_state.cases = []

# Şık ve Butonları Net Okunan Tema
st.markdown("""
<style>
    header, footer, #MainMenu, .stDeployButton, [data-testid="stDecoration"] { display: none !important; }
    .stApp { background: #0f172a; color: #f8fafc; font-family: sans-serif; }
    .block-container { padding-top: 1rem; padding-bottom: 3rem; }
    
    .match-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-left: 4px solid #38bdf8;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    .badge-tier1 { background: #0284c7; color: white; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    .badge-tier2 { background: #d97706; color: white; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    
    /* Input ve Buton Renk Düzeltmeleri */
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

# 1. Havuz (Sadece gerçek bülten için boş şablon veya test maçları)
current_pool = [
    {
        "id": 1, "tier": "Tier-1", "match": "Nordsjælland - St. Gallen",
        "model_report": "Öneri: MS 1 & 2.5 Üst | xG: 2.45 - 1.10 | Güven: %74 | Beklenen Skor: 2-1"
    },
    {
        "id": 2, "tier": "Tier-1", "match": "Lech Poznan - Thun",
        "model_report": "Öneri: MS 1 & 1.5 Üst | xG: 2.10 - 0.85 | Güven: %70 | Beklenen Skor: 2-0 / 3-1"
    },
    {
        "id": 3, "tier": "Tier-2", "match": "Brann - Arouca",
        "model_report": "Öneri: KG Var | xG: 1.65 - 1.40 | Güven: %66 | Beklenen Skor: 1-1 / 2-1"
    },
    {
        "id": 4, "tier": "Tier-2", "match": "Gent - Silkeborg",
        "model_report": "Öneri: 2.5 Üst | xG: 2.20 - 1.30 | Güven: %72 | Beklenen Skor: 2-1 / 3-1"
    }
]

tab1, tab2 = st.tabs(["🎯 İstişare Masası", "🔬 Vaka Analizi (Arşiv)"])

# ==========================================
# TAB 1: KÖR TAHMİN & MODEL İSTİŞARESİ
# ==========================================
with tab1:
    st.markdown("### 📋 Günün Seçilmiş Maç Havuzu")
    st.caption("Önce kendi taktiksel tahminini gir, ardından modelin raporunu aç ve karşılaştır.")

    for m in current_pool:
        m_id = m["id"]
        t_class = "badge-tier1" if m["tier"] == "Tier-1" else "badge-tier2"
        
        st.markdown(f"""
        <div class="match-card">
            <span class="{t_class}">{m['tier']}</span>
            <h4 style="margin: 6px 0 0 0; color:#ffffff;">{m['match']}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Kullanıcı Tahmin Alanı
        user_val = st.text_input(f"Senin Analizin / Tahminin:", key=f"in_{m_id}", value=st.session_state.user_preds.get(m_id, ""), placeholder="Örn: 2.5 Üst veya MS 1")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Tahminimi Kaydet 💾", key=f"save_{m_id}"):
                st.session_state.user_preds[m_id] = user_val
                st.toast("Tahminin kaydedildi!")
        with c2:
            if st.button("Model Raporunu Aç 🤖", key=f"rev_{m_id}"):
                st.session_state.revealed[m_id] = True

        # Model Raporu Sadece Butona Basılınca Açılır
        if st.session_state.revealed.get(m_id, False):
            st.info(f"📊 **Model Çıktısı:** {m['model_report']}")
            if st.session_state.user_preds.get(m_id):
                st.success(f"🤝 **Karşılaştırma:** Sen: `{st.session_state.user_preds[m_id]}` | Model: `{m['model_report'].split('|')[0]}`")

        st.divider()

# ==========================================
# TAB 2: VAKA ANALİZİ (ÖĞRENEN SİSTEM)
# ==========================================
with tab2:
    st.markdown("### 📚 Biten Maç Vaka Analizi")
    
    col_a, col_b = st.columns(2)
    with col_a:
        v_match = st.text_input("Maç Adı:", placeholder="Örn: Inter Turku - Kopenhag")
        v_source = st.selectbox("Tahmin Kaynağı:", ["İnsan Sezgisi", "Model Sinyali", "Ortak Konsensüs"])
    with col_b:
        v_res = st.selectbox("Sonuç:", ["Başarısız", "Başarılı", "Kısmi"])
        v_note = st.text_area("Analist Notu (Neden tuttu / yattı?):", placeholder="Örn: Kopenhag ceza sahasına girdi ama bitiricilik zayıftı...")

    if st.button("Vakayı Arşive Kaydet 📌"):
        if v_match:
            st.session_state.cases.append({"match": v_match, "source": v_source, "res": v_res, "note": v_note})
            st.success("Vaka arşive işlendi!")

    st.markdown("---")
    st.markdown("#### 🗄️ Geçmiş Dersler")
    for c in reversed(st.session_state.cases):
        color = "#22c55e" if c['res'] == "Başarılı" else "#ef4444"
        st.markdown(f"""
        <div style="background:#1e293b; border-left:4px solid {color}; padding:8px 12px; border-radius:6px; margin-bottom:8px;">
            <b>{c['match']}</b> — <span style="color:{color}; font-weight:bold;">{c['res']}</span> ({c['source']})<br>
            <small style="color:#cbd5e1;">{c['note']}</small>
        </div>
        """, unsafe_allow_html=True)
