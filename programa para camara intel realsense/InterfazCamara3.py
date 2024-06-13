import tkinter as tk
from tkinter import messagebox
import cv2
import time
import os
import pyrealsense2 as rs
import numpy as np
from PIL import Image, ImageTk
import datetime

print("reset start")
ctx = rs.context()
devices = ctx.query_devices()
for dev in devices:
    dev.hardware_reset()
print("reset done")

# Variables globales para la cámara y su estado
pipeline = None
align = None
camera_running = False
image_counter = 1  # Contador de imágenes
image_preview = None  # Variable para almacenar la vista previa de la imagen

# Variables globales para las imágenes
color_image = None
depth_image = None

# Función para iniciar la cámara RealSense
def start_camera():
    global pipeline, align, camera_running
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 5)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 5)
    profile = pipeline.start(config)
    align_to = rs.stream.color
    align = rs.align(align_to)
    camera_running = True

    # Bloquear la configuración de la cámara de profundidad para evitar modificaciones
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_sensor.set_option(rs.option.enable_auto_exposure, False)
    depth_sensor.set_option(rs.option.enable_auto_white_balance, False)
    depth_sensor.set_option(rs.option.visual_preset, rs.option.visual_preset_custom)

# Función para mostrar la vista previa de la imagen en una ventana emergente
def show_image_preview(color_img, depth_img):
    global image_preview, color_image, depth_image
    color_image = color_img
    depth_image = depth_img

    # Convierte la imagen de BGR a RGB
    color_image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

    # Crear una nueva ventana emergente que se ajuste al ancho de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    image_preview = tk.Toplevel(root)
    image_preview.title("Vista Previa de la Imagen Tomada")
    image_preview.geometry(f"{screen_width}x{screen_height}")

    # Frame para contener los elementos en la parte superior
    top_frame = tk.Frame(image_preview)
    top_frame.pack(side=tk.TOP)

    # Muestra la imagen en color
    color_photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.resize(color_image_rgb, (300, 200))))
    color_label = tk.Label(top_frame, image=color_photo)
    color_label.image = color_photo
    color_label.pack(side=tk.LEFT, padx=10, pady=10)

    # Crear entrada para el nombre de la imagen
    name_label = tk.Label(image_preview, text="Nombre de la Imagen:")
    name_label.pack()
    name_entry = tk.Entry(image_preview)
    name_entry.pack()

    # Crear Spinbox para seleccionar el año
    year_label = tk.Label(image_preview, text="Año:")
    year_label.pack()
    # Obtener el año actual
    current_year = datetime.datetime.now().year
    year_spinbox = tk.Spinbox(image_preview, from_=current_year, to=current_year + 10)
    year_spinbox.pack()

    # Crear Spinbox para seleccionar el mes
    month_label = tk.Label(image_preview, text="Mes:")
    month_label.pack()
    # Obtener el mes actual
    current_month = datetime.datetime.now().month
    month_spinbox = tk.Spinbox(image_preview, from_=1, to=12, value=current_month)
    month_spinbox.pack()

    # Crear Spinbox para seleccionar el día
    day_label = tk.Label(image_preview, text="Día:")
    day_label.pack()
    # Obtener el día actual
    current_day = datetime.datetime.now().day
    day_spinbox = tk.Spinbox(image_preview, from_=1, to=31, value=current_day)
    day_spinbox.pack()

    # Botón para guardar la imagen
    save_button = tk.Button(image_preview, text="Proceder a Guardar", command=lambda: save_image(name_entry.get(), int(year_spinbox.get()), int(month_spinbox.get()), int(day_spinbox.get())))
    save_button.pack()

    # Muestra la imagen de profundidad
    depth_image_rectified = cv2.normalize(depth_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    depth_photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.resize(depth_image_rectified * 6, (300, 200))))
    depth_label = tk.Label(top_frame, image=depth_photo)
    depth_label.image = depth_photo
    depth_label.pack(side=tk.LEFT, padx=10, pady=10)

