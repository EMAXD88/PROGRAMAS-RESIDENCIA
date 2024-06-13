import numpy as np
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

# Crear una ventana de tkinter (puede estar oculta)
root = tk.Tk()
root.withdraw()

# Abrir un cuadro de diálogo para seleccionar el archivo
archivo_nombre = filedialog.askopenfilename(filetypes=[("Archivos NPZ", "*.npz")])

# Comprobar si se seleccionó un archivo
if not archivo_nombre:
    print("No se seleccionó ningún archivo.")
else:
    # Cargar los datos desde el archivo seleccionado
    datos = np.load(archivo_nombre)
    x = datos['matriz']
    print(len(x))
    coordenadas_por_hoja = []  # Lista para almacenar coordenadas por hoja

    # Obtener la fecha actual
    fecha_actual = datetime.now()
    carpeta_fecha = fecha_actual.strftime('%Y-%m-%d')

    # Crear carpeta principal
    os.makedirs(carpeta_fecha, exist_ok=True)

    # Obtener el nombre del archivo sin la extensión
    nombre_sin_extension = os.path.splitext(os.path.basename(archivo_nombre))[0]

    # Crear carpeta con el nombre del archivo dentro de la carpeta de la fecha
    carpeta_archivo = os.path.join(carpeta_fecha, nombre_sin_extension)
    os.makedirs(carpeta_archivo, exist_ok=True)

    for i in range(len(x)):
        # Encontrar las coordenadas de los píxeles
        y_coords, x_coords = np.where(x[i, :, :] != 0)
        pixel_coords = list(zip(x_coords, y_coords))
        coordenadas_por_hoja.append(pixel_coords)  # Agregar coordenadas a la lista

        # Crear carpeta para cada hoja y guardar el archivo de texto
        carpeta_hoja = os.path.join(carpeta_archivo, f"Imagen{i}")
        os.makedirs(carpeta_hoja, exist_ok=True)
        archivo_nombre = os.path.join(carpeta_hoja, f"coordenadas_hoja_{i}.txt")
        with open(archivo_nombre, 'w') as f:
            #f.write(f"Coordenadas para hoja {i}:\n")
            for coord in pixel_coords:
                formatted_coord = " ".join(map(str, coord))
                f.write(f"{formatted_coord}\n")
