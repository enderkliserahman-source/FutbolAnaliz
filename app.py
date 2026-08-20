import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Futbol Analiz",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Streamlit standart çerçevesini tamamen sıfırlayan ve gizleyen CSS
st.markdown("""
<style>
    header, footer, #MainMenu, .stDeployButton, [data-testid="stDecoration"], div[class*="viewerBadge"], [data-testid="stStatusWidget"] {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
    }
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        border: none !important;
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# Birebir Mobil Nesine / İddaa Deneyimi (HTML5 + CSS3 Grid + JS Motoru)
app_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        -webkit-tap-highlight-color: transparent;
    }

    body {
        background-color: #0f1e2c;
        color: #f1f5f9;
        padding-bottom: 90px;
    }

    /* Üst Bar */
    .top-header {
        background: #09141f;
        padding: 12px 14px;
        text-align: center;
        border-bottom: 1px solid #1e3347;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    .top-header h1 {
        font-size: 15px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 0.5px;
    }
    .top-header span {
        font-size: 11px;
        color: #38bdf8;
        font-weight: 600;
    }

    /* Navigasyon / Sekmeler */
    .nav-tabs {
        display: flex;
        background: #132435;
        border-bottom: 1px solid #1e3347;
    }
    .nav-tab {
        flex: 1;
        text-align: center;
        padding: 10px 0;
        font-size: 12px;
        font-weight: 700;
        color: #94a3b8;
        cursor: pointer;
        border-bottom: 2px solid transparent;
    }
    .nav-tab.active {
        color: #38bdf8;
        border-bottom: 2px solid #38bdf8;
        background: rgba(56, 189, 248, 0.05);
    }

    /* Lig Başlığı */
    .league-title {
        background: #162a3d;
        color: #94a3b8;
        font-size: 11px;
        font-weight: 800;
        padding: 6px 10px;
        display: flex;
        justify-content: space-between;
        border-top: 1px solid #1e3347;
        border-bottom: 1px solid #1e3347;
        margin-top: 6px;
    }

    /* Maç Kartı */
    .match-card {
        background: #11202e;
        border-bottom: 1px solid #1a3045;
        padding: 8px 10px;
    }

    .match-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    .match-name {
        font-size: 13px;
        font-weight: 700;
        color: #ffffff;
    }
    .ev-badge {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid #059669;
        font-size: 10px;
        font-weight: 800;
        padding: 2px 6px;
        border-radius: 4px;
    }

    /* 5'li Yan Yana Asla Kaymayan Oran Izgarası */
    .odds-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 4px;
        width: 100%;
    }

    .odd-btn {
        background: #1b3248;
        border: 1px solid #244360;
        border-radius: 6px;
        padding: 5px 0;
        text-align: center;
        cursor: pointer;
        transition: all 0.1s ease;
        user-select: none;
    }
    .odd-btn:active {
        transform: scale(0.96);
    }
    .odd-label {
        font-size: 9px;
        color: #94a3b8;
        display: block;
        line-height: 1;
        margin-bottom: 2px;
        font-weight: 600;
    }
    .odd-value {
        font-size: 12px;
        font-weight: 800;
        color: #ffffff;
        line-height: 1;
    }

    /* SEÇİLDİĞİNDE YANAN CANLI KIRMIZI RENK */
    .odd-btn.selected {
        background: #e63946 !important;
        border-color: #ff4d5e !important;
    }
    .odd-btn.selected .odd-label {
        color: #ffe5e8 !important;
    }
    .odd-btn.selected .odd-value {
        color: #ffffff !important;
    }

    /* Maç Detay ve Model Akordiyon */
    .match-detail-toggle {
        font-size: 11px;
        color: #38bdf8;
        margin-top: 6px;
        display: inline-block;
        cursor: pointer;
        font-weight: 600;
    }
    .detail-body {
        display: none;
        background: #0a1622;
        border-radius: 6px;
        padding: 8px;
        margin-top: 6px;
        border: 1px solid #1a3045;
        font-size: 11px;
    }

    /* Sabit Alt Kupon Çubuğu (Bottom Slip Bar) */
    .bottom-slip {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #09141f;
        border-top: 2px solid #e63946;
        padding: 10px 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 999;
        box-shadow: 0 -4px 15px rgba(0,0,0,0.5);
    }
    .slip-info span {
        font-size: 11px;
        color: #94a3b8;
    }
    .slip-info h3 {
        font-size: 16px;
        color: #38bdf8;
        font-weight: 800;
    }
    .slip-action-btn {
        background: #e63946;
        color: white;
        border: none;
        padding: 8px 14px;
        border-radius: 6px;
        font-weight: 800;
        font-size: 12px;
        cursor: pointer;
    }

    /* Açılır Kupon Modalı */
    #couponModal {
        display: none;
        position: fixed;
        bottom: 60px;
        left: 0;
        right: 0;
        background: #11202e;
        border-top: 1px solid #244360;
        padding: 12px;
        max-height: 50vh;
        overflow-y: auto;
        z-index: 998;
    }
    .coupon-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #1a3045;
        padding: 6px 0;
        font-size: 12px;
    }
</style>
</head>
<body>

<div class="top-header">
    <h1>⚽ FUTBOL ANALİZ & BÜLTEN</h1>
    <span>Poisson & +EV Değer Radarı</span>
</div>

<div class="nav-tabs">
    <div class="nav-tab active">Günün Bülteni</div>
    <div class="nav-tab">+EV Fırsatlar</div>
    <div class="nav-tab">Kayıtlı Kuponlar</div>
</div>

<!-- LİG 1 -->
<div class="league-title">
    <span>🏆 UEFA AVRUPA LİGİ, PLAYOFF</span>
    <span>⏱ 19:00</span>
</div>

<div class="match-card">
    <div class="match-header">
        <span class="match-name">J. Bialystok — Iberia 1999</span>
        <span class="ev-badge">+9.2% EV</span>
    </div>
    <div class="odds-grid">
        <div class="odd-btn" onclick="togglePick(this, 'J. Bialystok - Iberia', 'MS 1', 1.23)"><span class="odd-label">MS 1</span><span class="odd-value">1.23</span></div>
        <div class="odd-btn" onclick="togglePick(this, 'J. Bialystok - Iberia', 'MS X', 4.44)"><span class="odd-label">MS X</span><span class="odd-value">4.44</span></div>
        <div class="odd-btn" onclick="togglePick(this, 'J. Bialystok - Iberia', 'MS 2', 7.26)"><span class="odd-label">MS 2</span><span class="odd-value">7.26</span></div>
        <div class="odd-btn" onclick="togglePick(this, 'J. Bialystok - Iberia', '2.5 Ü', 1.53)"><span class="odd-label">2.5 Ü</span><span class="odd-value">1.53</span></div>
        <div class="odd-btn" onclick="togglePick(this, 'J. Bialystok - Iberia', 'KG V', 1.70)"><span class="odd-label">KG V</span><span class="odd-value">1.70</span></div>
    </div>
    <span class="match-detail-toggle" onclick="toggleDetail('d1')">📊 Model İstatistikleri ▾</span>
    <div class="detail-body" id="d1">
        🎯 <b>Model Tercihi:</b> 2.5 Üst<br>
        📈 <b>Beklenen Gol (xG):</b> Bialystok 2.30 — Iberia 0.65<br>
        🎲 <b>Monte Carlo:</b> %71 Ev | %18 Ber | %11 Dep
    </div>
</div>

<div class="match-card">
    <div class="match-header">
        <span class="match-name">Mjallby — Salzburg</span>
        <span class="ev-badge">+7.8% EV</span>
    </div>
    <div class="odds-grid">
        <div class="odd-btn" onclick="togglePick(this, 'Mjallby - Salzburg', 'MS 1', 3.82)"><span class="odd-label">MS 1</span><span class="odd-value">3.82</span></div>
        <div class="odd-btn" onclick="togglePick(this, 'Mjallby - Salzburg', 'MS X', 3.63)"><span class="odd-label">MS X</span><span class="odd-value">3.63</span></div>
        <div class="odd-btn" onclick="togglePick(this, 'Mjallby - Salzburg', 'MS 2', 1.57)"><span class="odd-label">MS 2</span><span class="odd-value">1.57</span></div>
        <div class="odd-btn" onclick="togglePick(this, 'Mjallby - Salzburg', '2.5 Ü', 1.41)"><span class="odd-label">2.5 Ü</span><span class="odd-value">1.41</span></div>
        <div class="odd-btn" onclick="togglePick(this, 'Mjallby - Salzburg', 'KG V', 1.50)"><span class="odd-label">KG V</span><span class="odd-value">1.50</span></div>
    </div>
    <span class="match-detail-toggle" onclick="toggleDetail('d2')">📊 Model İstatistikleri ▾</span>
    <div class="detail-body" id="d2">
        🎯 <b>Model Tercihi:</b> MS 2<br>
        📈 <b>Beklenen Gol (xG):</b> Mjallby 0.95 — Salzburg 2.10<br>
        🎲 <b>Monte Carlo:</b> %19 Ev | %23 Ber | %58 Dep
    </div>
</div>

<!-- LİG 2 -->
<div class="league-title">
    <span>🏆 UEFA KONFERANS LİGİ, PLAYOFF</span>
    <span>⏱ 20:00</span>
</div>

<div class="match-card">
    <div class="match-header">
        <span class="match-name">Nordsjælland — St. Gallen</span>
        <span class="ev-badge">+10.4% EV</span>
    </div>
    <div class="odds-grid">
        <div class="odd-btn" onclick="togglePick(this, 'Nordsjælland - St. Gallen', 'MS 1', 1.37)"><span class="odd-label">MS 1</span><span class="odd-value">1.37</span></div>
        <div class="odd-btn" onclick="togglePick(this, 'Nordsjælland - St. Gallen', 'MS X', 4.36)"><span class="odd-label">MS X</span><span class="odd-value">4.36</span></div>
        <div class="odd-btn" onclick="togglePick(this, 'Nordsjælland - St. Gallen', 'MS 2', 4.59)"><span class="odd-label">MS 2</span><span class="odd-value">4.59</span></div>
        <div class="odd-btn" onclick="togglePick(this, 'Nordsjælland - St. Gallen', '2.5 Ü', 1.52)"><span class="odd-label">2.5 Ü</span><span class="odd-value">1.52</span></div>
        <div class="odd-btn" onclick="togglePick(this, 'Nordsjælland - St. Gallen', 'KG V', 1.48)"><span class="odd-label">KG V</span><span class="odd-value">1.48</span></div>
    </div>
    <span class="match-detail-toggle" onclick="toggleDetail('d3')">📊 Model İstatistikleri ▾</span>
    <div class="detail-body" id="d3">
        🎯 <b>Model Tercihi:</b> MS 1 & 2.5 Üst<br>
        📈 <b>Beklenen Gol (xG):</b> Nordsjælland 2.45 — St. Gallen 1.10<br>
        🎲 <b>Monte Carlo:</b> %65 Ev | %20 Ber | %15 Dep
    </div>
</div>

<!-- AÇILIR KUPON LİSTESİ MODALI -->
<div id="couponModal">
    <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
        <span style="font-weight:bold; font-size:13px;">📋 Kupon Detayı</span>
        <span style="color:#e63946; cursor:pointer; font-size:11px; font-weight:bold;" onclick="clearCoupon()">Hepsini Temizle ✕</span>
    </div>
    <div id="couponList"></div>
</div>

<!-- ALT SABİT BAR -->
<div class="bottom-slip">
    <div class="slip-info" onclick="toggleModal()">
        <span id="slipCount">0 Maç Seçildi ▴</span>
        <h3 id="slipOdds">Oran: 0.00</h3>
    </div>
    <button class="slip-action-btn" onclick="saveCoupon()">Kuponu Onayla ➔</button>
</div>

<script>
    let myCoupon = {};

    function togglePick(el, match, pick, odd) {
        const key = match + "_" + pick;
        if (myCoupon[key]) {
            delete myCoupon[key];
            el.classList.remove('selected');
        } else {
            myCoupon[key] = { match: match, pick: pick, odd: odd, el: el };
            el.classList.add('selected');
        }
        updateSlip();
    }

    function updateSlip() {
        const keys = Object.keys(myCoupon);
        let total = 1.0;
        let listHtml = "";

        if (keys.length === 0) {
            document.getElementById('slipCount').innerText = "0 Maç Seçildi ▴";
            document.getElementById('slipOdds').innerText = "Oran: 0.00";
            document.getElementById('couponList').innerHTML = "<div style='color:#64748b; text-align:center; padding:10px;'>Kuponunuz boş</div>";
            return;
        }

        keys.forEach(k => {
            const item = myCoupon[k];
            total *= item.odd;
            listHtml += `
                <div class="coupon-item">
                    <div><b>${item.match}</b><br><span style="color:#38bdf8;">${item.pick}</span></div>
                    <div style="font-weight:800; color:#e63946; font-size:13px;">${item.odd.toFixed(2)}</div>
                </div>
            `;
        });

        document.getElementById('slipCount').innerText = keys.length + " Maç Seçildi ▴";
        document.getElementById('slipOdds').innerText = "Toplam: " + total.toFixed(2);
        document.getElementById('couponList').innerHTML = listHtml;
    }

    function toggleDetail(id) {
        const el = document.getElementById(id);
        el.style.display = (el.style.display === 'block') ? 'none' : 'block';
    }

    function toggleModal() {
        const modal = document.getElementById('couponModal');
        modal.style.display = (modal.style.display === 'block') ? 'none' : 'block';
    }

    function clearCoupon() {
        Object.keys(myCoupon).forEach(k => {
            if (myCoupon[k].el) myCoupon[k].el.classList.remove('selected');
        });
        myCoupon = {};
        updateSlip();
        document.getElementById('couponModal').style.display = 'none';
    }

    function saveCoupon() {
        if (Object.keys(myCoupon).length === 0) {
            alert("Lütfen önce bültenden oran seçiniz.");
            return;
        }
        alert("Kupon başarıyla hafızaya kaydedildi!");
    }
</script>
</body>
</html>
"""

components.html(app_html, height=750, scrolling=True)