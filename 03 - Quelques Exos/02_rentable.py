"""
Énoncé :
L'abonnement du cinema pour un an coute 120 euros.
Chaque place de cinema coute 7 euros.
À partir de combien de places achetées l'abonnement devient-il rentable ?
Combien de fois par mois faut-il aller au cinema pour que l'abonnement soit rentable ?
"""

compteur = 0
abonnement = 120
prix_place = 7
while abonnement >= compteur * prix_place:
    compteur += 1

print(f"À partir de {compteur} places, l'abonnement est rentable.")
print(f"Il faut aller au cinéma {compteur / 12} fois par mois pour que l'abonnement soit rentable.")