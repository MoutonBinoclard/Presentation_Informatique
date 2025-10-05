import random

def plus_ou_moins():
    nombre_aleatoire = random.randint(1, 100)
    essais = 0
    while True:
        essai = int(input("Devinez le nombre (entre 1 et 100) : "))
        essais += 1
        if essai < nombre_aleatoire:
            print("Plus haut !")
        elif essai > nombre_aleatoire:
            print("Plus bas !")
        else:
            print(f"Bravo ! Vous avez trouvé le nombre {nombre_aleatoire} en {essais} essais.")
            return

# Exemple d'utilisation
plus_ou_moins()