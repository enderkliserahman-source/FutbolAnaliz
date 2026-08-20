import pandas as pd
import numpy as np
from scipy.stats import poisson

class BulletinScanner:
    def __init__(self):
        pass

    def get_live_bulletin(self):
        matches = [
            {
                "id": 101,
                "lig": "UEFA Şampiyonlar Ligi",
                "ev": "Slovan Bratislava",
                "dep": "NK Celje",
                "ms1_oran": 1.95,
                "ms0_oran": 3.38,
                "ms2_oran": 3.40,
                "ust25_oran": 1.78,
                "kg_var_oran": 1.70,
                "ev_xg": 1.65,
                "dep_xg": 1.05
            },
            {
                "id": 102,
                "lig": "Avrupa Ligi / Hazırlık",
                "ev": "NEC Nijmegen",
                "dep": "Bodo Glimt",
                "ms1_oran": 2.65,
                "ms0_oran": 3.53,
                "ms2_oran": 2.20,
                "ust25_oran": 1.62,
                "kg_var_oran": 1.55,
                "ev_xg": 1.30,
                "dep_xg": 1.75
            },
            {
                "id": 103,
                "lig": "UEFA Konferans Ligi",
                "ev": "Hapoel Beer Sheva",
                "dep": "Sabah",
                "ms1_oran": 1.75,
                "ms0_oran": 3.07,
                "ms2_oran": 4.10,
                "ust25_oran": 2.10,
                "kg_var_oran": 1.90,
                "ev_xg": 1.55,
                "dep_xg": 0.75
            },
            {
                "id": 104,
                "lig": "UEFA Şampiyonlar Ligi",
                "ev": "Celtic",
                "dep": "LASK",
                "ms1_oran": 1.52,
                "ms0_oran": 3.69,
                "ms2_oran": 4.80,
                "ust25_oran": 1.58,
                "kg_var_oran": 1.72,
                "ev_xg": 2.20,
                "dep_xg": 0.90
            },
            {
                "id": 105,
                "lig": "İspanya La Liga / Kupa",
                "ev": "Atletico Madrid",
                "dep": "Malaga CF",
                "ms1_oran": 1.25,
                "ms0_oran": 4.80,
                "ms2_oran": 9.50,
                "ust25_oran": 1.65,
                "kg_var_oran": 2.15,
                "ev_xg": 1.90,
                "dep_xg": 0.55
            }
        ]
        return matches

    def scan_all(self, max_goals=6):
        matches = self.get_live_bulletin()
        results = []

        for m in matches:
            h_lambda = m["ev_xg"]
            a_lambda = m["dep_xg"]

            # Poisson Matrisi
            h_probs = [poisson.pmf(i, h_lambda) for i in range(max_goals)]
            a_probs = [poisson.pmf(i, a_lambda) for i in range(max_goals)]
            matrix = np.outer(h_probs, a_probs)

            # Saf Olasılıklar
            prob_1 = np.sum(np.tril(matrix, -1))
            prob_0 = np.sum(np.diag(matrix))
            prob_2 = np.sum(np.triu(matrix, 1))
            prob_over25 = sum(matrix[h, a] for h in range(max_goals) for a in range(max_goals) if h + a > 2.5)
            prob_btts = sum(matrix[h, a] for h in range(1, max_goals) for a in range(1, max_goals))

            # Seçenekler Havuzu (Olasılık, Oran)
            market = {
                "MS 1": (prob_1, m["ms1_oran"]),
                "MS 0": (prob_0, m["ms0_oran"]),
                "MS 2": (prob_2, m["ms2_oran"]),
                "2.5 Üst": (prob_over25, m["ust25_oran"]),
                "KG Var": (prob_btts, m["kg_var_oran"])
            }

            # 1. En Yüksek İhtimal (Modelin Bankosu)
            most_likely_pick = max(market, key=lambda k: market[k][0])
            ml_prob, ml_odd = market[most_likely_pick]

            # 2. En Değerli Tercih (+EV Avcısı)
            ev_dict = {k: (v[0] * v[1]) - 1 for k, v in market.items()}
            best_ev_pick = max(ev_dict, key=lambda k: ev_dict[k])
            best_ev_val = ev_dict[best_ev_pick]
            best_ev_odd = market[best_ev_pick][1]
            best_ev_prob = market[best_ev_pick][0]

            # Yorum & Değerlendirme
            if ml_prob >= 0.65:
                taktik = f"🔥 {most_likely_pick} Çok Güçlü (Net Favori)"
            elif best_ev_val > 0:
                taktik = f"💎 {best_ev_pick} Değerli Oran (+EV Fırsatı)"
            else:
                taktik = f"⚖️ {most_likely_pick} Dengeli / Oran Sıkışık"

            results.append({
                "Lig": m["lig"],
                "Karşılaşma": f"{m['ev']} - {m['dep']}",
                "Model xG": f"{h_lambda:.2f} : {a_lambda:.2f}",
                "Modelin Bankosu": f"{most_likely_pick} (%{ml_prob*100:.1f})",
                "Banko Oranı": ml_odd,
                "Fırsat / Değerli Tercih": f"{best_ev_pick} ({best_ev_odd})",
                "+EV Avantajı": f"+%{best_ev_val*100:.1f}" if best_ev_val > 0 else f"%{best_ev_val*100:.1f}",
                "Taktiksel Yorum": taktik
            })

        return pd.DataFrame(results)