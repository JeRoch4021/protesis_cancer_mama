import os
import shutil
from rembg import remove

def quitar_fondo(carpeta_origen, carpeta_destino):
    if os.path.exists(carpeta_destino):
        shutil.rmtree(carpeta_destino)
    os.makedirs(carpeta_destino, exist_ok=True)

    print("Eliminando fondos...")
    for nombre_archivo in os.listdir(carpeta_origen):
        ruta_in = os.path.join(carpeta_origen, nombre_archivo)
        ruta_out = os.path.join(carpeta_destino, nombre_archivo)

        try:
            with open(ruta_in, 'rb') as i:
                input_image = i.read()
                output_image = remove(input_image)
                with open(ruta_out, 'wb') as o:
                    o.write(output_image)
        except Exception as e:
            print(f"No se pudo procesar el fondo de {nombre_archivo}: {e}")