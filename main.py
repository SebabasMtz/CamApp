import tkinter as tk
from tkinter import filedialog 
import cv2
from PIL import Image, ImageTk
import imutils


video = None
is_on = False

def video_camara():
  global video
  video = cv2.VideoCapture(1) #0 = EOS Cam // #1 = WebCam
  etiqueta_cam.config(text="Usando cámara 1")
  iniciar()

def cambiar_camara():
    global video
    global is_on
    if is_on:
        is_on = False
        video = cv2.VideoCapture(1)
        etiqueta_cam.config(text="Usando cámara 1")
        iniciar()
    else:
        is_on = True
        video = cv2.VideoCapture(0)
        etiqueta_cam.config(text="Usando cámara 2")
        iniciar()

def iniciar():
  global video
  ret, frame = video.read()
  if ret == True:
        frame = imutils.resize(frame, width=700)
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
    if ret == True:
        frame = imutils.resize(frame, width=700)
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

def guardar_foto(img_recortada):
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

    if file_path:
        img_recortada.save(file_path)

        
root = tk.Tk()
root.state('zoomed')

fondo_inicio = tk.PhotoImage(file="./img/INICIO.png")
fondo_inicio_label = tk.Label(root, image=fondo_inicio).place(x=0,y=0,relwidth=1,relheight=1)

iniciar_cam_btn = tk.Button(root, text="Iniciar Cámara", bg="#32bea6",cursor="hand2",command=video_camara,width=15,height=3,font=("Calisto MT",12,"bold")).place(x=340,y=720)

tomar_foto_btn = tk.Button(root, text="Tomar fotografía", bg="#32bea6",cursor="hand2",command=tomar_foto,width=15,height=3,font=("Calisto MT",12,"bold")).place(x=540,y=720)

detener_cam_btn = tk.Button(root, text="Detener Cámara", bg="#ff4500", cursor="hand2",command=detener_video, width=15,height=3, font=("Calisto MT", 12, "bold")).place(x=740, y=720)

cerrar_btn = tk.Button(root, text="Cerrar Programa", bg="#ff4500", cursor="hand2",command=cerrar_ventana, width=15,height=3, font=("Calisto MT", 12, "bold")).place(x=940, y=720)

cambiar_cam_btn = tk.Button(root, text="Cambiar cámara", bg="#32bea6", cursor="hand2",command=cambiar_camara, width=15,height=3, font=("Calisto MT", 12, "bold")).place(x=1000, y=320)

etiqueta_cam = tk.Label(root,text="Usando cámara 1",font=("Calisto MT",12,"bold"))
etiqueta_cam.place(x=1015,y=400)

etiqueta_video = tk.Label(root,bg="black")
etiqueta_video.place(x=520,y=220)

root.mainloop()
