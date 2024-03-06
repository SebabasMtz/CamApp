import tkinter as tk
import cv2
from PIL import Image, ImageTk
import imutils

video = None

def video_camara():
  global video
  video = cv2.VideoCapture(0)
  iniciar()

def iniciar():
  global videoret 
  ret, frame = video.read()
  if ret == True:
    frame = imutils.resize(frame, width=640)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    image = ImageTk.PhotoImage(image=img)
    etiqueta_video.configure(image=image)
    etiqueta_video.image = image
    etiqueta_video.after(10,iniciar)

root = tk.Tk()
root.state('zoomed')

fondo_inicio = tk.PhotoImage(file="./img/INICIO.png")
fondo_inicio_label = tk.Label(root, image=fondo_inicio).place(x=0,y=0,relwidth=1,relheight=1)

iniciar_cam_btn = tk.Button(root, text="Iniciar Cámara", bg="#32bea6",relief="flat",cursor="hand2",command=video_camara,width=15,height=3,font=("Calisto MT",12,"bold")).place(x=640,y=720)

etiqueta_video = tk.Label(root,bg="white")
etiqueta_video.place(x=520,y=225)
root.mainloop()
