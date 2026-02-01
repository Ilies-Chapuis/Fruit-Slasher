import datetime
from game import Game

def highscores():
    score = 0
    try:
        with open("history.txt", "a", encoding="utf-8") as f:
            f.write(f"{score},{datetime}\n")
    except Exception as e:
        print("Erreur lors de l'enregistrement du score :", e)

def read_history():
    history = []

    try:
        with open("history.txt", "r", encoding="utf-8") as f:
            for ligne in f:
                score = ligne.strip().split(",")
                history.append((int(score), int(datetime)))
    except FileNotFoundError:
        pass
    except Exception as e:
        print("Erreur lors de la lecture des scores :", e)