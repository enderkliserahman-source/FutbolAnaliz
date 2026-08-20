import pandas as pd

class LeagueData:
    def __init__(self):
        # Süper Lig + Bülten Maçlarındaki Takımların Hücum/Savunma Profilleri
        self.teams_data = {
            # Süper Lig Takımları
            "Galatasaray": {"OM_Ic": 12, "IA": 32, "IY": 9, "OM_Dis": 12, "DA": 28, "DY": 10},
            "Fenerbahçe": {"OM_Ic": 12, "IA": 30, "IY": 11, "OM_Dis": 12, "DA": 25, "DY": 11},
            "Beşiktaş": {"OM_Ic": 12, "IA": 22, "IY": 14, "OM_Dis": 12, "DA": 18, "DY": 15},
            "Trabzonspor": {"OM_Ic": 12, "IA": 20, "IY": 12, "OM_Dis": 12, "DA": 16, "DY": 16},
            "Başakşehir": {"OM_Ic": 12, "IA": 19, "IY": 15, "OM_Dis": 12, "DA": 15, "DY": 17},
            "Samsunspor": {"OM_Ic": 12, "IA": 18, "IY": 13, "OM_Dis": 12, "DA": 14, "DY": 16},
            "Eyüpspor": {"OM_Ic": 12, "IA": 17, "IY": 14, "OM_Dis": 12, "DA": 13, "DY": 15},
            "Göztepe": {"OM_Ic": 12, "IA": 18, "IY": 12, "OM_Dis": 12, "DA": 12, "DY": 17},
            "Gaziantep FK": {"OM_Ic": 12, "IA": 16, "IY": 15, "OM_Dis": 12, "DA": 11, "DY": 20},
            "Kasımpaşa": {"OM_Ic": 12, "IA": 15, "IY": 18, "OM_Dis": 12, "DA": 14, "DY": 19},
            "Sivasspor": {"OM_Ic": 12, "IA": 14, "IY": 16, "OM_Dis": 12, "DA": 12, "DY": 21},
            "Antalyaspor": {"OM_Ic": 12, "IA": 15, "IY": 17, "OM_Dis": 12, "DA": 11, "DY": 22},
            "Konyaspor": {"OM_Ic": 12, "IA": 14, "IY": 16, "OM_Dis": 12, "DA": 10, "DY": 20},
            "Alanyaspor": {"OM_Ic": 12, "IA": 13, "IY": 17, "OM_Dis": 12, "DA": 10, "DY": 22},
            "Çaykur Rizespor": {"OM_Ic": 12, "IA": 15, "IY": 18, "OM_Dis": 12, "DA": 9, "DY": 23},
            "Kayserispor": {"OM_Ic": 12, "IA": 13, "IY": 19, "OM_Dis": 12, "DA": 9, "DY": 24},
            "Bodrum FK": {"OM_Ic": 12, "IA": 11, "IY": 18, "OM_Dis": 12, "DA": 7, "DY": 22},
            "Hatayspor": {"OM_Ic": 12, "IA": 12, "IY": 20, "OM_Dis": 12, "DA": 8, "DY": 25},
            "Adana Demirspor": {"OM_Ic": 12, "IA": 10, "IY": 25, "OM_Dis": 12, "DA": 6, "DY": 30},

            # Bültendeki Avrupa & Kupa Takımları
            "Slovan Bratislava": {"OM_Ic": 10, "IA": 22, "IY": 10, "OM_Dis": 10, "DA": 18, "DY": 12},
            "NK Celje": {"OM_Ic": 10, "IA": 18, "IY": 12, "OM_Dis": 10, "DA": 15, "DY": 16},
            "NEC Nijmegen": {"OM_Ic": 10, "IA": 16, "IY": 14, "OM_Dis": 10, "DA": 13, "DY": 16},
            "Bodo Glimt": {"OM_Ic": 10, "IA": 26, "IY": 11, "OM_Dis": 10, "DA": 23, "DY": 13},
            "Hapoel Beer Sheva": {"OM_Ic": 10, "IA": 19, "IY": 9, "OM_Dis": 10, "DA": 14, "DY": 11},
            "Sabah": {"OM_Ic": 10, "IA": 14, "IY": 13, "OM_Dis": 10, "DA": 10, "DY": 15},
            "Celtic": {"OM_Ic": 10, "IA": 30, "IY": 8, "OM_Dis": 10, "DA": 24, "DY": 11},
            "LASK": {"OM_Ic": 10, "IA": 17, "IY": 12, "OM_Dis": 10, "DA": 13, "DY": 17},
            "Atletico Madrid": {"OM_Ic": 10, "IA": 25, "IY": 8, "OM_Dis": 10, "DA": 20, "DY": 10},
            "Malaga CF": {"OM_Ic": 10, "IA": 12, "IY": 15, "OM_Dis": 10, "DA": 7, "DY": 20},
        }

    def get_team_names(self):
        return sorted(list(self.teams_data.keys()))

    def calculate_league_averages(self):
        total_home_goals = sum(d["IA"] for d in self.teams_data.values())
        total_away_goals = sum(d["DA"] for d in self.teams_data.values())
        total_home_matches = sum(d["OM_Ic"] for d in self.teams_data.values())
        total_away_matches = sum(d["OM_Dis"] for d in self.teams_data.values())

        avg_home_goals = total_home_goals / total_home_matches
        avg_away_goals = total_away_goals / total_away_matches
        return avg_home_goals, avg_away_goals

    def get_team_factors(self, home_team_name, away_team_name):
        avg_home_goals, avg_away_goals = self.calculate_league_averages()

        h_data = self.teams_data[home_team_name]
        a_data = self.teams_data[away_team_name]

        home_attack = (h_data["IA"] / h_data["OM_Ic"]) / avg_home_goals
        home_defense = (h_data["IY"] / h_data["OM_Ic"]) / avg_away_goals

        away_attack = (a_data["DA"] / a_data["OM_Dis"]) / avg_away_goals
        away_defense = (a_data["DY"] / a_data["OM_Dis"]) / avg_home_goals

        return {
            "home_attack": home_attack,
            "home_defense": home_defense,
            "away_attack": away_attack,
            "away_defense": away_defense,
            "league_home_avg": avg_home_goals,
            "league_away_avg": avg_away_goals
        }