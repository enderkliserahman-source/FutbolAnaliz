import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(layout="centered", initial_sidebar_state="collapsed", page_title="Futbol Analiz Masası")

DB_FILE = "database.json"

# Kalıcı Veritabanı Fonksiyonları
def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"user_preds": {}, "user_odds": {}, "revealed": {}, "chat_logs": {}, "cases": []}

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

PRESET_OPTIONS = [
    "Seçim Yapılmadı",
    "Ev Sahibi 1.5 Üst",
    "Deplasman 1.5 Üst",
    "2.5 Üst",
    "KG Var",
    "2.5 Üst & KG Var",
    "MS 1 & 1.5 Üst",
    "MS 2 & 1.5 Üst",
    "Ev Sahibi 2.5 Üst"
]

matches = [
    {"id": "1", "session": "Gündüz Seansı", "time": "13:00", "league": "Japonya J-League", "match": "Kashiwa Reysol — V-Varen Nagasaki", "model_market": "Ev Sahibi 1.5 Üst", "model_xg": "1.92 - 0.85", "confidence": "%76", "score_pred": "2-0 / 2-1"},
    {"id": "2", "session": "Gündüz Seansı", "time": "13:30", "league": "Japonya J-League", "match": "FC Tokyo — JEF United Chiba", "model_market": "2.5 Üst & KG Var", "model_xg": "1.68 - 1.15", "confidence": "%72", "score_pred": "2-1 / 1-2"},
    {"id": "3", "session": "Akşam Erken Seans", "time": "20:30", "league": "Avusturya Bundesliga", "match": "SV Ried — Grazer AK", "model_market": "2.5 Üst & KG Var", "model_xg": "1.75 - 1.35", "confidence": "%70", "score_pred": "2-1 / 2-2"},
    {"id": "4", "session": "Akşam Erken Seans", "time": "21:30", "league": "Trendyol Süper Lig", "match": "Erzurumspor — Galatasaray", "model_market": "Deplasman 1.5 Üst & MS 2", "model_xg": "0.65 - 2.10", "confidence": "%78", "score_pred": "0-2 / 1-3"},
    {"id": "5", "session": "Akşam Erken Seans", "time": "21:30", "league": "Trendyol 1. Lig", "match": "Fatih Karagümrük — Bursaspor", "model_market": "Ev Sahibi 1.5 Üst & KG Var", "model_xg": "1.80 - 1.20", "confidence": "%69", "score_pred": "2-1"},
    {"id": "6", "session": "Gece Ana Seansı", "time": "21:45", "league": "Fransa Ligue 1", "match": "Marsilya — Strasbourg", "model_market": "Ev Sahibi 1.5 Üst & 2.5 Üst", "model_xg": "2.30 - 0.90", "confidence": "%75", "score_pred": "2-1 / 3-1"},
    {"id": "7", "session": "Gece Ana Seansı", "time": "21:45", "league": "Belçika Pro League", "match": "Standard Liège — La Louvière", "model_market": "Ev Sahibi 1.5 Üst & MS 1", "model_xg": "2.05 - 0.70", "confidence": "%74", "score_pred": "2-0 / 3-0"},
    {"id": "8", "session": "Gece Ana Seansı", "time": "22:00", "league": "İngiltere Kupası", "match": "Arsenal — Coventry", "model_market": "Ev Sahibi 2.5 Üst", "model_xg": "2.85 - 0.40", "confidence": "%84", "score_pred": "3-0 / 4-0"},
    {"id": "9", "session": "Gece Ana Seansı", "time": "22:00", "league": "İspanya La Liga", "match": "Real Betis — Real Sociedad", "model_market": "KG Var", "model_xg": "1.45 - 1.30", "confidence": "%67", "score_pred": "1-1 / 2-1"}
]

tab1, tab2 = st.tabs(["🎯 Canlı İstişare Masası", "🔬 Vaka Analizi & Öğrenme"])

