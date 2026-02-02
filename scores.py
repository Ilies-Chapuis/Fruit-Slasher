import os
import json
from datetime import datetime


class ScoreManager:
    def __init__(self, filename="highscores.json"):
        self.filename = filename
        self.scores = self.load_scores()

    def load_scores(self):
        #Charge les scores depuis le fichier
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erreur lecture scores: {e}")
                return []
        return []

    def save_score(self, player_name, score, difficulty, game_mode):
        """Enregistre un nouveau score"""
        new_score = {
            'player': player_name,
            'score': score,
            'difficulty': difficulty,
            'mode': game_mode,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.scores.append(new_score)

        # Trier par score décroissant
        self.scores.sort(key=lambda x: x['score'], reverse=True)

        # Garder seulement les 100 meilleurs scores
        self.scores = self.scores[:100]

        # Sauvegarder
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.scores, f, indent=2, ensure_ascii=False)
            print(f"Score enregistre: {score} points")
            return True
        except Exception as e:
            print(f"Erreur sauvegarde score: {e}")
            return False

    def get_top_scores(self, limit=10, difficulty=None, game_mode=None):
        """Retourne les meilleurs scores"""
        filtered_scores = self.scores

        # Filtrer par difficulté
        if difficulty:
            filtered_scores = [s for s in filtered_scores if s['difficulty'] == difficulty]

        # Filtrer par mode de jeu
        if game_mode:
            filtered_scores = [s for s in filtered_scores if s['mode'] == game_mode]

        return filtered_scores[:limit]

    def get_player_best_score(self, player_name):
        """Retourne le meilleur score d'un joueur"""
        player_scores = [s for s in self.scores if s['player'] == player_name]
        if player_scores:
            return max(player_scores, key=lambda x: x['score'])
        return None

    def is_high_score(self, score, limit=10):
        """Vérifie si c'est un top score"""
        if len(self.scores) < limit:
            return True
        return score > self.scores[limit - 1]['score']

    def get_rank(self, score):
        """Retourne le rang d'un score"""
        rank = 1
        for s in self.scores:
            if s['score'] > score:
                rank += 1
            else:
                break
        return rank