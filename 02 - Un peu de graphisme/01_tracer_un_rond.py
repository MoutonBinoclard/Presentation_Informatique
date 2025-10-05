import matplotlib.pyplot as plt
import math

def tracer_un_rond(nombre_de_point):
    # Le cercle sera toujours de centre 0, 0 et de rayon 1
    x = []
    y = []
    for i in range(nombre_de_point):
        angle = 2 * math.pi * i / nombre_de_point
        x.append(math.cos(angle))
        y.append(math.sin(angle))
    x.append(x[0])  # Pour fermer le cercle
    y.append(y[0])  # Pour fermer le cercle
    plt.plot(x, y)
    plt.axis('equal')  # Pour que le cercle ne soit pas déformé
    plt.show()

# Exemple d'utilisation
tracer_un_rond(10)
tracer_un_rond(20)
tracer_un_rond(250)