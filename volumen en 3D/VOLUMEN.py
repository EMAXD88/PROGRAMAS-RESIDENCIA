import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Función para calcular el volumen a partir de las coordenadas XYZ
def calcular_volumen(coordenadas):
    if len(coordenadas) < 4:
        return 0.0

    volume = 0.0
    origin = np.array(coordenadas[0])  # Convertir la tupla en un vector numpy
    for i in range(1, len(coordenadas) - 2):
        v1 = np.array(coordenadas[i]) - origin  # Convertir la tupla en un vector numpy
        v2 = np.array(coordenadas[i + 1]) - origin  # Convertir la tupla en un vector numpy
        v3 = np.array(coordenadas[i + 2]) - origin  # Convertir la tupla en un vector numpy
        volume += abs(np.dot(v1, np.cross(v2, v3))) / 6.0

    return volume

# Función para crear una representación 3D del objeto
def crear_representacion_3d(coordenadas):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Organizar las coordenadas en arrays separados para X, Y y Z
    x, y, z = zip(*coordenadas)

    # Crear una malla de triángulos para visualizar el objeto
    triangulos = [(x[i], y[i], z[i]) for i in range(len(x))]

    # Descomponer los triángulos en vértices
    xs, ys, zs = zip(*triangulos)
    verts = [list(zip(xs, ys, zs))]

    # Crear una colección de polígonos 3D
    poly3d = Poly3DCollection(verts, alpha=0.25, linewidths=1, edgecolors='r')

    ax.add_collection3d(poly3d)

    # Establecer límites para los ejes
    ax.set_xlim(min(x), max(x))
    ax.set_ylim(min(y), max(y))
    ax.set_zlim(min(z), max(z))

    # Etiquetas de ejes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Mostrar la figura
    plt.show()

# Función para leer las coordenadas desde un archivo
def leer_coordenadas_desde_archivo():
    file_path = filedialog.askopenfilename(title="Seleccionar archivo de coordenadas")
    if not file_path:
        return

    coordenadas = []
    with open(file_path, 'r') as archivo:
        # Ignorar la primera línea
        next(archivo)
        for linea in archivo:
            x, y, z = map(float, linea.strip().split())
            coordenadas.append((x, y, z))

    # Calcular el volumen del objeto
    volumen = calcular_volumen(coordenadas)

    # Mostrar el resultado en la etiqueta de resultado
    resultado_label.config(text=f'El volumen del objeto es: {volumen} unidades cúbicas')

    # Crear la representación 3D del objeto
    crear_representacion_3d(coordenadas)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Cálculo de Volumen y Visualización 3D")

# Botón para abrir el archivo
abrir_archivo_button = tk.Button(ventana, text="Abrir Archivo", command=leer_coordenadas_desde_archivo)
abrir_archivo_button.pack(pady=20)

# Etiqueta para mostrar el resultado
resultado_label = tk.Label(ventana, text="")
resultado_label.pack()

# Iniciar la aplicación
ventana.mainloop()
