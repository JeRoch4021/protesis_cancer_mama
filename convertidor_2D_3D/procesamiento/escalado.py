import os
import shutil
from PIL import Image

def escalar_imagenes (carpeta_origen, carpeta_destino, nuevo_ancho = 1024):
    if os.path.exists(carpeta_destino):
        print(f"Limpiando carpeta de imágenes reescaladas: {carpeta_destino}")
        shutil.rmtree(carpeta_destino)

    os.makedirs(carpeta_destino, exist_ok=True)

    for nombre_archivo in os.listdir(carpeta_origen):
        ruta_original = os.path.join(carpeta_origen, nombre_archivo)

        nombre_salida = os.path.splitext(nombre_archivo)[0] + ".jpg"
        ruta_destino = os.path.join(carpeta_destino, nombre_salida)

        try:
            with Image.open(ruta_original) as img:
                # Correccion: Si la imagen tiene transparencia (RGBA), la aplanamos
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGBA")
                    # Creamos un fondo negro (0,0,0) del mismo tiempo
                    fondo = Image.new("RGB", img.size, (0, 0, 0))
                    fondo.paste(img, mask=img.split()[3]) # El canal 3 es el Alfa
                    img = fondo
                else:
                    img = img.convert("RGB")

                # Mantener proporción al redimensionar
                proporcion = nuevo_ancho / img.width
                nuevo_alto = int(img.height * proporcion)
                imagen_redimensionada = img.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
                # Lo guardamos como JPEG
                imagen_redimensionada.save(ruta_destino, "JPEG", quality=95)

        except Exception as e:
            print(f"Error al procesar {nombre_archivo}: {e}")