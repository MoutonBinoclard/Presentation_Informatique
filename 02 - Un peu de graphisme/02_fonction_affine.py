import matplotlib.pyplot as plt

def tracer_fonction_affine(a, b, x_0, x_1):
    # On peut se permettre de ne mettre que 2 points car c'est une droite
    x = [x_0, x_1]
    y = [a * x_0 + b, a * x_1 + b]
    plt.plot(x, y)
    plt.grid()
    plt.axhline(0, color='black', linewidth=3)
    plt.axvline(0, color='black', linewidth=3)
    plt.show()

# Exemple d'utilisation
tracer_fonction_affine(2, 3, -2, 10)  # y = x