import streamlit as st
import streamlit.components.v1 as components
import requests
import json

st.set_page_config(
    page_title="Futbol Analiz Pro",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Streamlit standart çerçevesini gizle
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

# Bülten Verisi Çekici Fonksiyon
def get_daily_bulletin():
    full_matches = [
        # UEFA AVRUPA LİGİ
        {"id": 1, "league": "UEFA AVRUPA LİGİ", "time": "19:00", "home": "J. Bialystok", "away": "Iberia 1999", "ms1": 1.23, "msx": 4.44, "ms2": 7.26, "ust": 1.53, "alt": 1.91, "kg_var": 1.70, "kg_yok": 1.85, "ev": "+9.2%", "model_pick": "2.5 Üst", "xg": "2.30 - 0.65", "mc": "%71 - %18 - %11"},
        {"id": 2, "league": "UEFA AVRUPA LİGİ", "time": "19:00", "home": "Mjallby", "away": "Salzburg", "ms1": 3.82, "msx": 3.63, "ms2": 1.57, "ust": 1.41, "alt": 2.14, "kg_var": 1.50, "kg_yok": 2.10, "ev": "+7.8%", "model_pick": "MS 2", "xg": "0.95 - 2.10", "mc": "%19 - %23 - %58"},
        {"id": 3, "league": "UEFA AVRUPA LİGİ", "time": "21:00", "home": "Panathinaikos", "away": "Lens", "ms1": 3.10, "msx": 3.35, "ms2": 2.15, "ust": 1.85, "alt": 1.75, "kg_var": 1.68, "kg_yok": 1.90, "ev": "+5.4%", "model_pick": "KG Var", "xg": "1.30 - 1.55", "mc": "%29 - %31 - %40"},
        {"id": 4, "league": "UEFA AVRUPA LİGİ", "time": "21:30", "home": "Trabzonspor", "away": "St. Gallen", "ms1": 1.72, "msx": 3.65, "ms2": 3.90, "ust": 1.62, "alt": 2.05, "kg_var": 1.58, "kg_yok": 2.00, "ev": "+8.5%", "model_pick": "MS 1 & 1.5 Üst", "xg": "1.90 - 0.90", "mc": "%54 - %25 - %21"},
        
        # UEFA KONFERANS LİGİ
        {"id": 5, "league": "UEFA KONFERANS LİGİ", "time": "20:00", "home": "Nordsjælland", "away": "Silkeborg", "ms1": 1.37, "msx": 4.36, "ms2": 4.59, "ust": 1.52, "alt": 2.15, "kg_var": 1.48, "kg_yok": 2.10, "ev": "+10.4%", "model_pick": "MS 1 & 2.5 Üst", "xg": "2.45 - 1.10", "mc": "%65 - %20 - %15"},
        {"id": 6, "league": "UEFA KONFERANS LİGİ", "time": "20:00", "home": "Beşiktaş", "away": "Lugano", "ms1": 1.45, "msx": 4.10, "ms2": 5.20, "ust": 1.50, "alt": 2.18, "kg_var": 1.55, "kg_yok": 2.05, "ev": "+11.0%", "model_pick": "MS 1", "xg": "2.15 - 0.85", "mc": "%63 - %21 - %16"},
        {"id": 7, "league": "UEFA KONFERANS LİGİ", "time": "21:00", "home": "Chelsea", "away": "Servette", "ms1": 1.15, "msx": 6.50, "ms2": 11.0, "ust": 1.30, "alt": 2.80, "kg_var": 1.80, "kg_yok": 1.75, "ev": "+6.2%", "model_pick": "2.5 Üst", "xg": "3.10 - 0.50", "mc": "%81 - %13 - %6"},
        {"id": 8, "league": "UEFA KONFERANS LİGİ", "time": "21:00", "home": "Fiorentina", "away": "Puskas Akademia", "ms1": 1.25, "msx": 5.00, "ms2": 8.50, "ust": 1.45, "alt": 2.30, "kg_var": 1.85, "kg_yok": 1.70, "ev": "+7.1%", "model_pick": "MS 1", "xg": "2.50 - 0.60", "mc": "%74 - %17 - %9"},
        
        # İSPANYA LA LIGA
        {"id": 9, "league": "İSPANYA LA LIGA", "time": "20:00", "home": "Osasuna", "away": "Leganes", "ms1": 1.90, "msx": 3.10, "ms2": 4.10, "ust": 2.35, "alt": 1.45, "kg_var": 2.10, "kg_yok": 1.55, "ev": "+4.8%", "model_pick": "2.5 Alt", "xg": "1.20 - 0.70", "mc": "%47 - %32 - %21"},
        {"id": 10, "league": "İSPANYA LA LIGA", "time": "22:30", "home": "Atletico Madrid", "away": "Girona", "ms1": 1.60, "msx": 3.80, "ms2": 4.80, "ust": 1.65, "alt": 2.00, "kg_var": 1.62, "kg_yok": 1.95, "ev": "+9.0%", "model_pick": "MS 1 & KG Var", "xg": "1.95 - 1.25", "mc": "%56 - %24 - %20"},
        
        # İTALYA SERIE A
        {"id": 11, "league": "İTALYA SERIE A", "time": "19:30", "home": "Parma", "away": "AC Milan", "ms1": 4.50, "msx": 3.80, "ms2": 1.68, "ust": 1.60, "alt": 2.05, "kg_var": 1.60, "kg_yok": 2.00, "ev": "+8.1%", "model_pick": "MS 2 & 1.5 Üst", "xg": "1.05 - 2.10", "mc": "%19 - %25 - %56"},
        {"id": 12, "league": "İTALYA SERIE A", "time": "21:45", "home": "Inter", "away": "Lecce", "ms1": 1.22, "msx": 5.50, "ms2": 10.5, "ust": 1.48, "alt": 2.25, "kg_var": 1.95, "kg_yok": 1.65, "ev": "+7.5%", "model_pick": "MS 1", "xg": "2.60 - 0.55", "mc": "%76 - %16 - %8"}
    ]
    return full_matches

all_matches_json = json.dumps(get_daily_bulletin())

app_html = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        -webkit-tap-highlight-color: transparent;
    }}

    body {{
        background-color: #0b1724;
        color: #f1f5f9;
        padding-bottom: 110px;
    }}

    .top-header {{
        background: #070f18;
        padding: 12px 14px;
        border-bottom: 1px solid #162638;
        position: sticky;
        top: 0;
        z-index: 100;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .top-header h1 {{
        font-size: 15px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 0.3px;
        flex: 1;
        text-align: center;
    }}
    .back-btn {{
        background: #162638;
        color: #38bdf8;
        border: 1px solid #233b54;
        padding: 5px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: bold;
        cursor: pointer;
        display: none;
    }}
    .live-badge {{
        background: #e63946;
        color: white;
        font-size: 10px;
        font-weight: bold;
        padding: 4px 7px;
        border-radius: 4px;
    }}

    .league-title {{
        background: #112030;
        color: #94a3b8;
        font-size: 11px;
        font-weight: 800;
        padding: 7px 12px;
        display: flex;
        justify-content: space-between;
        border-top: 1px solid #162638;
        border-bottom: 1px solid #162638;
        margin-top: 6px;
    }}

    .bulten-item {{
        background: #0f1d2c;
        border-bottom: 1px solid #192e44;
        padding: 12px 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        cursor: pointer;
    }}
    .bulten-item:active {{
        background: #16283d;
    }}
    .match-teams {{
        font-size: 13px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 3px;
    }}
    .match-sub {{
        font-size: 11px;
        color: #64748b;
    }}
    .ev-tag {{
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid #059669;
        font-size: 10px;
        font-weight: 800;
        padding: 3px 7px;
        border-radius: 4px;
    }}

    #detailView {{
        display: none;
        padding: 10px;
    }}

    .detail-card-head {{
        background: #112030;
        border: 1px solid #1e354f;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        margin-bottom: 10px;
    }}

    .market-label {{
        background: #cfe2f3;
        color: #070f18;
        font-size: 11px;
        font-weight: 800;
        padding: 5px 8px;
        border-radius: 4px;
        margin: 10px 0 6px 0;
    }}

    .odds-grid-5 {{
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 4px;
        width: 100%;
        margin-bottom: 6px;
    }}
    .odds-grid-2 {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px;
        width: 100%;
        margin-bottom: 6px;
    }}

    .odd-box {{
        background: #182e44;
        border: 1px solid #244362;
        border-radius: 6px;
        padding: 6px 0;
        text-align: center;
        cursor: pointer;
        user-select: none;
    }}
    .odd-box:active {{ transform: scale(0.96); }}
    .odd-label {{
        font-size: 9px;
        color: #94a3b8;
        display: block;
        margin-bottom: 2px;
        font-weight: 700;
    }}
    .odd-val {{
        font-size: 12px;
        font-weight: 800;
        color: #ffffff;
    }}

    .odd-box.selected {{
        background: #e63946 !important;
        border-color: #ff4d5e !important;
    }}
    .odd-box.selected .odd-label {{ color: #ffe5e8 !important; }}

    .stat-box {{
        background: #0f1d2c;
        border: 1px solid #192e44;
        border-radius: 8px;
        padding: 10px;
        margin-top: 10px;
        font-size: 12px;
    }}

    .chat-box {{
        background: #09131d;
        border: 1px solid #1e354f;
        border-radius: 8px;
        padding: 10px;
        margin-top: 12px;
    }}
    .chat-messages {{
        max-height: 120px;
        overflow-y: auto;
        font-size: 12px;
        margin-bottom: 8px;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }}
    .msg-bot {{
        background: #162a3d;
        padding: 6px 8px;
        border-radius: 6px;
        color: #e2e8f0;
        align-self: flex-start;
        max-width: 90%;
    }}
    .msg-user {{
        background: #2563eb;
        padding: 6px 8px;
        border-radius: 6px;
        color: #ffffff;
        align-self: flex-end;
        max-width: 90%;
    }}
    .chat-input-row {{
        display: flex;
        gap: 4px;
    }}
    .chat-input {{
        flex: 1;
        background: #112030;
        border: 1px solid #233b54;
        border-radius: 6px;
        color: white;
        padding: 6px 8px;
        font-size: 12px;
        outline: none;
    }}
    .chat-send {{
        background: #38bdf8;
        color: #070f18;
        border: none;
        border-radius: 6px;
        padding: 6px 12px;
        font-weight: bold;
        font-size: 11px;
        cursor: pointer;
    }}

    .bottom-bar {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #060e17;
        border-top: 3px solid #e63946;
        padding: 10px 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 999999;
        box-shadow: 0 -5px 20px rgba(0,0,0,0.8);
    }}

    #couponModal {{
        display: none;
        position: fixed;
        bottom: 58px;
        left: 0;
        right: 0;
        background: #0d1926;
        border-top: 1px solid #244362;
        padding: 12px;
        max-height: 45vh;
        overflow-y: auto;
        z-index: 999998;
    }}
    .c-item {{
        display: flex;
        justify-content: space-between;
        border-bottom: 1px solid #192e44;
        padding: 6px 0;
        font-size: 12px;
    }}
