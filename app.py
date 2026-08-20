import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# 1. Veri Yapıları
if "cases" not in st.session_state: st.session_state.cases = []

# 2. CSS - Daha Profesyonel Veri Laboratuvarı Görünümü
st.markdown("""
<style>
    .stApp { background: #0f172a; color: #f8fafc; }
    .case-card { background: #1e293b; border-left: 4px solid #38bdf8; padding: 10px; margin-bottom: 10px; border-radius: 4px; }
    input, select { background: #334155 !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

st.title("🔬 Veri Laboratuvarı: Vaka Analizi")

# 3. Sekmeler
tab1, tab2 = st.tabs(["📋 Yeni Vaka Analizi", "📚 Arşivlenmiş Dersler"])

with tab1:
    st.subheader("Maç Sonrası Analiz Formu")
    col1, col2 = st.columns(2)
    
    with col1:
        match_name = st.text_input("Maç Adı (Örn: Inter Turku - Kopenhag)")
        source = st.selectbox("Kaynak:", ["Model Sinyali", "İnsan Sezgisi (Senin Tahminin)"])
    with col2:
        outcome = st.selectbox("Sonuç:", ["Başarılı", "Başarısız", "Yarı Başarılı"])
        reason = st.text_area("Analist Notu (Neden böyle oldu?):", placeholder="Örn: Kopenhag çok baskı kurdu ama Inter'in 5'li savunması beklentinin üzerindeydi.")
    
    if st.button("Vakayı Sisteme İşle 💾"):
        st.session_state.cases.append({
            "match": match_name, "source": source, "outcome": outcome, "reason": reason
        })
        st.success("Not alındı! Bu veri sistemi geliştirmek için kullanıldı.")

with tab2:
    st.subheader("Öğrenilenler Arşivi")
    if not st.session_state.cases:
        st.info("Henüz vaka analizi girilmemiş.")
    else:
        for c in reversed(st.session_state.cases):
            color = "#22c55e" if c['outcome'] == "Başarılı" else "#ef4444"
            st.markdown(f"""
            <div class="case-card">
                <b>{c['match']}</b> | <span style="color:{color}">{c['outcome']}</span><br>
                <small>Kaynak: {c['source']}</small><br>
                <i>{c['reason']}</i>
            </div>
            """, unsafe_allow_html=True)

st.divider()
st.caption("Not: Bu veriler, bir sonraki seans için algoritma filtrelerini güncellemede kullanılacaktır.")
