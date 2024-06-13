import tkinter as tk
from tkinter import filedialog
import numpy as np
from PIL import Image
import os

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("REDIMENSIONAR IMÁGENES")
        self.root.geometry("{0}x{1}".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))

        self.directorio_entrada = ""
        self.directorio_salida = ""
        self.resolucion_var = tk.StringVar()
        self.resolucion_var.set("Alto X Ancho")

        self.create_widgets()

    def create_widgets(self):
        boton_entrada = tk.Button(self.root, text="Seleccionar carpeta de entrada", command=self.seleccionar_directorio_entrada)
        boton_salida = tk.Button(self.root, text="Seleccionar carpeta de salida", command=self.seleccionar_directorio_salida)
        boton_convertir = tk.Button(self.root, text="Convertir imágenes", command=self.redimensionar_y_guardar_imagenes)

        boton_entrada.grid(row=0, column=0, padx=10, pady=5)
        boton_salida.grid(row=0, column=1, padx=10, pady=5)
        boton_convertir.grid(row=0, column=2, padx=10, pady=10)

        label_resolucion = tk.Label(self.root, text="Seleccionar resolución:")
        label_resolucion.grid(row=1, column=0, columnspan=3, pady=10)
        resoluciones = ["640x640", "1280x720", "1920x1080"]
        menu_resolucion = tk.OptionMenu(self.root, self.resolucion_var, *resoluciones)
        menu_resolucion.grid(row=2, column=0, columnspan=3)
        
        self.etiqueta_rutas = tk.Label(self.root, text="")
        self.etiqueta_rutas.grid(row=3, column=0, columnspan=3, pady=20)

    def seleccionar_directorio_entrada(self):
        self.directorio_entrada = filedialog.askdirectory(title="Seleccionar carpeta de entrada")
        self.actualizar_etiqueta_rutas()

    def seleccionar_directorio_salida(self):
        self.directorio_salida = filedialog.askdirectory(title="Seleccionar carpeta de salida")
        self.actualizar_etiqueta_rutas()

    def actualizar_etiqueta_rutas(self):
        texto_entrada = f"Carpeta de entrada: {self.directorio_entrada}"
        texto_salida = f"Carpeta de salida: {self.directorio_salida}"
        self.etiqueta_rutas.config(text=f"{texto_entrada}\n{texto_salida}")

    def redimensionar_y_guardar_imagenes(self):
        try:
            resolucion = tuple(map(int, self.resolucion_var.get().split("x")))
            for nombre_archivo in os.listdir(self.directorio_entrada):
                if nombre_archivo.lower().endswith((".npy", ".png", ".jpg", ".jpeg")):
                    ruta_imagen = os.path.join(self.directorio_entrada, nombre_archivo)

                    if nombre_archivo.lower().endswith(".npy"):
                        arreglo_imagen = np.load(ruta_imagen)
                    else:
                        imagen = Image.open(ruta_imagen)
                        arreglo_imagen = np.array(imagen)

                    imagen_redimensionada = np.array(Image.fromarray(arreglo_imagen).resize(resolucion))

                    nombre_salida = nombre_archivo.replace(".", f"_redimensionada.")
                    ruta_salida = os.path.join(self.directorio_salida, nombre_salida)

                    np.save(ruta_salida, imagen_redimensionada) if nombre_archivo.lower().endswith(".npy") else Image.fromarray(imagen_redimensionada).save(ruta_salida)

        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()
