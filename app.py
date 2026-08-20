import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Futbol Analiz Pro",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Streamlit varsayılan başlık ve logolarını kaldıran CSS
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

# Tek Parça Native WebApp Kodu (SPA - Sayfa Geçişli, AI Sohbetli, Kupon Motorlu)
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
        background-color: #0b1724;
        color: #f1f5f9;
        padding-bottom: 130px; /* Kupon barının altında hiçbir şey kalmasın */
    }

    /* Üst Başlık */
    .top-header {
        background: #070f18;
        padding: 12px 14px;
        text-align: center;
        border-bottom: 1px solid #162638;
        position: sticky;
        top: 0;
        z-index: 100;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .top-header h1 {
        font-size: 15px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 0.3px;
        flex: 1;
    }
    .back-btn {
        background: #162638;
        color: #38bdf8;
        border: 1px solid #233b54;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: bold;
        cursor: pointer;
        display: none;
    }

    /* Lig Bandı */
    .league-title {
        background: #112030;
        color: #94a3b8;
        font-size: 11px;
        font-weight: 800;
        padding: 7px 12px;
        display: flex;
        justify-content: space-between;
        border-top: 1px solid #162638;
        border-bottom: 1px solid #162638;
        margin-top: 8px;
    }

    /* Ana Sayfa Maç Kartı */
    .bulten-item {
        background: #0f1d2c;
        border-bottom: 1px solid #192e44;
        padding: 12px 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        cursor: pointer;
        transition: background 0.15s ease;
    }
    .bulten-item:active {
        background: #16283d;
    }
    .match-teams {
        font-size: 13px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 3px;
    }
    .match-sub {
        font-size: 11px;
        color: #64748b;
    }
    .ev-tag {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid #059669;
        font-size: 10px;
        font-weight: 800;
        padding: 3px 7px;
        border-radius: 4px;
    }

    /* Detay Sayfası Tasarımı */
    #detailView {
        display: none;
        padding: 10px;
    }

    .detail-card-head {
        background: #112030;
        border: 1px solid #1e354f;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        margin-bottom: 10px;
    }

    .market-label {
        background: #cfe2f3;
        color: #070f18;
        font-size: 11px;
        font-weight: 800;
        padding: 5px 8px;
        border-radius: 4px;
        margin: 10px 0 6px 0;
    }

    /* 5'li Yan Yana Oran Izgarası */
    .odds-grid-5 {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 4px;
        width: 100%;
        margin-bottom: 6px;
    }
    .odds-grid-2 {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px;
        width: 100%;
        margin-bottom: 6px;
    }

    .odd-box {
        background: #182e44;
        border: 1px solid #244362;
        border-radius: 6px;
        padding: 6px 0;
        text-align: center;
        cursor: pointer;
        user-select: none;
    }
    .odd-box:active { transform: scale(0.96); }
    .odd-label {
        font-size: 9px;
        color: #94a3b8;
        display: block;
        margin-bottom: 2px;
        font-weight: 700;
    }
    .odd-val {
        font-size: 12px;
        font-weight: 800;
        color: #ffffff;
    }

    /* Seçilince Kırmızı */
    .odd-box.selected {
        background: #e63946 !important;
        border-color: #ff4d5e !important;
    }
    .odd-box.selected .odd-label { color: #ffe5e8 !important; }

    /* İstatistik / Analiz Kutuları */
    .stat-box {
        background: #0f1d2c;
        border: 1px solid #192e44;
        border-radius: 8px;
        padding: 10px;
        margin-top: 10px;
        font-size: 12px;
    }

    /* AI Danışman Sohbet Alanı */
    .chat-box {
        background: #09131d;
        border: 1px solid #1e354f;
        border-radius: 8px;
        padding: 10px;
        margin-top: 12px;
    }
    .chat-messages {
        max-height: 140px;
        overflow-y: auto;
        font-size: 12px;
        margin-bottom: 8px;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    .msg-bot {
        background: #162a3d;
        padding: 6px 8px;
        border-radius: 6px;
        color: #e2e8f0;
        align-self: flex-start;
        max-width: 90%;
    }
    .msg-user {
        background: #2563eb;
        padding: 6px 8px;
        border-radius: 6px;
        color: #ffffff;
        align-self: flex-end;
        max-width: 90%;
    }
    .chat-input-row {
        display: flex;
        gap: 4px;
    }
    .chat-input {
        flex: 1;
        background: #112030;
        border: 1px solid #233b54;
        border-radius: 6px;
        color: white;
        padding: 6px 8px;
        font-size: 12px;
        outline: none;
    }
    .chat-send {
        background: #38bdf8;
        color: #070f18;
        border: none;
        border-radius: 6px;
        padding: 6px 12px;
        font-weight: bold;
        font-size: 11px;
        cursor: pointer;
    }

    /* Alt Sabit Kupon Barı */
    .bottom-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #070f18;
        border-top: 2px solid #e63946;
        padding: 10px 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 999;
        box-shadow: 0 -4px 15px rgba(0,0,0,0.6);
    }

    #couponModal {
        display: none;
        position: fixed;
        bottom: 62px;
        left: 0;
        right: 0;
        background: #0f1d2c;
        border-top: 1px solid #244362;
        padding: 12px;
        max-height: 45vh;
        overflow-y: auto;
        z-index: 998;
    }
    .c-item {
        display: flex;
        justify-content: space-between;
        border-bottom: 1px solid #192e44;
        padding: 6px 0;
        font-size: 12px;
    }