with tab1:
    st.markdown("<h2 style='color:#ffffff; margin:0;'>📋 Günün Bülteni & Analiz Masası</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:13px; margin-bottom:15px;'>🔒 Tercihini kilitleyip model raporunu aç; veriler otomatik olarak diskte saklanır.</p>", unsafe_allow_html=True)

    current_session = ""
    for m in matches:
        m_id = str(m["id"])
        
        if m["session"] != current_session:
            current_session = m["session"]
            st.markdown(f"<div style='margin-top:20px; margin-bottom:8px;'><span style='background:#2563eb; color:#ffffff; padding:4px 10px; border-radius:4px; font-size:12px; font-weight:bold;'>{current_session}</span></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#1e293b; border:1px solid #334155; border-left:5px solid #38bdf8; padding:12px; border-radius:8px; margin-bottom:8px;">
            <div style="display:flex; justify-content:space-between;">
                <span style="background:#0284c7; color:#ffffff; padding:2px 6px; border-radius:4px; font-size:11px; font-weight:bold;">{m['league']}</span>
                <span style="color:#cbd5e1; font-size:12px; font-weight:bold;">{m['time']}</span>
            </div>
            <h3 style="margin:6px 0 0 0; color:#ffffff; font-size:16px;">{m['match']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Seçim ve Oran Alanı
        col_sel, col_odd = st.columns([2, 1])
        with col_sel:
            saved_choice = data["user_preds"].get(m_id, "Seçim Yapılmadı")
            idx = PRESET_OPTIONS.index(saved_choice) if saved_choice in PRESET_OPTIONS else 0
            user_choice = st.selectbox(f"Tahminin ({m['match']}):", PRESET_OPTIONS, index=idx, key=f"sel_{m_id}")
        with col_odd:
            saved_odd = data["user_odds"].get(m_id, 1.50)
            user_odd = st.number_input("İddaa Oranı:", min_value=1.00, max_value=20.00, value=float(saved_odd), step=0.05, key=f"odd_{m_id}")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Tahminimi Kilitle 🔒", key=f"save_{m_id}"):
                data["user_preds"][m_id] = user_choice
                data["user_odds"][m_id] = user_odd
                save_data(data)
                st.toast("Diske kaydedildi!")
        with c2:
            if st.button("Model Raporunu Aç 📊", key=f"rev_{m_id}"):
                data["revealed"][m_id] = True
                save_data(data)
                st.rerun()

        # Model Raporu
        if data["revealed"].get(m_id, False):
            st.markdown(f"""
            <div style="background:#090d16; border:1px solid #334155; padding:10px; border-radius:6px; margin-top:6px;">
                <b style="color:#ffffff;">🤖 Model Sinyali:</b> <span style="color:#38bdf8; font-weight:bold; font-size:15px;">{m['model_market']}</span><br>
                <div style="color:#94a3b8; font-size:12px; margin-top:2px;">
                    xG: {m['model_xg']} &nbsp;|&nbsp; Güven: {m['confidence']} &nbsp;|&nbsp; Skor: {m['score_pred']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            cur_p = data["user_preds"].get(m_id, "Seçim Yapılmadı")
            if cur_p != "Seçim Yapılmadı":
                is_match = cur_p.lower() in m['model_market'].lower() or m['model_market'].lower() in cur_p.lower()
                status_color = "#22c55e" if is_match else "#eab308"
                status_label = "🟢 Tam Mutabakat (Ortak Karar)" if is_match else "🟡 İstişare Gerekli"
                
                st.markdown(f"""
                <div style="margin-top:6px; padding:6px 10px; border-radius:4px; background:{status_color}22; border-left:4px solid {status_color};">
                    <span style="color:{status_color}; font-weight:bold; font-size:12px;">{status_label}</span><br>
                    <small style="color:#ffffff;">Sen: <b>{cur_p} (@{data['user_odds'].get(m_id, '-')})</b> &nbsp;|&nbsp; Model: <b>{m['model_market']}</b></small>
                </div>
                """, unsafe_allow_html=True)

        # Canlı Tartışma Odası
        with st.expander("💬 Bu Maç İçin Canlı Tartışma"):
            logs = data["chat_logs"].get(m_id, [])
            for c in logs:
                st.markdown(f"""
                <div style="background:#1e3a8a; border:1px solid #3b82f6; padding:6px 10px; border-radius:6px; margin-bottom:4px; font-size:13px; color:#ffffff;">
                    <b>Sen ({c['time']}):</b> {c['msg']}
                </div>
                """, unsafe_allow_html=True)
            
            c_msg, c_snd = st.columns([3, 1])
            with c_msg:
                user_msg = st.text_input("Görüşünü Yaz:", key=f"chat_{m_id}", placeholder="Taktiksel not...")
            with c_snd:
                if st.button("Gönder", key=f"snd_{m_id}"):
                    if user_msg.strip():
                        if m_id not in data["chat_logs"]: data["chat_logs"][m_id] = []
                        data["chat_logs"][m_id].append({"time": datetime.now().strftime("%H:%M"), "msg": user_msg})
                        save_data(data)
                        st.rerun()

        st.divider()

with tab2:
    st.markdown("<h2 style='color:#ffffff;'>📚 Biten Maç Vaka Analizi</h2>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        v_match = st.selectbox("Maç Seç:", [m["match"] for m in matches])
        v_source = st.selectbox("Kaynak:", ["İnsan Sezgisi", "Model Sinyali", "Ortak Konsensüs"])
    with col_b:
        v_res = st.selectbox("Sonuç:", ["Başarılı", "Başarısız"])
        v_note = st.text_area("Taktiksel Not:", placeholder="Örn: Erken gol tempoyu artırdı...")

    if st.button("Vakayı Sisteme Kaydet 💾"):
        if v_match:
            data["cases"].append({"match": v_match, "source": v_source, "res": v_res, "note": v_note})
            save_data(data)
            st.success("Vaka diske kaydedildi!")
            st.rerun()

    st.markdown("---")
    if data["cases"]:
        for c in reversed(data["cases"]):
            color = "#22c55e" if c['res'] == "Başarılı" else "#ef4444"
            st.markdown(f"""
            <div style="background:#1e293b; border-left:4px solid {color}; padding:8px 12px; border-radius:6px; margin-bottom:8px;">
                <b style="color:#ffffff;">{c['match']}</b> — <span style="color:{color}; font-weight:bold;">{c['res']}</span> ({c['source']})<br>
                <small style="color:#cbd5e1;">{c['note']}</small>
            </div>
            """, unsafe_allow_html=True)