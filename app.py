import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import poisson
import pandas as pd
from bulletin_fetcher import BulletinScanner

# Bülten Servisi
scanner = BulletinScanner()
matches = scanner.get_live_bulletin()

# Sayfa Ayarları
st.set_page_config(page_title="Futbol Analiz Laboratuvarı", page_icon="⚽", layout="wide")
st.title("⚽ Futbol Analiz & Canlı Bülten Laboratuvarı")
st.caption("Poisson Modeli + Monte Carlo Simülatörü + Otomatik +EV Bülten Radarı")

# Sol Panel - Sadece Maç Seçimi
st.sidebar.header("📋 Bülten Maçı Seç")
match_names = [f"{m['ev']} vs {m['dep']} ({m['lig']})" for m in matches]
selected_match_str = st.sidebar.selectbox("Analiz Edilecek Karşılaşma", match_names, index=0)

# Seçilen Maçın Bilgilerini Çek
selected_idx = match_names.index(selected_match_str)
m_data = matches[selected_idx]

home_team = m_data["ev"]
away_team = m_data["dep"]
home_lambda = m_data["ev_xg"]
away_lambda = m_data["dep_xg"]
odds_1 = m_data["ms1_oran"]
odds_0 = m_data["ms0_oran"]
odds_2 = m_data["ms2_oran"]
ust25_oran = m_data["ust25_oran"]
kg_var_oran = m_data["kg_var_oran"]

# Sol Panel Bilgi Özeti
st.sidebar.markdown("---")
st.sidebar.subheader("📌 Seçili Maç Oranları")
st.sidebar.write(f"**MS 1:** `{odds_1}`")
st.sidebar.write(f"**MS 0:** `{odds_0}`")
st.sidebar.write(f"**MS 2:** `{odds_2}`")
st.sidebar.write(f"**2.5 Üst:** `{ust25_oran}`")
st.sidebar.write(f"**KG Var:** `{kg_var_oran}`")

# Poisson Olasılık Matrisi
max_goals = 6
home_probs = [poisson.pmf(i, home_lambda) for i in range(max_goals)]
away_probs = [poisson.pmf(i, away_lambda) for i in range(max_goals)]
matrix = np.outer(home_probs, away_probs)

# İhtimaller
home_win = np.sum(np.tril(matrix, -1)) * 100
draw = np.sum(np.diag(matrix)) * 100
away_win = np.sum(np.triu(matrix, 1)) * 100

over_2_5 = sum(matrix[h, a] for h in range(max_goals) for a in range(max_goals) if h + a > 2.5) * 100
under_2_5 = 100.0 - over_2_5
btts = sum(matrix[h, a] for h in range(1, max_goals) for a in range(1, max_goals)) * 100

# Değerli Oran (+EV)
ev_1 = ((home_win / 100) * odds_1) - 1
ev_0 = ((draw / 100) * odds_0) - 1
ev_2 = ((away_win / 100) * odds_2) - 1
ev_over = ((over_2_5 / 100) * ust25_oran) - 1
ev_kg = ((btts / 100) * kg_var_oran) - 1

# En Olası Skorlar
score_list = []
for h in range(max_goals):
    for a in range(max_goals):
        score_list.append((f"{h} - {a}", matrix[h, a] * 100))
score_list.sort(key=lambda x: x[1], reverse=True)
top_scores = score_list[:5]

# --- EKRAN YERLEŞİMİ (4 SEKME) ---
tab_radar, tab1, tab2, tab3 = st.tabs([
    "📡 Otomatik Bülten Radarı (+EV Fırsatları)",
    f"📊 {home_team} - {away_team} Detaylı Analiz", 
    f"🎲 {home_team} - {away_team} 10.000 Maç Simülasyonu", 
    "📝 Kupon Takip Masası"
])

with tab_radar:
    st.subheader("📡 Günün Bülteni Otomatik Tarama & Fırsat Dedektifi")
    st.write("Tüm bülten tek tıkla taranır ve piyasa oranlarındaki değerler listelenir.")

    if st.button("🔄 Bülteni Tara ve Değerleri Listele"):
        with st.spinner("Bülten taranıyor..."):
            df_radar = scanner.scan_all()
            st.success(f"Tarama tamamlandı! Toplam {len(df_radar)} maç analiz edildi.")
            st.dataframe(df_radar, use_container_width=True)