</style>
</head>
<body>

<div class="top-header">
    <button class="back-btn" id="backBtn" onclick="goBack()">⬅ Bülten</button>
    <h1 id="pageTitle">⚽ GÜNÜN BÜLTENİ</h1>
</div>

<!-- 1. GÖRÜNÜM: ANA SAYFA BÜLTEN LİSTESİ -->
<div id="bultenView">
    <div class="league-title">
        <span>🏆 UEFA AVRUPA LİGİ, PLAYOFF</span>
        <span>Bugün</span>
    </div>

    <div class="bulten-item" onclick="openMatch(1)">
        <div>
            <div class="match-teams">J. Bialystok — Iberia 1999</div>
            <div class="match-sub">⏱ 19:00 • Oranlar & Analiz için dokun</div>
        </div>
        <span class="ev-tag">+9.2% EV</span>
    </div>

    <div class="bulten-item" onclick="openMatch(2)">
        <div>
            <div class="match-teams">Mjallby — Salzburg</div>
            <div class="match-sub">⏱ 19:00 • Oranlar & Analiz için dokun</div>
        </div>
        <span class="ev-tag">+7.8% EV</span>
    </div>

    <div class="league-title">
        <span>🏆 UEFA KONFERANS LİGİ, PLAYOFF</span>
        <span>Bugün</span>
    </div>

    <div class="bulten-item" onclick="openMatch(3)">
        <div>
            <div class="match-teams">Nordsjælland — St. Gallen</div>
            <div class="match-sub">⏱ 20:00 • Oranlar & Analiz için dokun</div>
        </div>
        <span class="ev-tag">+10.4% EV</span>
    </div>

    <div class="league-title">
        <span>🏆 PORTEKİZ U23 LİGİ</span>
        <span>Bugün</span>
    </div>

    <div class="bulten-item" onclick="openMatch(4)">
        <div>
            <div class="match-teams">Benfica U23 — Rio Ave U23</div>
            <div class="match-sub">⏱ 19:00 • Oranlar & Analiz için dokun</div>
        </div>
        <span class="ev-tag">+6.5% EV</span>
    </div>
</div>

<!-- 2. GÖRÜNÜM: MAÇ DETAY, ORANLAR, ANALİZ & SOHBET -->
<div id="detailView">
    <div class="detail-card-head">
        <div style="font-size:11px; color:#94a3b8;" id="dTimeLeague">⏱ 19:00 • UEFA AVRUPA LİGİ</div>
        <div style="font-size:15px; font-weight:800; margin-top:2px;" id="dMatchTitle">Takım A — Takım B</div>
    </div>

    <!-- MAÇ SONUCU -->
    <div class="market-label">MAÇ SONUCU & POPÜLER</div>
    <div class="odds-grid-5" id="oddsGrid">
        <!-- Dinamik basılacak -->
    </div>

    <!-- ALT / ÜST & KG -->
    <div class="market-label">DİĞER SEÇENEKLER</div>
    <div class="odds-grid-2" id="oddsGrid2">
        <!-- Dinamik basılacak -->
    </div>

    <!-- MODEL ANALİZ VE xG KARTI -->
    <div class="stat-box">
        <div style="color:#38bdf8; font-weight:bold; margin-bottom:4px;">📊 Model Analizi & xG</div>
        <div id="dModelDesc">Model Önerisi Yükleniyor...</div>
        <div style="margin-top:6px; font-weight:600;" id="dXgVal">xG: -</div>
        <div style="margin-top:4px; color:#94a3b8;" id="dMonteCarlo">Monte Carlo: -</div>
    </div>

    <!-- SENİNLE SOHBET ALANI -->
    <div class="chat-box">
        <div style="font-weight:bold; font-size:12px; color:#38bdf8; margin-bottom:6px;">💬 Model Danışmanı Sohbeti</div>
        <div class="chat-messages" id="chatMsgs">
            <div class="msg-bot">Selam ortak! Bu maçın verilerini inceledim. Aklına takılan bir istatistik veya oran varsa sor, hemen değerlendireyim.</div>
        </div>
        <div class="chat-input-row">
            <input type="text" class="chat-input" id="chatInput" placeholder="Maçla ilgili bir şey sor..." onkeypress="handleEnter(event)">
            <button class="chat-send" onclick="sendMsg()">Sor</button>
        </div>
    </div>
