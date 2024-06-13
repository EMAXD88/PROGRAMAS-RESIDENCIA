import numpy as np
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

# Función para cargar y procesar el archivo al hacer clic en el botón
def procesar_archivo():
    global coordenadas_por_hoja, x
    archivo_nombre = filedialog.askopenfilename(filetypes=[("Archivos NPZ", "*.npz")])

    if not archivo_nombre:
        resultado.config(text="No se seleccionó ningún archivo.")
        num_hojas_label.config(text="Hojas detectadas: N/A")
        visualizar_boton.config(state="disabled")
    else:
        datos = np.load(archivo_nombre)
        x = datos['matriz']
        coordenadas_por_hoja = []
        fecha_actual = datetime.now()
        carpeta_fecha = fecha_actual.strftime('%Y-%m-%d')
        os.makedirs(carpeta_fecha, exist_ok=True)
        nombre_sin_extension = os.path.splitext(os.path.basename(archivo_nombre))[0]
        carpeta_archivo = os.path.join(carpeta_fecha, nombre_sin_extension)
        os.makedirs(carpeta_archivo, exist_ok=True)

        for i in range(len(x)):
            y_coords, x_coords = np.where(x[i, :, :] != 0)
            pixel_coords = list(zip(x_coords, y_coords))
            coordenadas_por_hoja.append(pixel_coords)
            carpeta_hoja = os.path.join(carpeta_archivo, f"Imagen{i}")
            os.makedirs(carpeta_hoja, exist_ok=True)
            archivo_nombre = os.path.join(carpeta_hoja, f"coordenadas_hoja_{i}.txt")
            with open(archivo_nombre, 'w') as f:
                for coord in pixel_coords:
                    formatted_coord = " ".join(map(str, coord))
                    f.write(f"{formatted_coord}\n")

        num_hojas_label.config(text=f"Hojas detectadas: {len(coordenadas_por_hoja)}")
        resultado.config(text="Procesamiento completo.")
        visualizar_boton.config(state="normal")

# Función para visualizar la hoja seleccionada
def visualizar_hoja():
    hoja_a_visualizar_str = num_hoja.get()
    try:
        hoja_a_visualizar = int(hoja_a_visualizar_str)
        if 0 <= hoja_a_visualizar < len(coordenadas_por_hoja):
            plt.imshow(x[hoja_a_visualizar, :, :], cmap='gray')
            plt.title(f"Hoja {hoja_a_visualizar}")
            plt.show()
            resultado.config(text="")  # Borrar cualquier mensaje de error anterior
        else:
            resultado.config(text="El número de hoja ingresado no está en rango.")
    except ValueError:
        resultado.config(text="Ingrese un número de hoja válido.")

# Función para cerrar la aplicación
def salir():
    ventana.destroy()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Procesador de Archivos NPZ")

# Etiqueta para mostrar un mensaje
mensaje_label = tk.Label(ventana, text="Este programa te mostrará la hoja que desees", font=("Helvetica", 13))
mensaje_label.pack(pady=10)

# Crear un botón para seleccionar un archivo (inicialmente habilitado)
boton_cargar = tk.Button(ventana, text="Seleccionar Archivo", command=procesar_archivo)
boton_cargar.pack(pady=10)

# Etiqueta para mostrar el resultado del procesamiento
resultado = tk.Label(ventana, text="")
resultado.pack()

# Etiqueta para mostrar la cantidad de hojas detectadas
num_hojas_label = tk.Label(ventana, text="Hojas detectadas: N/A", font=("Helvetica", 13))
num_hojas_label.pack()

# Entrada de texto para ingresar el número de hoja a visualizar
etiqueta_hoja = tk.Label(ventana, text="Número de hoja a visualizar:")
etiqueta_hoja.pack()
num_hoja = tk.Entry(ventana)
num_hoja.pack()

# Botón para visualizar la hoja seleccionada (inicialmente deshabilitado)
visualizar_boton = tk.Button(ventana, text="Visualizar", command=visualizar_hoja, state="disabled")
visualizar_boton.pack()

# Botón para salir de la aplicación
boton_salir = tk.Button(ventana, text="Salir", command=salir)
boton_salir.pack()

# Variables para almacenar datos
coordenadas_por_hoja = []
x = None

# Ejecutar la ventana
ventana.mainloop()