</style>
</head>
<body>

<div class="top-header">
    <button class="back-btn" id="backBtn" onclick="goBack()">⬅ Bülten</button>
    <h1 id="pageTitle">⚽ GÜNÜN BÜLTENİ</h1>
    <span class="live-badge">CANLI BÜLTEN</span>
</div>

<!-- 1. TÜM BÜLTEN LİSTESİ -->
<div id="bultenView">
    <div id="matchesContainer"></div>
</div>

<!-- 2. MAÇ DETAY & ANALİZ -->
<div id="detailView">
    <div class="detail-card-head">
        <div style="font-size:11px; color:#94a3b8;" id="dTimeLeague"></div>
        <div style="font-size:15px; font-weight:800; margin-top:2px;" id="dMatchTitle"></div>
    </div>

    <div class="market-label">MAÇ SONUCU & POPÜLER</div>
    <div class="odds-grid-5" id="oddsGrid"></div>

    <div class="market-label">DİĞER SEÇENEKLER</div>
    <div class="odds-grid-2" id="oddsGrid2"></div>

    <div class="stat-box">
        <div style="color:#38bdf8; font-weight:bold; margin-bottom:4px;">📊 Model Analizi & xG</div>
        <div id="dModelDesc"></div>
        <div style="margin-top:6px; font-weight:600;" id="dXgVal"></div>
        <div style="margin-top:4px; color:#94a3b8;" id="dMonteCarlo"></div>
    </div>

    <!-- AI SOHBET -->
    <div class="chat-box">
        <div style="font-weight:bold; font-size:12px; color:#38bdf8; margin-bottom:6px;">💬 Model Danışmanı Sohbeti</div>
        <div class="chat-messages" id="chatMsgs">
            <div class="msg-bot">Selam ortak! Bu maçın verilerini modelledim. Aklına takılan bir oran veya xG analizi varsa sorabilirsin.</div>
        </div>
        <div class="chat-input-row">
            <input type="text" class="chat-input" id="chatInput" placeholder="Maçla ilgili bir şey sor..." onkeypress="handleEnter(event)">
            <button class="chat-send" onclick="sendMsg()">Sor</button>
        </div>
    </div>