with tab1:
    st.subheader(f"📊 {home_team} vs {away_team} Matematiksel Olasılıkları")
    c1, c2, c3 = st.columns(3)
    c1.metric(label=f"MS 1 ({home_team})", value=f"%{home_win:.1f}", delta=f"Oran: {odds_1}")
    c2.metric(label="MS 0 (Beraberlik)", value=f"%{draw:.1f}", delta=f"Oran: {odds_0}")
    c3.metric(label=f"MS 2 ({away_team})", value=f"%{away_win:.1f}", delta=f"Oran: {odds_2}")

    st.markdown("---")
    st.subheader("💡 Değerli Oran (+EV) Analizi")
    ev_col1, ev_col2, ev_col3, ev_col4, ev_col5 = st.columns(5)
    
    with ev_col1:
        if ev_1 > 0:
            st.success(f"**MS 1 DEĞERLİ!**\n\n+EV: %{ev_1*100:.1f}")
        else:
            st.info(f"MS 1\n\nEV: %{ev_1*100:.1f}")
            
    with ev_col2:
        if ev_0 > 0:
            st.success(f"**MS 0 DEĞERLİ!**\n\n+EV: %{ev_0*100:.1f}")
        else:
            st.info(f"MS 0\n\nEV: %{ev_0*100:.1f}")
            
    with ev_col3:
        if ev_2 > 0:
            st.success(f"**MS 2 DEĞERLİ!**\n\n+EV: %{ev_2*100:.1f}")
        else:
            st.info(f"MS 2\n\nEV: %{ev_2*100:.1f}")

    with ev_col4:
        if ev_over > 0:
            st.success(f"**2.5 Üst DEĞERLİ!**\n\n+EV: %{ev_over*100:.1f}")
        else:
            st.info(f"2.5 Üst\n\nEV: %{ev_over*100:.1f}")

    with ev_col5:
        if ev_kg > 0:
            st.success(f"**KG Var DEĞERLİ!**\n\n+EV: %{ev_kg*100:.1f}")
        else:
            st.info(f"KG Var\n\nEV: %{ev_kg*100:.1f}")

    st.markdown("---")
    col_left, col_mid, col_right = st.columns([1, 1, 1.2])

    with col_left:
        st.subheader("🎯 Gol Pazarları")
        st.write(f"**2.5 Üst:** %{over_2_5:.1f} (Oran: `{ust25_oran}`)")
        st.write(f"**2.5 Alt:** %{under_2_5:.1f}")
        st.write(f"**KG Var:** %{btts:.1f} (Oran: `{kg_var_oran}`)")
        st.markdown("---")
        st.subheader("📈 Beklenen Gol (xG)")
        st.write(f"**{home_team}:** {home_lambda:.2f}")
        st.write(f"**{away_team}:** {away_lambda:.2f}")

    with col_mid:
        st.subheader("🏆 En Olası 5 Skor")
        for rank, (score, prob) in enumerate(top_scores, 1):
            st.write(f"**{rank}.** `{score}` ➔ **%{prob:.1f}**")

    with col_right:
        st.subheader("🔥 Skor Isı Haritası")
        fig, ax = plt.subplots(figsize=(6, 4.5))
        sns.heatmap(matrix * 100, annot=True, fmt=".1f", cmap="Blues", cbar=False,
                    xticklabels=[f"{i}" for i in range(max_goals)], 
                    yticklabels=[f"{i}" for i in range(max_goals)], 
                    ax=ax)
        ax.set_xlabel(f"{away_team} Golleri")
        ax.set_ylabel(f"{home_team} Golleri")
        st.pyplot(fig)

