import tkinter as tk
from tkinter import filedialog
import numpy as np
from PIL import Image
import cv2
import os
from datetime import datetime

def cargar_archivo():
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos .dat.npz", "*.dat.npz")])
    if ruta_archivo:
        calcular_areas(ruta_archivo)

def calcular_areas(ruta):
    datos = np.load(ruta)
    carpeta_nombre = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs(carpeta_nombre)  # Crear carpeta con la fecha actual
    
    for key in datos.keys():
        matrices = datos[key]
        if isinstance(matrices, np.ndarray):
            for i, matriz in enumerate(matrices):
                imagen = matriz * 255
                imagen_pil = Image.fromarray(imagen.astype(np.uint8))
                imagen_cv2 = cv2.cvtColor(np.array(imagen_pil), cv2.COLOR_GRAY2BGR)
                gris = cv2.cvtColor(imagen_cv2, cv2.COLOR_BGR2GRAY)
                _, umbralizada = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY)
                contornos, _ = cv2.findContours(umbralizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                contorno_objeto = max(contornos, key=cv2.contourArea)
                area_objeto = cv2.contourArea(contorno_objeto)
                
                nombre_archivo = f"{key}_{i}.png"
                ruta_imagen = os.path.join(carpeta_nombre, nombre_archivo)
                cv2.drawContours(imagen_cv2, contornos, -1, (0, 255, 0), 2)
                cv2.imwrite(ruta_imagen, imagen_cv2)  # Guardar imagen
                
                ruta_txt = os.path.join(carpeta_nombre, f"{key}_areas.txt")
                with open(ruta_txt, "a") as archivo_txt:
                    archivo_txt.write(f"Matriz {key}-{i}: Área -> {area_objeto}\n")  # Guardar área en archivo txt

# Crear ventana principal
root = tk.Tk()
root.title("Cargar Archivo .dat.npz")

# Botón para cargar archivo
btn_cargar = tk.Button(root, text="Cargar Archivo", command=cargar_archivo)
btn_cargar.pack(padx=20, pady=10)

root.mainloop()
