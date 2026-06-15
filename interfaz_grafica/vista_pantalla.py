#Importación de librerias
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import imutils
import numpy as np
import os
import modelo_pantalla as modelo

class VistaPantalla:
    def __init__ (self, modelo):
        self.modelo = modelo
        #Construcción de la pantalla
        self.pantalla = tk.Tk()
        self.pantalla.title("Escaner Modelador")
        self.pantalla.geometry("1038x650")
        self.pantalla.resizable(0,0)
    
        #Implementar una imagen de fondo para personalizar la pantalla
        self.ruta_imagen_fondo = "interfaz_grafica/Detalles_de_pantalla/fondo_de_pantalla.png"
        self.imagen_fondo = tk.PhotoImage(file=self.ruta_imagen_fondo)
        self.background = tk.Label(image=self.imagen_fondo, text="Fondo")
        self.background.place(x=0, y=0, relwidth=1, relheight=1)

        #Implementar etiquetas de texto en la pantalla
        self.etiqueta_control = tk.Label(self.pantalla, text="CONTROLES DE VIDEO:")
        self.etiqueta_control.place(x=100, y=10)

        self.etiqueta_video = tk.Label(self.pantalla, text="VIDEO EN TIEMPO REAL:")
        self.etiqueta_video.place(x=580, y=10)
        self.etiqueta_filtro = tk.Label(self.pantalla, text="FILTROS DE CAMARA:")
        self.etiqueta_filtro.place(x=104, y=220)

        self.etiqueta_canny = tk.Label(self.pantalla, text="CONTROL DE UMBRALES DE CANNY:")
        self.etiqueta_canny.place(x=57, y=436)

        #Construcción de los botones para navegar con las funciones de la pantalla
        self.ruta_imagen_boton_inicio = "interfaz_grafica/Detalles_de_pantalla/abierto.png"
        self.imagen_boton_inicio = tk.PhotoImage(file=self.ruta_imagen_boton_inicio)
        self.boton_inicio = tk.Button(self.pantalla, text="Iniciar", image=self.imagen_boton_inicio, width=90, height=60, font=("Calibri", 12))
        self.boton_inicio.place(x=70, y=60)

        self.ruta_imagen_boton_fin = "interfaz_grafica/Detalles_de_pantalla/cerrar.png"
        self.imagen_boton_fin = tk.PhotoImage(file=self.ruta_imagen_boton_fin)
        self.boton_fin = tk.Button(self.pantalla, text="Terminar", image=self.imagen_boton_fin, width=90, height=60, font=("Calibri", 12))
        self.boton_fin.place(x=180, y=60)

        self.ruta_imagen_boton_iniciar_grabacion = "interfaz_grafica/Detalles_de_pantalla/captura.png"
        self.imagen_boton_iniciar_grabacion = tk.PhotoImage(file=self.ruta_imagen_boton_iniciar_grabacion)
        self.boton_iniciar_grabacion = tk.Button(self.pantalla, text="Capturar", image=self.imagen_boton_iniciar_grabacion, width=90, height=50, font=("Calibri", 12))
        self.boton_iniciar_grabacion.place(x=70, y=137)
        self.boton_iniciar_grabacion.config(state=tk.DISABLED)

        self.ruta_imagen_boton_detener_grabacion = "interfaz_grafica/Detalles_de_pantalla/parar.png"
        self.imagen_boton_detener_grabacion = tk.PhotoImage(file=self.ruta_imagen_boton_detener_grabacion)
        self.boton_detener_grabacion = tk.Button(self.pantalla, text="Detener Grabacion", image=self.imagen_boton_detener_grabacion, width=90, height=50, font=("Calibri", 12))
        self.boton_detener_grabacion.place(x=180, y=137)
        self.boton_detener_grabacion.config(state=tk.DISABLED)

        self.ruta_imagen_boton_rgb = "interfaz_grafica/Detalles_de_pantalla/rgb.png"
        self.imagen_boton_rgb = tk.PhotoImage(file=self.ruta_imagen_boton_rgb)
        self.boton_rgb = tk.Button(self.pantalla, text="RGB", image=self.imagen_boton_rgb, width=200, height=40, font=("Calibri", 12))
        self.boton_rgb.place(x=70, y=265)

        self.ruta_imagen_boton_grises = "interfaz_grafica/Detalles_de_pantalla/grises.png"
        self.imagen_boton_grises = tk.PhotoImage(file=self.ruta_imagen_boton_grises)
        self.boton_grises = tk.Button(self.pantalla, text="Grises", image=self.imagen_boton_grises, width=200, height=40, font=("Calibri", 12))
        self.boton_grises.place(x=70, y=315)

        self.ruta_imagen_boton_canny = "interfaz_grafica/Detalles_de_pantalla/canny.png"
        self.imagen_boton_canny = tk.PhotoImage(file=self.ruta_imagen_boton_canny)
        self.boton_canny = tk.Button(self.pantalla, text="Canny", image=self.imagen_boton_canny, width=200, height=40, font=("Calibri", 12))
        self.boton_canny.place(x=70, y=365)

        self.ruta_imagen_boton_ia = "interfaz_grafica/Detalles_de_pantalla/ia.png"
        self.imagen_boton_ia = tk.PhotoImage(file=self.ruta_imagen_boton_ia)
        self.boton_ia = tk.Button(self.pantalla, text="Activar Clasificador", image=self.imagen_boton_ia, width=200, height=40, font=("Calibri", 12))
        self.boton_ia.place(x=380, y=560)
        
        self.ruta_imagen_extraer_frames = "interfaz_grafica/Detalles_de_pantalla/extraer_frames.png"
        self.imagen_extraer_frames = tk.PhotoImage(file=self.ruta_imagen_extraer_frames)
        self.boton_extraer_frames = tk.Button(self.pantalla, text="Extraer Frames", image=self.imagen_extraer_frames, width=200, height=40, font=("Calibri", 12))
        self.boton_extraer_frames.place(x=680, y=560)

        #Sliders para controlar el valor de los umbrales alto y bajo del filtro de cámara: "Canny"
        self.slider_umbral_alto = tk.Scale(self.pantalla, from_=0, to=255, orient=tk.HORIZONTAL)
        self.slider_umbral_alto.place(x=70, y=490, width=205)
        self.slider_umbral_bajo = tk.Scale(self.pantalla, from_=0, to=255, orient=tk.HORIZONTAL)
        self.slider_umbral_bajo.place(x=70, y=560, width=205)

        #Ubicacion de la camara de video
        self.lblVideo = tk.Label(self.pantalla)