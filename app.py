import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

if "user_preds" not in st.session_state: st.session_state.user_preds = {}
if "cases" not in st.session_state: st.session_state.cases = []

st.markdown("""
<style>
    .stApp { background: #0f172a; color: #f8fafc; font-family: sans-serif; }
    .lab-card { background: #1e293b; border-left: 4px solid #38bdf8; padding: 12px; margin-bottom: 10px; border-radius: 6px; }
    .btn-save { background: #0ea5e9 !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# Sabit Bülten Havuzu (Örnek)
current_pool = [
    {"id": 1, "tier": "Tier-1", "match": "Mjallby - Salzburg", "model": "MS 2"},
    {"id": 2, "tier": "Tier-1", "match": "Inter Turku - Kopenhag", "model": "2.5 Üst"},
    {"id": 3, "tier": "Tier-2", "match": "Lincoln Red - Larne FC", "model": "KG Var"}
]

tab1, tab2 = st.tabs(["⚡ Canlı İstişare & Tahmin", "🔬 Vaka Analizi (Arşiv)"])

with tab1:
    st.subheader("🎯 İstişare Masası")
    for m in current_pool:
        with st.container():
            st.markdown(f'<div class="lab-card"><b>{m["match"]}</b><br>Model Önerisi: {m["model"]}</div>', unsafe_allow_html=True)
            
            # Manuel Giriş Alanı
            pred_key = f"input_{m['id']}"
            user_input = st.text_input("Tahminin:", key=pred_key, value=st.session_state.user_preds.get(m['id'], ""))
            
            if st.button("Tahminimi Kaydet", key=f"btn_{m['id']}"):
                st.session_state.user_preds[m['id']] = user_input
                st.toast(f"{m['match']} için tahminin kaydedildi!")

with tab2:
    st.subheader("Maç Sonrası Vaka Analizi")
    col1, col2 = st.columns(2)
    with col1:
        match_name = st.selectbox("Analiz Edilecek Maç:", [m['match'] for m in current_pool])
        outcome = st.selectbox("Sonuç:", ["Başarılı", "Başarısız"])
    with col2:
        reason = st.text_area("Neden böyle oldu?")
        if st.button("Analizi Arşive Ekle"):
            st.session_state.cases.append({"match": match_name, "outcome": outcome, "reason": reason})
            st.success("Arşive eklendi.")

    st.markdown("---")
    for c in reversed(st.session_state.cases):
        st.info(f"**{c['match']}** | {c['outcome']}\n\nNot: {c['reason']}")
