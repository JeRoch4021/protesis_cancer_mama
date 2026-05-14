# Librerías utilizadas para el archivo
import os
import shutil
from rembg import remove

# Función que permite leer todas las imágenes de una carpeta 
# para eliminar el fondo usando IA y guardar los resultados en una nueva carpeta
def quitar_fondo(carpeta_origen, carpeta_destino):
    # Borramos la carpeta para evitar mezclar contenido viejo con nuevo
    if os.path.exists(carpeta_destino):
        shutil.rmtree(carpeta_destino)
    os.makedirs(carpeta_destino, exist_ok=True)

    print("Eliminando fondos...")
    # Recorre cada archivo dentro de la carpeta donde están las fotos originales
    for nombre_archivo in os.listdir(carpeta_origen):
        # Construye la ruta completa de entrada
        ruta_in = os.path.join(carpeta_origen, nombre_archivo)
        # Construye la ruta completa de salida
        ruta_out = os.path.join(carpeta_destino, nombre_archivo)

        try:
            # Abre la imagen original en modo de lectura binaria
            with open(ruta_in, 'rb') as i:
                input_image = i.read()
                # Procesa la imagen con la IA de rembg para detectar el sujeto y quitar el fondo
                output_image = remove(input_image)
                # Abre o crea el archivo de destino en modo de escritura binaria 
                with open(ruta_out, 'wb') as o:
                    o.write(output_image) # Guarda la imagen procesada (ahora tiene transparencia)
        except Exception as e:
            # Si ocurre un error lo reporta sin detener el programa
            print(f"No se pudo procesar el fondo de {nombre_archivo}: {e}")