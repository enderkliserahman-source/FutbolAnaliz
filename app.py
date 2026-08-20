import streamlit as st
import streamlit.components.v1 as components
import json

# Mobil Sayfa Ayarı
st.set_page_config(
    page_title="Futbol Analiz",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Kupon Hafızası
if "selected_bets" not in st.session_state:
    st.session_state.selected_bets = {}

# Özel CSS: Ekrana %100 Kilitleme ve Sıfır Kayma
st.markdown("""
<style>
    /* Sağa Kaymayı (Horizontal Scroll) Kesin Olarak Engelle */
    html, body, [class*="css"], .stApp {
        overflow-x: hidden !important;
        max-width: 100vw !important;
        background-color: #f1f5f9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    .block-container {
        padding: 0.5rem 0.5rem 5rem 0.5rem !important;
        max-width: 100% !important;
    }

    /* Üst Maç Başlık Alanı */
    .header-box {
        background: #0f2438;
        color: #ffffff;
        padding: 12px 10px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }
    .header-time {
        font-size: 0.75rem;
        color: #94a3b8;
    }
    .header-league {
        font-size: 0.72rem;
        color: #38bdf8;
        font-weight: 700;
        text-transform: uppercase;
        margin: 2px 0 4px 0;
    }
    .header-teams {
        font-size: 1.05rem;
        font-weight: 800;
    }

    /* Alt Sabit Kupon Barı */
    .bottom-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #0f2438;
        color: white;
        padding: 10px 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 3px solid #e63946;
        z-index: 999999;
        box-sizing: border-box;
    }
</style>
""", unsafe_allow_html=True)

# Üst Başlık Kartı
st.markdown("""
<div class="header-box">
    <div class="header-time">Bugün 20:00</div>
    <div class="header-league">UEFA Avrupa Konferans Ligi, Playoff</div>
    <div class="header-teams">Nordsjælland — St. Gallen</div>
</div>
""", unsafe_allow_html=True)

# Sekmeler
tab_oranlar, tab_istatistik, tab_simulasyon = st.tabs(["📌 Oranlar", "📊 Model İstatistikleri", "🎲 Simülasyon"])

with tab_oranlar:
    # Nesine Arayüzünün Birebir HTML/JS Render Motoru
    # Bu blok mobilde asla sağa taşmaz, ekrana tam yapışır ve tıklandığında kırmızıya boyanır.
    
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background-color: #f1f5f9; padding: 2px; }
        
        .market-header {
            background: #cfe2f3;
            color: #0f2438;
            font-size: 11px;
            font-weight: 800;
            padding: 5px 8px;
            border-radius: 5px;
            margin: 8px 0 4px 0;
            display: flex;
            align-items: center;
        }
        .badge {
            background: #e63946;
            color: white;
            font-size: 10px;
            padding: 1px 4px;
            border-radius: 3px;
            margin-right: 5px;
            font-weight: bold;
        }
        
        .row-card {
            display: grid;
            grid-template-columns: 1.4fr 1fr 1fr 1fr;
            align-items: center;
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 5px 6px;
            margin-bottom: 4px;
            gap: 4px;
        }
        
        .row-card-2 {
            display: grid;
            grid-template-columns: 1.4fr 1.5fr 1.5fr;
            align-items: center;
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 5px 6px;
            margin-bottom: 4px;
            gap: 5px;
        }
        
        .row-title {
            font-size: 12px;
            font-weight: 700;
            color: #1e293b;
            padding-left: 2px;
        }
        
        .btn-box {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: #1e3a5f;
            color: #ffffff;
            border-radius: 6px;
            padding: 4px 0;
            min-height: 36px;
            cursor: pointer;
            user-select: none;
            transition: background 0.15s ease;
        }
        
        .btn-box .label {
            font-size: 9px;
            color: #94a3b8;
            font-weight: 600;
            line-height: 1;
            margin-bottom: 2px;
        }
        
        .btn-box .odd {
            font-size: 12px;
            font-weight: 800;
            line-height: 1;
        }
        
        /* Seçildiğinde Canlı Kırmızı Vurgu */
        .btn-box.selected {
            background: #e63946 !important;
            color: #ffffff !important;
        }
        .btn-box.selected .label {
            color: #ffccd5 !important;
        }
    </style>
    </head>
    <body>

        <!-- 1. MAÇ SONUCU -->
        <div class="market-header"><span class="badge">1</span> MAÇ SONUCU</div>
        <div class="row-card">
            <div class="row-title">📌 Maç Sonucu</div>
            <div class="btn-box" onclick="toggle(this, 'MS', '1', 1.37)">
                <span class="label">MS 1</span>
                <span class="odd">1.37</span>
            </div>
            <div class="btn-box" onclick="toggle(this, 'MS', 'X', 4.36)">
                <span class="label">MS X</span>
                <span class="odd">4.36</span>
            </div>
            <div class="btn-box" onclick="toggle(this, 'MS', '2', 4.59)">
                <span class="label">MS 2</span>
                <span class="odd">4.59</span>
            </div>
        </div>

        <!-- 2. ÇİFTE ŞANS -->
        <div class="market-header"><span class="badge">1</span> ÇİFTE ŞANS</div>
        <div class="row-card">
            <div class="row-title">📌 Çifte Şans</div>
            <div class="btn-box" onclick="toggle(this, 'ÇŞ', '1-X', 1.05)">
                <span class="label">ÇŞ 1-X</span>
                <span class="odd">1.05</span>
            </div>
            <div class="btn-box" onclick="toggle(this, 'ÇŞ', '1-2', 1.07)">
                <span class="label">ÇŞ 1-2</span>
                <span class="odd">1.07</span>
            </div>
            <div class="btn-box" onclick="toggle(this, 'ÇŞ', 'X-2', 2.17)">
                <span class="label">ÇŞ X-2</span>
                <span class="odd">2.17</span>
            </div>
        </div>

        <!-- 3. TOPLAM GOL (2.5) -->
        <div class="market-header"><span class="badge">1</span> TOPLAM GOL (2.5)</div>
        <div class="row-card-2">
            <div class="row-title">📌 2.5 Alt/Üst</div>
            <div class="btn-box" onclick="toggle(this, '2.5', 'Alt', 2.15)">
                <span class="label">Alt</span>
                <span class="odd">2.15</span>
            </div>
            <div class="btn-box" onclick="toggle(this, '2.5', 'Üst', 1.52)">
                <span class="label">Üst</span>
                <span class="odd">1.52</span>
            </div>
        </div>

        <!-- 4. KARŞILIKLI GOL -->
        <div class="market-header"><span class="badge">1</span> KARŞILIKLI GOL</div>
        <div class="row-card-2">
            <div class="row-title">📌 KG Var/Yok</div>
            <div class="btn-box" onclick="toggle(this, 'KG', 'Var', 1.48)">
                <span class="label">Var</span>
                <span class="odd">1.48</span>
            </div>
            <div class="btn-box" onclick="toggle(this, 'KG', 'Yok', 2.10)">
                <span class="label">Yok</span>
                <span class="odd">2.10</span>
            </div>
        </div>

        <script>
            function toggle(el, m, p, o) {
                el.classList.toggle('selected');
            }
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=360, scrolling=False)

with tab_istatistik:
    st.info("🎯 **Model Tercihi:** MS 1 & 2.5 Üst (%9.4 +EV Avantajı)")
    st.metric("Beklenen Gol (xG)", "Nordsjælland: 2.14 — St. Gallen: 0.88")
    st.progress(74, text="Model Güven Skoru: %74")

with tab_simulasyon:
    st.write("🎲 **10.000 Maç Simülasyon Çıktısı:**")
    c1, c2, c3 = st.columns(3)
    c1.metric("1", "%64.2")
    c2.metric("X", "%20.5")
    c3.metric("2", "%15.3")

# Alt Kupon Çubuğu
st.markdown("""
<div class="bottom-bar">
    <div>
        <span style="font-size:0.75rem; color:#94a3b8;">Canlı Kupon</span><br>
        <span style="font-size:1.05rem; font-weight:800; color:#38bdf8;">Oran: 1.37</span>
    </div>
    <div style="background:#e63946; padding:6px 14px; border-radius:6px; font-weight:bold; font-size:0.85rem; cursor:pointer;">
        Kuponu İncele ➔
    </div>
</div>
""", unsafe_allow_html=True)