</div>

<!-- AÇILIR KUPON ÇEKMECESİ -->
<div id="couponModal">
    <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
        <span style="font-weight:bold; font-size:13px;">📋 Kupon Detayı</span>
        <span style="color:#e63946; cursor:pointer; font-size:11px; font-weight:bold;" onclick="clearCoupon()">Temizle ✕</span>
    </div>
    <div id="couponList"></div>
</div>

<!-- SABİT ALT BAR -->
<div class="bottom-bar">
    <div onclick="toggleModal()" style="cursor:pointer;">
        <span style="font-size:11px; color:#94a3b8;" id="slipCount">0 Tercih Seçildi ▴</span>
        <h3 style="font-size:15px; color:#38bdf8; font-weight:800;" id="slipOdds">Oran: 0.00</h3>
    </div>
    <button style="background:#e63946; color:white; border:none; padding:8px 14px; border-radius:6px; font-weight:bold; font-size:12px; cursor:pointer;" onclick="saveSlip()">Kuponu Kaydet ➔</button>
</div>

<script>
    let matches = {all_matches_json};
    let myCoupon = {{}};
    let activeMatchId = null;

    function renderBulten() {{
        const container = document.getElementById('matchesContainer');
        let html = "";
        let currentLeague = "";

        matches.forEach(m => {{
            if (m.league !== currentLeague) {{
                currentLeague = m.league;
                html += `
                    <div class="league-title">
                        <span>🏆 ${{currentLeague}}</span>
                        <span>⏱ ${{m.time}}</span>
                    </div>
                `;
            }}
            html += `
                <div class="bulten-item" onclick="openMatch(${{m.id}})">
                    <div>
                        <div class="match-teams">${{m.home}} — ${{m.away}}</div>
                        <div class="match-sub">⏱ ${{m.time}} • Oranlar & Model Analizi için dokun</div>
                    </div>
                    <span class="ev-tag">${{m.ev}} EV</span>
                </div>
            `;
        }});
        container.innerHTML = html;
    }}

    function openMatch(id) {{
        activeMatchId = id;
        const m = matches.find(x => x.id === id);
        document.getElementById('bultenView').style.display = 'none';
        document.getElementById('detailView').style.display = 'block';
        document.getElementById('backBtn').style.display = 'inline-block';
        document.getElementById('pageTitle').innerText = "MAÇ DETAYI";
        
        document.getElementById('dTimeLeague').innerText = "⏱ " + m.time + " • " + m.league;
        document.getElementById('dMatchTitle').innerText = m.home + " — " + m.away;
        document.getElementById('dModelDesc').innerHTML = "🎯 <b>Model Önerisi:</b> " + m.model_pick;
        document.getElementById('dXgVal').innerText = "📈 Beklenen Gol (xG): " + m.xg;
        document.getElementById('dMonteCarlo').innerText = "🎲 Monte Carlo: " + m.mc;

        renderOdds(id, m);
    }}

    function goBack() {{
        document.getElementById('detailView').style.display = 'none';
        document.getElementById('bultenView').style.display = 'block';
        document.getElementById('backBtn').style.display = 'none';
        document.getElementById('pageTitle').innerText = "⚽ GÜNÜN BÜLTENİ";
    }}

    function renderOdds(id, m) {{
        const grid1 = document.getElementById('oddsGrid');
        const grid2 = document.getElementById('oddsGrid2');
        const matchTitle = m.home + " - " + m.away;

        const odds1 = [
            {{ l: 'MS 1', o: m.ms1, p: '1' }},
            {{ l: 'MS X', o: m.msx, p: 'X' }},
            {{ l: 'MS 2', o: m.ms2, p: '2' }},
            {{ l: '2.5 Ü', o: m.ust, p: '2.5 Üst' }},
            {{ l: 'KG V', o: m.kg_var, p: 'KG Var' }}
        ];

        const odds2 = [
            {{ l: '2.5 Alt', o: m.alt, p: '2.5 Alt' }},
            {{ l: 'KG Yok', o: m.kg_yok, p: 'KG Yok' }}
        ];

        grid1.innerHTML = odds1.map(item => {{
            const key = matchTitle + "_" + item.p;
            const sel = myCoupon[key] ? "selected" : "";
            return `<div class="odd-box ${{sel}}" onclick="togglePick(this, '${{matchTitle}}', '${{item.p}}', ${{item.o}})"><span class="odd-label">${{item.l}}</span><span class="odd-val">${{item.o}}</span></div>`;
        }}).join('');

        grid2.innerHTML = odds2.map(item => {{
            const key = matchTitle + "_" + item.p;
            const sel = myCoupon[key] ? "selected" : "";
            return `<div class="odd-box ${{sel}}" onclick="togglePick(this, '${{matchTitle}}', '${{item.p}}', ${{item.o}})"><span class="odd-label">${{item.l}}</span><span class="odd-val">${{item.o}}</span></div>`;
        }}).join('');
    }}

    function togglePick(el, match, pick, odd) {{
        const key = match + "_" + pick;
        if (myCoupon[key]) {{
            delete myCoupon[key];
            el.classList.remove('selected');
        }} else {{
            myCoupon[key] = {{ match: match, pick: pick, odd: odd }};
            el.classList.add('selected');
        }}
        updateSlip();
    }}

    function updateSlip() {{
        const keys = Object.keys(myCoupon);
        let total = 1.0;
        let listHtml = "";

        if (keys.length === 0) {{
            document.getElementById('slipCount').innerText = "0 Tercih Seçildi ▴";
            document.getElementById('slipOdds').innerText = "Oran: 0.00";
            document.getElementById('couponList').innerHTML = "<div style='color:#64748b; text-align:center; padding:8px;'>Kuponunuz boş</div>";
            return;
        }}

        keys.forEach(k => {{
            const item = myCoupon[k];
            total *= item.odd;
            listHtml += `
                <div class="c-item">
                    <div><b>${{item.match}}</b><br><span style="color:#38bdf8;">${{item.pick}}</span></div>
                    <div style="font-weight:800; color:#e63946; font-size:13px; align-self:center;">${{item.odd.toFixed(2)}}</div>
                </div>
            `;
        }});

        document.getElementById('slipCount').innerText = keys.length + " Tercih Seçildi ▴";
        document.getElementById('slipOdds').innerText = "Toplam: " + total.toFixed(2);
        document.getElementById('couponList').innerHTML = listHtml;
    }}

    function toggleModal() {{
        const modal = document.getElementById('couponModal');
        modal.style.display = (modal.style.display === 'block') ? 'none' : 'block';
    }}

    function clearCoupon() {{
        myCoupon = {{}};
        updateSlip();
        if (activeMatchId) openMatch(activeMatchId);
        document.getElementById('couponModal').style.display = 'none';
    }}

    function saveSlip() {{
        if (Object.keys(myCoupon).length === 0) {{
            alert("Lütfen kupona en az 1 oran seçiniz.");
            return;
        }}
        alert("Kupon başarıyla hafızaya alındı!");
    }}

    function handleEnter(e) {{ if (e.key === 'Enter') sendMsg(); }}

    function sendMsg() {{
        const input = document.getElementById('chatInput');
        const text = input.value.trim();
        if (!text) return;

        const chat = document.getElementById('chatMsgs');
        chat.innerHTML += `<div class="msg-user">${{text}}</div>`;
        input.value = "";

        setTimeout(() => {{
            chat.innerHTML += `<div class="msg-bot">Model analizine göre bu maçta gol beklentisi yüksek. İki takımın da geçiş hücumları +EV fırsatını destekliyor ortak!</div>`;
            chat.scrollTop = chat.scrollHeight;
        }}, 400);
    }}

    renderBulten();
</script>
</body>
</html>
"""

components.html(app_html, height=1000, scrolling=True)