# Función para tomar una foto
def take_photo():
    global camera_running, image_counter
    if not camera_running:
        messagebox.showerror("ERROR", "LA CAMARA NO SE HA INICIADO CORRECTAMENTE!")
        return

    # Captura las imágenes RGB y de profundidad
    frames = pipeline.wait_for_frames()
    aligned_frames = align.process(frames)
    aligned_depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()
    
    if not aligned_depth_frame or not color_frame:
        messagebox.showerror("ERROR", "FALLO EN LA CAPTURA!")
        return

    # Convierte las imágenes a formato numpy
    depth_image = np.asanyarray(aligned_depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    # Muestra la vista previa de la imagen
    show_image_preview(color_image, depth_image)

# Función para verificar si el archivo ya existe
def image_exists(image_path):
    return os.path.isfile(image_path)

# Función para guardar la imagen con el nombre y la fecha proporcionados
def save_image(name, year, month, day):
    global image_counter, image_preview
    if not name:
        messagebox.showerror("ERROR", "Debe ingresar un nombre para la imagen.")
        return

    # Construir la fecha en el formato deseado
    date_str = f"{year}-{month:02d}-{day:02d}"

    # Convierte la cadena de fecha a un objeto datetime
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")

    # Cierra la ventana de vista previa
    if image_preview:
        image_preview.destroy()

    # Crear subcarpeta para el día actual si no existe
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    folder_name = os.path.join("CapturasDeFotos", current_date)
    os.makedirs(folder_name, exist_ok=True)

    # Crear subcarpetas para las imágenes RGB, de profundidad y .npy
    rgb_folder = os.path.join(folder_name, "RGB")
    depth_folder = os.path.join(folder_name, "Profundidad")
    npy_rgb_folder = os.path.join(folder_name, "RGB_npy")
    npy_depth_folder = os.path.join(folder_name, "Profundidad_npy")
    os.makedirs(rgb_folder, exist_ok=True)
    os.makedirs(depth_folder, exist_ok=True)
    os.makedirs(npy_rgb_folder, exist_ok=True)
    os.makedirs(npy_depth_folder, exist_ok=True)

    # Guarda las imágenes con el nombre y la fecha proporcionados
    image_counter += 1
    image_name = name + "_" + date.strftime("%Y%m%d")
    
    rgb_image_path = os.path.join(rgb_folder, f"{image_name}_rgb.png")
    depth_image_path = os.path.join(depth_folder, f"{image_name}_profundidad.png")
    npy_rgb_image_path = os.path.join(npy_rgb_folder, f"{image_name}_rgb.npy")
    npy_depth_image_path = os.path.join(npy_depth_folder, f"{image_name}_profundidad.npy")
    
    # Verificar si el archivo ya existe
    while (
        image_exists(rgb_image_path) or
        image_exists(depth_image_path) or
        image_exists(npy_rgb_image_path) or
        image_exists(npy_depth_image_path)
    ):
        confirm = messagebox.askyesno("Archivo Existente", "Este archivo ya existe. ¿Deseas sobrescribirlo?")
        if confirm:
            # Si se confirma la sobrescritura, eliminar el archivo existente
            os.remove(rgb_image_path)
            os.remove(depth_image_path)
            os.remove(npy_rgb_image_path)
            os.remove(npy_depth_image_path)
            break
        else:
            # Mostrar la ventana de vista previa nuevamente
            show_image_preview(color_image, depth_image)
            return

    cv2.imwrite(rgb_image_path, color_image)
    cv2.imwrite(depth_image_path, depth_image)
    np.save(npy_rgb_image_path, color_image)
    np.save(npy_depth_image_path, depth_image)
    
    messagebox.showinfo("FOTO GUARDADA", f"Las imágenes se guardaron como:\n{rgb_image_path}\n{depth_image_path}\n{npy_rgb_image_path}\n{npy_depth_image_path}")

# Función para cerrar la aplicación y detener la cámara
def close_app():
    global camera_running
    if camera_running:
        pipeline.stop()
    root.destroy()

# Función para actualizar las vistas de la cámara en tiempo real
def update_camera_frame():
    global camera_running
    if camera_running:
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()

        if color_frame and depth_frame:
            color_image = np.asanyarray(color_frame.get_data())
            color_image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
            color_photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.resize(color_image_rgb, (300, 200))))
            label_color.config(image=color_photo)
            label_color.image = color_photo

            depth_image = np.asanyarray(depth_frame.get_data())
            depth_image_rectified = cv2.normalize(depth_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            depth_photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.resize(depth_image_rectified, (300, 200))))
            label_depth.config(image=depth_photo)
            label_depth.image = depth_photo

    root.after(60, update_camera_frame)  # Ajustamos el retraso a 30 ms para mejorar el rendimiento

# Creación de la ventana principal de la interfaz
root = tk.Tk()
root.title("INTERFAZ DE LA CÁMARA")
root.attributes('-fullscreen', True)

# Creación de un marco para alinear los botones en la parte superior
frame_buttons_top = tk.Frame(root)
frame_buttons_top.pack(side=tk.TOP, fill=tk.X)  # Agrega un espaciado en la parte superior

# Botón para iniciar la cámara
start_camera_btn = tk.Button(frame_buttons_top, text="INICIAR CÁMARA", command=start_camera)
start_camera_btn.pack(side=tk.LEFT, padx=10)

# Botón para tomar una foto
take_photo_btn = tk.Button(frame_buttons_top, text="TOMAR FOTO", command=take_photo)
take_photo_btn.pack(side=tk.LEFT, padx=10)

# Botón para salir de la aplicación
exit_btn = tk.Button(frame_buttons_top, text="SALIR", command=close_app)
exit_btn.pack(side=tk.LEFT, padx=10)

# Creación del marco para las vistas de la cámara
frame_camera = tk.Frame(root)
frame_camera.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Etiqueta para la vista de la cámara en color (RGB)
label_color = tk.Label(frame_camera)
label_color.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Etiqueta para la vista de la cámara en profundidad
label_depth = tk.Label(frame_camera)
label_depth.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Iniciamos la actualización de las vistas de la cámara con un retraso de 30 ms
root.after(60, update_camera_frame)
root.mainloop()