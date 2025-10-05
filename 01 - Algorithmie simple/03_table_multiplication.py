def multiplication_table():
    n = int(input("Table de multiplication de : "))
    for i in range(1, 10+1): # De 1 à 10 inclus
        print(f"{n} x {i} = {n * i}")

# Exemple d'utilisation
multiplication_table()