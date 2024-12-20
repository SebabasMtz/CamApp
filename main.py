import tkinter as tk
from tkinter import filedialog 
import cv2
from PIL import Image, ImageTk
import imutils
import ctypes
import io
from PIL import ImageGrab
import win32clipboard

video = None
camera_index = 0

def video_camara():
    global video
    video = cv2.VideoCapture(camera_index)  # 0 = EOS Cam // 1 = WebCam
    iniciar()

def iniciar():
    global video
    ret, frame = video.read()
    if ret:
        frame = imutils.resize(frame, width=950)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img_recortada = recortar_tamano_infantil(img)
        img_tk_recortada = ImageTk.PhotoImage(img_recortada)
        etiqueta_video.configure(image=img_tk_recortada)
        etiqueta_video.image = img_tk_recortada
        etiqueta_video.after(10, iniciar)

def detener_video():
    global video
    if video is not None:
        video.release()
        etiqueta_video.configure(image="")
        etiqueta_video.image = None

def cerrar_ventana():
    detener_video()
    root.destroy()

def recortar_tamano_infantil(imagen):
    x1, y1, x2, y2 = 80, 50, 475, 530
    imagen_recortada = imagen.crop((x1, y1, x2, y2))
    return imagen_recortada

def tomar_foto():
    global video
    ret, frame = video.read()
    if ret:
        frame = imutils.resize(frame, width=950)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img_recortada = recortar_tamano_infantil(img)

        ventana_foto = tk.Toplevel(root)
        ventana_foto.title("Foto Capturada")

        img_tk_recortada = ImageTk.PhotoImage(img_recortada)
        etiqueta_foto_recortada = tk.Label(ventana_foto, image=img_tk_recortada)
        etiqueta_foto_recortada.image = img_tk_recortada
        etiqueta_foto_recortada.pack()

        btn_guardar = tk.Button(ventana_foto, text="Guardar", command=lambda: guardar_foto(img_recortada))
        btn_guardar.pack(pady=10)

        btn_repetir = tk.Button(ventana_foto, text="Repetir Fotografía", command=ventana_foto.destroy)
        btn_repetir.pack(pady=10)

        btn_copiar = tk.Button(ventana_foto, text="Copiar al Portapapeles", command=lambda: copiar_al_portapapeles(img_recortada))
        btn_copiar.pack(pady=10)

def copiar_al_portapapeles(imagen):
    output = io.BytesIO()
    imagen.convert("RGB").save(output, format="BMP")
    data = output.getvalue()[14:]  # Saltar el header de BMP
    output.close()
    
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

def guardar_foto(img_recortada):
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

    if file_path:
        img_recortada.save(file_path)
        
def set_dpi_awareness():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # DPI aware
    except Exception as e:
        print(f"Error setting DPI awareness: {e}")
        
root = tk.Tk()
root.geometry('1000x650')
set_dpi_awareness()

iniciar_cam_btn = tk.Button(root, text="Iniciar Cámara", bg="#32bea6",cursor="hand2",command=video_camara,width=15,height=3,font=("Calisto MT",12,"bold")).place(x=750,y=100)

tomar_foto_btn = tk.Button(root, text="Tomar fotografía", bg="#32bea6",cursor="hand2",command=tomar_foto,width=15,height=3,font=("Calisto MT",12,"bold")).place(x=750,y=200)

detener_cam_btn = tk.Button(root, text="Detener Cámara", bg="#ff4500", cursor="hand2",command=detener_video, width=15,height=3, font=("Calisto MT", 12, "bold")).place(x=750, y=300)

cerrar_btn = tk.Button(root, text="Cerrar Programa", bg="#ff4500", cursor="hand2",command=cerrar_ventana, width=15,height=3, font=("Calisto MT", 12, "bold")).place(x=750, y=400)

etiqueta_video = tk.Label(root,bg="black")
etiqueta_video.place(x=300,y=80)

root.mainloop()
