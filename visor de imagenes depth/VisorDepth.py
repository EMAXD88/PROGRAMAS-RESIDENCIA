import tkinter as tk
from tkinter import filedialog
import subprocess
import cv2
import numpy as np
import os
import time

def ajustar_visibilidad(imagen, visibilidad):
    imagen_ajustada = imagen.astype(np.float32) * visibilidad
    imagen_ajustada = np.uint16(imagen_ajustada)
    return imagen_ajustada

def abrir_imagen():
    ruta_archivo = filedialog.askopenfilename()
    if ruta_archivo:
        imagen = None

        if ruta_archivo.endswith('.npy'):
            try:
                imagen = np.load(ruta_archivo)
            except Exception as e:
                etiqueta_resultado.config(text="Error al cargar el archivo .npy.")
                print(e)
        else:
            imagen = cv2.imread(ruta_archivo, cv2.IMREAD_UNCHANGED)

        if imagen is not None:
            imagen_ajustada = ajustar_visibilidad(imagen, visibilidad)
            archivo_temporal = "imagen_aumentada_de_visibilidad.png"
            cv2.imwrite(archivo_temporal, imagen_ajustada)
            subprocess.Popen(["start", archivo_temporal], shell=True)
            time.sleep(1)  # Esperar un segundo antes de eliminar el archivo temporal
            os.remove(archivo_temporal)  # Eliminamos el archivo temporal después de abrirlo
        else:
            etiqueta_resultado.config(text="Formato de archivo no compatible.")

def actualizar_visibilidad(nueva_visibilidad):
    global visibilidad
    visibilidad = float(nueva_visibilidad)
    etiqueta_visibilidad.config(text=f"Visibilidad: {visibilidad:.2f}")

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Visualizador de Imágenes de Profundidad")

# Etiqueta de visibilidad
etiqueta_visibilidad = tk.Label(ventana_principal, text="Visibilidad: 1.00")
etiqueta_visibilidad.pack()

# Barra deslizante para ajustar la visibilidad (rango de 0.0 a 100.0)
barra_deslizante_visibilidad = tk.Scale(ventana_principal, from_=0.0, to=100.0, resolution=0.01, orient="horizontal", length=200, command=actualizar_visibilidad)
barra_deslizante_visibilidad.pack()

# Botón para abrir la imagen en el visor de imágenes de Windows
boton_abrir_visualizador = tk.Button(ventana_principal, text="Elegir Imagen De Profundidad", command=abrir_imagen)
boton_abrir_visualizador.pack()

# Etiqueta para mostrar mensajes
etiqueta_resultado = tk.Label(ventana_principal, text="")
etiqueta_resultado.pack()

# Valor inicial de visibilidad
visibilidad = 1.0

ventana_principal.mainloop()
