import random
import unicodedata

# Charger la liste de mots depuis un fichier texte

def charger_mots(fichier):
    mots = []
    with open(fichier, encoding="utf-8") as f:
        for ligne in f:
            mot = ligne.strip().lower()
            # Supprimer les accents
            mot = ''.join(c for c in unicodedata.normalize('NFD', mot) if unicodedata.category(c) != 'Mn')
            # Vérifier que le mot ne contient que des lettres de l'alphabet standard
            if mot.isalpha():
                mots.append(mot)
    return mots

mots = charger_mots("liste_mots.txt")

def afficher_pendu(erreurs):
    etapes = [
        """
               |
               |
               |
               |
               |
               |
        =========
        """,
        """
           -----
               |
               |
               |
               |
               |
        =========
        """,
        """
           -----
           |   |
               |
               |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
               |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
           |   |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
          /|   |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          /    |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          / \\  |
               |
        =========
        """,
        """
           -----
          /|   |
           O   |
          /|\\  |
          / \\  |
               |
        =========
        """,
        """
          /-----\\
          |/   |
           O   |
          /|\\  |
          / \\  |
               |
        =========
        """
    ]
    print(etapes[erreurs])

def jouer_pendu():
    mot = random.choice(mots)
    lettres_trouvees = set()
    lettres_tentees = set()
    erreurs = 0
    max_erreurs = 10

    print("Bienvenue au jeu du pendu !")

    while erreurs < max_erreurs:
        afficher_pendu(erreurs)
        mot_affiche = " ".join([lettre if lettre in lettres_trouvees else "_" for lettre in mot])
        print(f"Mot à deviner : {mot_affiche}")
        print(f"Lettres tentées : {', '.join(sorted(lettres_tentees))}")

        if "_" not in mot_affiche:
            print("Félicitations, vous avez gagné !")
            break

        lettre = input("Proposez une lettre : ").lower()

        if len(lettre) != 1 or not lettre.isalpha():
            print("Veuillez entrer une seule lettre.")
            continue

        if lettre in lettres_tentees:
            print("Vous avez déjà tenté cette lettre.")
            continue

        lettres_tentees.add(lettre)

        if lettre in mot:
            lettres_trouvees.add(lettre)
            print("Bonne lettre !")
        else:
            erreurs += 1
            print("Mauvaise lettre.")

    if erreurs == max_erreurs:
        afficher_pendu(erreurs)
        print(f"Vous avez perdu. Le mot était : {mot}")

if __name__ == "__main__":
    jouer_pendu()