</div>

<!-- AÇILIR KUPON MODALI -->
<div id="couponModal">
    <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
        <span style="font-weight:bold; font-size:13px;">📋 Kupon Detayı</span>
        <span style="color:#e63946; cursor:pointer; font-size:11px; font-weight:bold;" onclick="clearCoupon()">Temizle ✕</span>
    </div>
    <div id="couponList"></div>
</div>

<!-- SABİT ALT KUPON BARI -->
<div class="bottom-bar">
    <div onclick="toggleModal()" style="cursor:pointer;">
        <span style="font-size:11px; color:#94a3b8;" id="slipCount">0 Tercih Seçildi ▴</span>
        <h3 style="font-size:15px; color:#38bdf8; font-weight:800;" id="slipOdds">Oran: 0.00</h3>
    </div>
    <button style="background:#e63946; color:white; border:none; padding:8px 14px; border-radius:6px; font-weight:bold; font-size:12px; cursor:pointer;" onclick="saveSlip()">Kuponu Kaydet ➔</button>
</div>

<script>
    const matches = {
        1: {
            title: "J. Bialystok — Iberia 1999", league: "UEFA AVRUPA LİGİ", time: "19:00",
            ms1: 1.23, msx: 4.44, ms2: 7.26, ust: 1.53, alt: 1.91, kg_var: 1.70, kg_yok: 1.85,
            model_pick: "2.5 Üst (%9.2 +EV Fırsatı)", xg: "Bialystok: 2.30 — Iberia: 0.65",
            mc: "Ev: %71 | Ber: %18 | Dep: %11"
        },
        2: {
            title: "Mjallby — Salzburg", league: "UEFA AVRUPA LİGİ", time: "19:00",
            ms1: 3.82, msx: 3.63, ms2: 1.57, ust: 1.41, alt: 2.14, kg_var: 1.50, kg_yok: 2.10,
            model_pick: "MS 2 (%7.8 +EV Fırsatı)", xg: "Mjallby: 0.95 — Salzburg: 2.10",
            mc: "Ev: %19 | Ber: %23 | Dep: %58"
        },
        3: {
            title: "Nordsjælland — St. Gallen", league: "UEFA KONFERANS LİGİ", time: "20:00",
            ms1: 1.37, msx: 4.36, ms2: 4.59, ust: 1.52, alt: 2.15, kg_var: 1.48, kg_yok: 2.10,
            model_pick: "MS 1 & 2.5 Üst (%10.4 +EV Fırsatı)", xg: "Nordsjælland: 2.45 — St. Gallen: 1.10",
            mc: "Ev: %65 | Ber: %20 | Dep: %15"
        },
        4: {
            title: "Benfica U23 — Rio Ave U23", league: "PORTEKİZ U23 LİGİ", time: "19:00",
            ms1: 1.96, msx: 3.11, ms2: 2.64, ust: 1.51, alt: 1.84, kg_var: 1.55, kg_yok: 2.05,
            model_pick: "KG Var (%6.5 +EV Fırsatı)", xg: "Benfica: 1.60 — Rio Ave: 1.40",
            mc: "Ev: %42 | Ber: %28 | Dep: %30"
        }
    };

    let myCoupon = {};
    let activeMatchId = null;

    function openMatch(id) {
        activeMatchId = id;
        const m = matches[id];
        document.getElementById('bultenView').style.display = 'none';
        document.getElementById('detailView').style.display = 'block';
        document.getElementById('backBtn').style.display = 'inline-block';
        document.getElementById('pageTitle').innerText = "MAÇ DETAYI";
        
        document.getElementById('dTimeLeague').innerText = "⏱ " + m.time + " • " + m.league;
        document.getElementById('dMatchTitle').innerText = m.title;
        document.getElementById('dModelDesc').innerHTML = "🎯 <b>Model Önerisi:</b> " + m.model_pick;
        document.getElementById('dXgVal').innerText = "📈 Beklenen Gol: " + m.xg;
        document.getElementById('dMonteCarlo').innerText = "🎲 Monte Carlo: " + m.mc;

        // Oran Butonlarını Doldur
        renderOdds(id, m);
    }

    function goBack() {
        document.getElementById('detailView').style.display = 'none';
        document.getElementById('bultenView').style.display = 'block';
        document.getElementById('backBtn').style.display = 'none';
        document.getElementById('pageTitle').innerText = "⚽ GÜNÜN BÜLTENİ";
    }

    function renderOdds(id, m) {
        const grid1 = document.getElementById('oddsGrid');
        const grid2 = document.getElementById('oddsGrid2');

        const odds1 = [
            { l: 'MS 1', o: m.ms1, p: '1' },
            { l: 'MS X', o: m.msx, p: 'X' },
            { l: 'MS 2', o: m.ms2, p: '2' },
            { l: '2.5 Ü', o: m.ust, p: '2.5 Üst' },
            { l: 'KG V', o: m.kg_var, p: 'KG Var' }
        ];

        const odds2 = [
            { l: '2.5 Alt', o: m.alt, p: '2.5 Alt' },
            { l: 'KG Yok', o: m.kg_yok, p: 'KG Yok' }
        ];

        grid1.innerHTML = odds1.map(item => {
            const key = m.title + "_" + item.p;
            const sel = myCoupon[key] ? "selected" : "";
            return `<div class="odd-box ${sel}" onclick="togglePick(this, '${m.title}', '${item.p}', ${item.o})"><span class="odd-label">${item.l}</span><span class="odd-val">${item.o}</span></div>`;
        }).join('');

        grid2.innerHTML = odds2.map(item => {
            const key = m.title + "_" + item.p;
            const sel = myCoupon[key] ? "selected" : "";
            return `<div class="odd-box ${sel}" onclick="togglePick(this, '${m.title}', '${item.p}', ${item.o})"><span class="odd-label">${item.l}</span><span class="odd-val">${item.o}</span></div>`;
        }).join('');
    }

    function togglePick(el, match, pick, odd) {
        const key = match + "_" + pick;
        if (myCoupon[key]) {
            delete myCoupon[key];
            el.classList.remove('selected');
        } else {
            myCoupon[key] = { match: match, pick: pick, odd: odd };
            el.classList.add('selected');
        }
        updateSlip();
    }

    function updateSlip() {
        const keys = Object.keys(myCoupon);
        let total = 1.0;
        let listHtml = "";

        if (keys.length === 0) {
            document.getElementById('slipCount').innerText = "0 Tercih Seçildi ▴";
            document.getElementById('slipOdds').innerText = "Oran: 0.00";
            document.getElementById('couponList').innerHTML = "<div style='color:#64748b; text-align:center; padding:8px;'>Kuponunuz boş</div>";
            return;
        }

        keys.forEach(k => {
            const item = myCoupon[k];
            total *= item.odd;
            listHtml += `
                <div class="c-item">
                    <div><b>${item.match}</b><br><span style="color:#38bdf8;">${item.pick}</span></div>
                    <div style="font-weight:800; color:#e63946; font-size:13px; align-self:center;">${item.odd.toFixed(2)}</div>
                </div>
            `;
        });

        document.getElementById('slipCount').innerText = keys.length + " Tercih Seçildi ▴";
        document.getElementById('slipOdds').innerText = "Toplam: " + total.toFixed(2);
        document.getElementById('couponList').innerHTML = listHtml;
    }

    function toggleModal() {
        const modal = document.getElementById('couponModal');
        modal.style.display = (modal.style.display === 'block') ? 'none' : 'block';
    }

    function clearCoupon() {
        myCoupon = {};
        updateSlip();
        if (activeMatchId) openMatch(activeMatchId);
        document.getElementById('couponModal').style.display = 'none';
    }

    function saveSlip() {
        if (Object.keys(myCoupon).length === 0) {
            alert("Lütfen kupona en az 1 oran seçiniz.");
            return;
        }
        alert("Kupon başarıyla hafızaya alındı!");
    }

    // AI Sohbet Motoru
    function handleEnter(e) {
        if (e.key === 'Enter') sendMsg();
    }

    function sendMsg() {
        const input = document.getElementById('chatInput');
        const text = input.value.trim();
        if (!text) return;

        const chat = document.getElementById('chatMsgs');
        chat.innerHTML += `<div class="msg-user">${text}</div>`;
        input.value = "";

        setTimeout(() => {
            let botReply = "Bu maçta model xG verilerine göre hücum varyasyonlarını güçlü buluyor. Özellikle ilk 30 dakikada tempo yüksek olabilir; canlıda 1.5 üst baremini yakından izleyebilirsin.";
            if (text.toLowerCase().includes("risk") || text.toLowerCase().includes("nasıl")) {
                botReply = "Matematiksel olarak +EV değeri pozitif. Ancak taraf bahsi yerine gol baremlerine (2.5 Üst veya KG) odaklanmak varyansı düşürür ortak.";
            }
            chat.innerHTML += `<div class="msg-bot">${botReply}</div>`;
            chat.scrollTop = chat.scrollHeight;
        }, 500);
    }
</script>
</body>
</html>
"""

components.html(app_html, height=850, scrolling=True)