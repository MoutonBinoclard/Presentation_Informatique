def fibonnaci_to_n():
    n = int(input("N atteint par la suite de Fibonacci : "))
    a, b = 0, 1
    while a < n:
        print(b, end=' ')
        a, b = b, a + b
    print()

# Exemple d'utilisation
fibonnaci_to_n()