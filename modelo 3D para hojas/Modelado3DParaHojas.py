import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import Delaunay
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import messagebox

# Variables globales
coordinates_file = None
depth_image_file = None
z_min = 0.0
z_max = 1.0
xyz_data = None  # Variable para almacenar los datos XYZ

# Función para cargar coordenadas desde un archivo txt
def load_coordinates_from_txt(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]  # Omitir la primera línea
        for line in lines:
            x, y = map(float, line.strip().split())
            coordinates.append([x, y])
    return np.array(coordinates)

# Función para cargar una imagen de profundidad npy
def load_depth_image(file_path):
    return np.load(file_path)

# Función para actualizar la visualización
def update_visualization():
    global coordinates_file, depth_image_file, z_min, z_max, xyz_data

    if coordinates_file is None or depth_image_file is None:
        return

    try:
        z_min = float(min_z_entry.get())
        z_max = float(max_z_entry.get())
    except ValueError:
        # Manejar excepción si los valores ingresados no son números válidos
        messagebox.showerror("Error", "Los valores de z deben ser números válidos.")
        return

    if z_min >= z_max:
        # Manejar excepción si el rango es incorrecto
        messagebox.showerror("Error", "El valor mínimo de z debe ser menor que el valor máximo de z.")
        return

    # Código para crear el modelo 3D
    coordinates = load_coordinates_from_txt(coordinates_file)
    depth_image = load_depth_image(depth_image_file)

    x = coordinates[:, 0]
    y = coordinates[:, 1]

    z = []
    x1 = []
    y1 = []
    for coord_x, coord_y in zip(x, y):
        z1 = depth_image[int(coord_y), int(coord_x)]
        if z_min <= z1 <= z_max:
            z.append(z1)
            x1.append(coord_x)
            y1.append(coord_y)
    z = np.array(z)
    x1 = np.array(x1)
    y1 = np.array(y1)

    if len(z) == 0:
        # Manejar excepción si no se grafica nada debido a valores bajos o altos
        messagebox.showwarning("Advertencia", "Los valores de z están fuera del rango para graficar.")
        return

    c3d = np.array([x1.tolist(), y1.tolist(), z.tolist()])
    c3d = c3d.T

    triangulation = Delaunay(c3d[:, 0:2])

    ax.clear()
    ax.scatter(c3d[:, 0], c3d[:, 1], c3d[:, 2], c='b', marker='o', label='Puntos')
    tetra_faces = c3d[triangulation.simplices]
    ax.add_collection3d(Poly3DCollection(tetra_faces, facecolors='cyan', linewidths=1, edgecolors='r', alpha=0.5))
    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.set_zlabel('Eje Z')
    ax.set_title('Modelo Hoja en 3D')
    canvas.draw()

    # Almacenar los datos XYZ
    xyz_data = c3d

# Función para guardar las coordenadas en un archivo de texto
def save_coordinates():
    global xyz_data
    if xyz_data is None:
        messagebox.showerror("Error", "No hay datos de coordenadas para guardar.")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
    if save_path:
        with open(save_path, 'w') as file:
            file.write("X Y Z\n")
            for xyz in xyz_data:
                x_str = f"{xyz[0]:.0f}"  # Formatear X sin decimales
                y_str = f"{xyz[1]:.0f}"  # Formatear Y sin decimales
                z_str = f"{xyz[2]:.0f}"  # Formatear Z sin decimales
                file.write(f"{x_str} {y_str} {z_str}\n")
        messagebox.showinfo("Información", "Coordenadas guardadas correctamente.")

# Función para seleccionar el archivo de coordenadas
def select_coordinates_file():
    global coordinates_file
    coordinates_file = filedialog.askopenfilename()

# Función para seleccionar el archivo de imagen de profundidad
def select_depth_image_file():
    global depth_image_file
    depth_image_file = filedialog.askopenfilename()

# Función para aplicar los cambios del rango de z
def apply_z_range():
    global z_min, z_max
    min_z_str = min_z_entry.get()
    max_z_str = max_z_entry.get()

    try:
        z_min = float(min_z_str)
        z_max = float(max_z_str)
    except ValueError:
        # Manejar excepción si los valores ingresados no son números válidos
        messagebox.showerror("Error", "Los valores de z deben ser números válidos.")
        return

    if z_min >= z_max:
        # Manejar excepción si el rango es incorrecto
        messagebox.showerror("Error", "El valor mínimo de z debe ser menor que el valor máximo de z.")
        return

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Visualización Hojas 3D")

# Configurar la interfaz para que ocupe todo el ancho y alto de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

# Crear un frame para la barra de herramientas
toolbar_frame = tk.Frame(root)
toolbar_frame.pack(side=tk.TOP, fill=tk.X)

# Agregar la barra de herramientas de Matplotlib
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
toolbar.update()

# Agregar botones para seleccionar archivos
coordinates_button = tk.Button(toolbar_frame, text="Seleccionar archivo de coordenadas", command=select_coordinates_file)
coordinates_button.pack(side=tk.LEFT, padx=10)

depth_image_button = tk.Button(toolbar_frame, text="Seleccionar archivo de imagen de profundidad", command=select_depth_image_file)
depth_image_button.pack(side=tk.LEFT, padx=10)

# Agregar controles para ajustar el rango de z
min_z_label = tk.Label(toolbar_frame, text="Valor mínimo de z:")
min_z_label.pack(side=tk.LEFT, padx=10)

min_z_entry = tk.Entry(toolbar_frame)
min_z_entry.pack(side=tk.LEFT, padx=10)

max_z_label = tk.Label(toolbar_frame, text="Valor máximo de z:")
max_z_label.pack(side=tk.LEFT, padx=10)

max_z_entry = tk.Entry(toolbar_frame)
max_z_entry.pack(side=tk.LEFT, padx=10)

apply_button = tk.Button(toolbar_frame, text="Aplicar Cambios de Rango", command=apply_z_range)
apply_button.pack(side=tk.LEFT, padx=10)

# Agregar el botón "Crear Modelo 3D"
create_model_button = tk.Button(toolbar_frame, text="Crear Modelo 3D", command=update_visualization)
create_model_button.pack(side=tk.LEFT, padx=10)

# Agregar el botón "Guardar Coordenadas"
save_coordinates_button = tk.Button(toolbar_frame, text="Guardar Coordenadas", command=save_coordinates)
save_coordinates_button.pack(side=tk.LEFT, padx=10)

# Ejecutar el bucle principal de la interfaz gráfica
root.mainloop()
