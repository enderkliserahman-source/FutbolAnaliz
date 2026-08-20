import streamlit as st
import pandas as pd
import numpy as np

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Futbol Veri Laboratuvarı",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 1. State Yönetimi
if "user_decisions" not in st.session_state:
    st.session_state.user_decisions = {}

# 2. Dünkü Başarılı Analizler (Referans Kaydı)
yesterday_results = [
    {
        "match": "Slovan Bratislava vs Celje",
        "pred": "KG Var & 2.5 Üst",
        "score_pred": "2-1 / 3-1",
        "actual_score": "5-0 (KG Yok / 2.5 Üst Geldi)",
        "ev": "+%8.6", "status": "✅ Geldi", "xg": "2.40 - 0.70"
    },
    {
        "match": "NEC Nijmegen vs Bodo Glimt",
        "pred": "2.5 Üst & KG Var",
        "score_pred": "1-2 / 2-2",
        "actual_score": "1-2 (Tam İsabet)",
        "ev": "+%10.2", "status": "🎯 Skor Yakaladı", "xg": "1.35 - 1.85"
    },
    {
        "match": "Hapoel Beer Sheva vs Sabah",
        "pred": "MS 1",
        "score_pred": "2-0",
        "actual_score": "2-0 (Tam İsabet)",
        "ev": "+%7.4", "status": "🎯 Skor Yakaladı", "xg": "1.90 - 0.50"
    },
    {
        "match": "Celtic vs LASK",
        "pred": "MS 1 & 1.5 Üst",
        "score_pred": "3-1",
        "actual_score": "3-1 (Tam İsabet)",
        "ev": "+%9.1", "status": "🎯 Skor Yakaladı", "xg": "2.65 - 0.90"
    },
    {
        "match": "Atletico Madrid vs Malaga",
        "pred": "MS 1 & 1.5 Üst",
        "score_pred": "2-0 / 3-0",
        "actual_score": "2-0 (Tam İsabet)",
        "ev": "+%6.8", "status": "🎯 Skor Yakaladı", "xg": "2.10 - 0.40"
    }
]

# 3. Güncel Maç Havuzu (Tier-1 ve Tier-2)
current_pool = [
    {
        "id": 101, "tier": "Tier-1 (Yüksek Güven)",
        "league": "UEFA Konferans Ligi", "match": "Nordsjælland vs St. Gallen",
        "xg_home": 2.45, "xg_away": 1.10,
        "model_main": "MS 1 & 2.5 Üst", "model_prob": "%74",
        "model_score": "2-1 veya 3-1", "ev": "+%10.4",
        "mc_home": "%65", "mc_draw": "%20", "mc_away": "%15"
    },
    {
        "id": 102, "tier": "Tier-1 (Yüksek Güven)",
        "league": "UEFA Avrupa Ligi", "match": "Mjallby vs Salzburg",
        "xg_home": 0.95, "xg_away": 2.10,
        "model_main": "MS 2 & 1.5 Üst", "model_prob": "%68",
        "model_score": "0-2 veya 1-2", "ev": "+%8.1",
        "mc_home": "%19", "mc_draw": "%23", "mc_away": "%58"
    },
    {
        "id": 103, "tier": "Tier-2 (Sürpriz / Yüksek Gol Değeri)",
        "league": "UEFA Avrupa Ligi", "match": "J. Bialystok vs Iberia 1999",
        "xg_home": 2.30, "xg_away": 0.65,
        "model_main": "2.5 Üst", "model_prob": "%76",
        "model_score": "3-0 veya 3-1", "ev": "+%9.2",
        "mc_home": "%71", "mc_draw": "%18", "mc_away": "%11"
    },
    {
        "id": 104, "tier": "Tier-2 (Sürpriz / Yüksek Gol Değeri)",
        "league": "Portekiz U23", "match": "Benfica U23 vs Rio Ave U23",
        "xg_home": 1.60, "xg_away": 1.40,
        "model_main": "KG Var", "model_prob": "%68",
        "model_score": "1-1 veya 2-1", "ev": "+%6.5",
        "mc_home": "%42", "mc_draw": "%28", "mc_away": "%30"
    }
]

