import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk

class CamaraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación de Cámara")
        self.root.state('zoomed')
        self.root.resizable(width=False,height=False)

        self.iniciar_btn = ttk.Button(root, text="Iniciar Cámara", command=self.iniciar_camara)
        self.iniciar_btn.pack(pady=10)

        self.tomar_foto_btn = ttk.Button(root, text="Tomar Foto", command=self.tomar_foto, state=tk.DISABLED)
        self.tomar_foto_btn.pack(pady=10)

        self.guardar_btn = ttk.Button(root, text="Guardar Foto", command=self.guardar_foto, state=tk.DISABLED)
        self.guardar_btn.pack(pady=10)

        self.resetear_btn = ttk.Button(root, text="Resetear", command=self.resetear, state=tk.DISABLED)
        self.resetear_btn.pack(pady=10)

        self.cap = None  # Objeto de captura de la cámara
        self.foto_tomada = None  # Variable para almacenar la foto tomada

    def iniciar_camara(self,camara_idx=0,ancho=640,alto=480):
        self.cap = cv2.VideoCapture()
        self.cap = cv2.VideoCapture(camara_idx)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, ancho)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, alto)

        if not self.cap.isOpened():
            print("Error al abrir la cámara")
        else:
            self.iniciar_btn.config(state=tk.DISABLED)
            self.tomar_foto_btn.config(state=tk.NORMAL)

    def tomar_foto(self):
        ret, frame = self.cap.read()  # Capturar un fotograma de la cámara
        if ret:
            # Convertir el fotograma de la cámara a una imagen compatible con Tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.foto_tomada = ImageTk.PhotoImage(Image.fromarray(frame_rgb))

            # Mostrar la foto tomada en una etiqueta
            self.label_foto = ttk.Label(self.root, image=self.foto_tomada)
            self.label_foto.pack()

            # Habilitar los botones de guardar y resetear
            self.guardar_btn.config(state=tk.NORMAL)
            self.resetear_btn.config(state=tk.NORMAL)

    def guardar_foto(self):
        if self.foto_tomada:
            # Puedes personalizar la lógica de guardado según tus necesidades
            self.foto_tomada.image.save("foto_infantil.png")

    def resetear(self):
        # Eliminar la etiqueta de la foto
        self.label_foto.destroy()

        # Deshabilitar los botones de guardar y resetear
        self.guardar_btn.config(state=tk.DISABLED)
        self.resetear_btn.config(state=tk.DISABLED)

root = tk.Tk()
fondo_inicio = tk.PhotoImage(file="./img/INICIO.png")
fondo_foto = tk.PhotoImage(file="./img/FOTOGRAFÍA.png")
fondo_ressav = tk.PhotoImage(file="./img/RESSAV.png")
app = CamaraApp(root)
root.mainloop()
