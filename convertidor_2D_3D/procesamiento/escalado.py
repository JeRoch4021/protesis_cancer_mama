# Librerías utilizadas para el archivo
import os
import shutil
from PIL import Image

# Reduce el tamaño de las imágenes y convierte fondos transparentes
# a negro para optimizar la recontrucción 3D en COLMAP
def escalar_imagenes (carpeta_origen, carpeta_destino, nuevo_ancho = 1024):
    # Verifica si existe la carpeta de destino, con el fin de borrar archivos duplicados o basura
    if os.path.exists(carpeta_destino):
        print(f"Limpiando carpeta de imágenes reescaladas: {carpeta_destino}")
        shutil.rmtree(carpeta_destino)

    os.makedirs(carpeta_destino, exist_ok=True)

    # Itera sobre cada archivo presente en la carpeta de origen
    for nombre_archivo in os.listdir(carpeta_origen):
        ruta_original = os.path.join(carpeta_origen, nombre_archivo)

        # Cambia la extensión original a .jpg (estándar óptimo para COLMAP)
        nombre_salida = os.path.splitext(nombre_archivo)[0] + ".jpg"
        ruta_destino = os.path.join(carpeta_destino, nombre_salida)

        try:
            with Image.open(ruta_original) as img:
                # Corrección: Si la imagen tiene transparencia (RGBA), la aplanamos
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGBA")
                    # Creamos un fondo negro (0,0,0) del mismo tamaño que la imagen original
                    fondo = Image.new("RGB", img.size, (0, 0, 0))
                    # Pegamos la imagen sobre el fondo negro usando su propio canal alfa como máscara
                    # Esto evita que el área eliminada se vea como ruido o colores extraños
                    fondo.paste(img, mask=img.split()[3]) # El canal 3 es el Alfa
                    img = fondo
                else:
                    # Si no tiene transparencia, simplemente nos aseguramos de que esté en formato RGB
                    img = img.convert("RGB")

                # Mantener proporción al redimensionar
                # Calculamos cuanto se debe escalar el alto basándonos en el nuevo ancho (1024px por defecto)
                proporcion = nuevo_ancho / img.width
                nuevo_alto = int(img.height * proporcion)
                # Redimensionar la imagen usando el filtro LANCZOS (alta calidad para detalles pequeños)
                imagen_redimensionada = img.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
                # Guardamos el resultado como JPEG con calidad del 95% para no perder detalles del objeto
                imagen_redimensionada.save(ruta_destino, "JPEG", quality=95)

        except Exception as e:
            # En caso de que el archivo esté corrupto o no sea una imagen, se muestra el error y continúa
            print(f"Error al procesar {nombre_archivo}: {e}")