with tab2:
    st.subheader(f"🎲 {home_team} vs {away_team} — 10.000 Maçlık Monte Carlo Simülasyonu")
    st.write(f"Algoritma bu maçı {home_team} ({home_lambda:.2f} xG) ve {away_team} ({away_lambda:.2f} xG) değerleriyle 10.000 kez baştan sona oynatır.")

    if st.button("🚀 Bu Maçı 10.000 Kez Simüle Et"):
        with st.spinner("10.000 maç simüle ediliyor..."):
            sim_home_goals = np.random.poisson(home_lambda, 10000)
            sim_away_goals = np.random.poisson(away_lambda, 10000)

            sim_home_wins = int(np.sum(sim_home_goals > sim_away_goals))
            sim_draws = int(np.sum(sim_home_goals == sim_away_goals))
            sim_away_wins = int(np.sum(sim_home_goals < sim_away_goals))

            sc1, sc2, sc3 = st.columns(3)
            sc1.metric(label=f"Simüle {home_team} Galibiyeti", value=f"{sim_home_wins} kez", delta=f"%{(sim_home_wins/10000)*100:.1f}")
            sc2.metric(label="Simüle Beraberlik", value=f"{sim_draws} kez", delta=f"%{(sim_draws/10000)*100:.1f}")
            sc3.metric(label=f"Simüle {away_team} Galibiyeti", value=f"{sim_away_wins} kez", delta=f"%{(sim_away_wins/10000)*100:.1f}")

            st.markdown("---")
            fig_sim, ax_sim = plt.subplots(figsize=(8, 3.5))
            ax_sim.hist(sim_home_goals - sim_away_goals, bins=range(-5, 6), color="teal", edgecolor="black", align="left", rwidth=0.8)
            ax_sim.set_title(f"Gol Farkı Dağılımı (Pozitif: {home_team} | Negatif: {away_team})")
            ax_sim.set_xlabel("Gol Farkı")
            ax_sim.set_ylabel("Maç Sayısı")
            st.pyplot(fig_sim)

with tab3:
    st.subheader("📝 Kupon Kayıt & Karşılaştırma Masası")
    
    coupons = {
        "🎯 Senin Kuponun (Taktik & Beraberlik)": {
            "Toplam Oran": 163.51,
            "Bahis Bedeli": "50 TL",
            "Maks Kazanç": "8.175,68 TL",
            "Maçlar": [
                {"Maç": "Slovan Bratislava - Celje", "Tercih": "MS 0", "Oran": 3.38},
                {"Maç": "NEC Nijmegen - Bodo Glimt", "Tercih": "MS 0", "Oran": 3.53},
                {"Maç": "Hapoel Beer Sheva - Sabah", "Tercih": "MS 0", "Oran": 3.07},
                {"Maç": "Celtic - LASK", "Tercih": "MS 1 & KG Var", "Oran": 3.10},
                {"Maç": "Atletico Madrid - Malaga", "Tercih": "MS 1 & 1.5 Üst", "Oran": 1.44}
            ]
        },
        "🤖 Modelin Kuponu (Saf Olasılık)": {
            "Toplam Oran": 15.43,
            "Bahis Bedeli": "50 TL",
            "Maks Kazanç": "771,50 TL",
            "Maçlar": [
                {"Maç": "Slovan Bratislava - Celje", "Tercih": "KG Var", "Oran": 1.70},
                {"Maç": "NEC Nijmegen - Bodo Glimt", "Tercih": "2.5 Üst", "Oran": 1.62},
                {"Maç": "Hapoel Beer Sheva - Sabah", "Tercih": "MS 1", "Oran": 1.75},
                {"Maç": "Celtic - LASK", "Tercih": "MS 1 & 1.5 Üst", "Oran": 1.80},
                {"Maç": "Atletico Madrid - Malaga", "Tercih": "MS 1 & 1.5 Üst", "Oran": 1.44}
            ]
        }
    }

    selected_coupon = st.selectbox("İncelemek / Takip Etmek İstediğin Kuponu Seç:", list(coupons.keys()))
    cp_data = coupons[selected_coupon]

    k1, k2, k3 = st.columns(3)
    k1.metric("Toplam Oran", f"{cp_data['Toplam Oran']}")
    k2.metric("Kupon Bedeli", cp_data["Bahis Bedeli"])
    k3.metric("Maksimum Kazanç", cp_data["Maks Kazanç"])

    st.markdown("#### Kupondaki Maçlar & Tercihler")
    df_matches = pd.DataFrame(cp_data["Maçlar"])
    st.table(df_matches)