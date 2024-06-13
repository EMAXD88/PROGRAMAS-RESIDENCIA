import tkinter as tk
from tkinter import filedialog
from skimage.util import img_as_float
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def cargar_imagenes():
    global depth_image, rgb_image
    depth_file_path = filedialog.askopenfilename(title="Seleccionar imagen de profundidad", filetypes=[("Archivos numpy", "*.npy")])
    if depth_file_path:
        depth_image = np.load(depth_file_path)

    rgb_file_path = filedialog.askopenfilename(title="Seleccionar imagen RGB", filetypes=[("Archivos numpy", "*.npy")])
    if rgb_file_path:
        rgb_image = np.load(rgb_file_path)

    if depth_image is not None and rgb_image is not None:
        procesar_imagenes()

def procesar_imagenes():
    if depth_image is not None and rgb_image is not None:
        # Tu código de procesamiento de imágenes aquí

        # Obtener las dimensiones de la imagen de profundidad
        height, width = depth_image.shape
        # Crear una figura y un eje 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        k = 0.8  # distancia del objeto más lejano
        cont = 0
        cx = width / 2
        cy = height / 2
        fx = width / 2
        fy = height / 2
        X = []
        Y = []
        Z = []
        rgb = []
        for y in range(0, height, 1):
            for x in range(0, width, 1):
                z = depth_image[y, x] * k
                if 0 < z < 500 :
                    X.append((x - cx) * z / fx)
                    Y.append((y - cy) * z / fy)
                    Z.append(z)
                    rgb.append([rgb_image[y, x, 2], rgb_image[y, x, 1], rgb_image[y, x, 1]])
        # Graficar los puntos 3D con colores RGB
        rgb2 = np.array(rgb) / 255
        ax.scatter(np.array(X), np.array(Y), -np.array(Z), c=rgb2)
        # Mostrar la figura
        plt.show()

# Crear la ventana principal
root = tk.Tk()
root.title("Selector de imágenes")

# Inicializar las imágenes como None
depth_image = None
rgb_image = None

# Botón para cargar imágenes
cargar_button = tk.Button(root, text="Cargar Imágenes", command=cargar_imagenes)
cargar_button.pack(pady=20)

# Ejecutar la aplicación
root.mainloop()
