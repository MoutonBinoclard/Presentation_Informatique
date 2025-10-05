import matplotlib.pyplot as plt
import numpy as np

def tracer_sinus(x_0, x_1, nombre_de_point):

    x = np.linspace(x_0, x_1, nombre_de_point)
    y = np.sin(x)
    plt.plot(x, y)
    plt.grid()
    plt.axhline(0, color='black', linewidth=3)
    plt.axvline(0, color='black', linewidth=3)
    plt.show()

# Exemple d'utilisation
tracer_sinus(0,  2 * np.pi, 100)  # De 0 à 2π avec 100 points