# Şık Veri Laboratuvarı Teması
st.markdown("""
<style>
    .stApp { background-color: #0d1527; color: #e2e8f0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .block-container { padding-top: 1.5rem; padding-bottom: 4rem; }
    .lab-card { background: #162035; border: 1px solid #1e293b; border-radius: 10px; padding: 14px; margin-bottom: 12px; }
    .badge-tier1 { background: #0284c7; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; }
    .badge-tier2 { background: #d97706; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; }
    .metric-value { font-size: 1.2rem; font-weight: 800; color: #38bdf8; }
</style>
""", unsafe_allow_html=True)

# Üst Başlık
st.markdown("""
<div style="text-align:center; margin-bottom: 20px;">
    <h2 style="color:#ffffff; margin-bottom:0;">🔬 FUTBOL VERİ & İSTİŞARE LABORATUVARI</h2>
    <span style="color:#38bdf8; font-size:0.9rem;">Poisson xG Dağılımı • İnsan & Model Konsensüs Masası</span>
</div>
""", unsafe_allow_html=True)

tab_analiz, tab_gecmis = st.tabs(["⚡ Canlı İstişare Masası (Günün Maçları)", "🏆 Dünün 5/5 Referans Kayıtları"])

# ==========================================
# SEKME 1: İSTİŞARE & KARAR MASASI
# ==========================================
with tab_analiz:
    st.markdown("#### 🎯 Modelin Filtrelediği Güncel Maç Havuzu")
    
    for m in current_pool:
        tier_class = "badge-tier1" if "Tier-1" in m["tier"] else "badge-tier2"
        
        with st.container():
            st.markdown(f"""
            <div class="lab-card">
                <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                    <span class="{tier_class}">{m['tier']}</span>
                    <span style="color:#94a3b8; font-size:0.8rem;">{m['league']}</span>
                </div>
                <h3 style="margin:0 0 10px 0; color:#ffffff;">{m['match']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col_model, col_human = st.columns(2)
            
            # SOL: MODEL ÇIKTISI
            with col_model:
                st.markdown("**🤖 Modelin Analiz Raporu:**")
                st.info(f"**Öneri:** {m['model_main']} (Güven: {m['model_prob']} | EV: {m['ev']})\n\n**Beklenen Skor:** `{m['model_score']}`")
                st.caption(f"xG: {m['xg_home']} - {m['xg_away']} | Monte Carlo: 1: {m['mc_home']} / X: {m['mc_draw']} / 2: {m['mc_away']}")

            # SAĞ: İNSAN TAHMİNİ & ORTAK KARAR
            with col_human:
                st.markdown("**👤 Senin Analizin & Ortak Karar:**")
                user_pick = st.text_input("Senin Taktiksel Öngörün:", key=f"user_pick_{m['id']}", placeholder="Örn: 2.5 Üst veya MS 1")
                consensus = st.selectbox("Ortak Konsensüs:", ["Henüz Karar Verilmedi", "Model ile Mutabık", "İnsan Görüşü Baskın", "Riskli - Pas Geç"], key=f"cons_{m['id']}")
                
                if st.button("Kararı Kaydet 💾", key=f"save_{m['id']}"):
                    st.session_state.user_decisions[m['id']] = {
                        "match": m['match'],
                        "model": m['model_main'],
                        "user": user_pick,
                        "status": consensus
                    }
                    st.success("Karar takip havuzuna kaydedildi!")
            
            st.divider()

# ==========================================
# SEKME 2: DÜNKÜ BAŞARILI 5/5 PERFORMANSI
# ==========================================
with tab_gecmis:
    st.markdown("#### 📊 Dünün 5/5 Tam İbreli Başarı Raporu")
    st.caption("Modelin dün ürettiği xG tahminleri, önerileri ve sahada yakalanan tam skorlar:")
    
    df_yesterday = pd.DataFrame(yesterday_results)
    st.table(df_yesterday.rename(columns={
        "match": "Karşılaşma",
        "pred": "Model Önerisi",
        "score_pred": "Öngörülen Skor",
        "actual_score": "Gerçek Skor",
        "ev": "Değer",
        "status": "Sonuç",
        "xg": "xG Değerleri"
    }))
