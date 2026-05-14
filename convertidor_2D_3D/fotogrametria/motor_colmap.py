# Librerías utilizadas para el archivo
import os
import subprocess
import shutil
import open3d as o3d

# Función auxiliar para ejecutar comandos en la terminal y capturar errores
def ejecutar_comando(comando):
    print("Ejecutando:", " ".join(comando))
    
    # Ejecuta el comando, guarda la salida (stdout) y los errores (stderr) en variables
    resultado = subprocess.run(comando, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
    # Muestra la respuesta estándar de COLMAP en la consola de python
    print(resultado.stdout)
    # Si el código de retorno no es 0, Significa que hubo un error en la ejecución
    if resultado.returncode != 0:
        # Se muestra el error específico y detiene el programa con una alerta
        print("Error:", resultado.stderr)
        raise RuntimeError("Error ejecutando COLMAP")
    return resultado

# Función principal para orquestar la reconstrucción 3D
def reconstruir_modelo_colmap(ruta_imagenes, ruta_proyecto, limpiar = True):
    # Define las rutas para la base de datos SQL y las carpetas de salida
    ruta_db = os.path.join(ruta_proyecto, "database.db")  # Archivo donde se guardan los "matches"
    ruta_sparse = os.path.join(ruta_proyecto, "sparse")   # Carpeta para la nube de puntos básica 
    ruta_dense = os.path.join(ruta_proyecto, "dense")     # Carpeta para el modelo detallado

    # Si se activa 'limpiar', se borran reconstrucciones anteriores para evitar conflictos
    if limpiar and os.path.exists(ruta_proyecto):
        print(f"Limpiando carpeta existente: {ruta_proyecto}")
        print()
        shutil.rmtree(ruta_proyecto) # Se borra carpeta completa y su contenido

    # Crea las carpetas necesarias si no existen (evita errores de ruta)
    os.makedirs(ruta_sparse, exist_ok=True)
    os.makedirs(ruta_dense, exist_ok=True)

    # Comando 1. Extracción de características (SIFT)
    # Detecta puntos clave en las imágenes (esquinas, bordes, texturas)
    ejecutar_comando([
        "colmap", "feature_extractor",    
        "--database_path", ruta_db,       # Donde guardar los puntos encontrados
        "--image_path", ruta_imagenes,    # Carpeta con tus fotos del maniquí
        "--ImageReader.single_camera", "1",    # Indica que todas las fotos son de la misma cámara
        "--SiftExtraction.max_num_features", "12000",   # Aumenta la cantidad de puntos buscados
        "--SiftExtraction.estimate_affine_shape", "1",  # Mejora la detección en superficies inclinadas 
        "--SiftExtraction.upright", "1"   # Asume que las fotos no están rotadas de lado
    ])

    # Comando 2. Emparejamiento (Matching)
    # Compara los puntos de cada imagen con todas las demás para encontrar coincidencias
    ejecutar_comando([
        "colmap", "exhaustive_matcher",    # Compara cada foto contra todas (más lento pero preciso)
        "--database_path", ruta_db,
        "--SiftMatching.guided_matching", "1"    # Usa la geometría para rescatar puntos perdidos
    ])

    # Comando 3. Reconstrucción de Dispersión (SfM)
    # Crea la estructura inicial (nube de puntos base) y determina la posición de la cámara
    ejecutar_comando([
        "colmap", "mapper",
        "--database_path", ruta_db,
        "--image_path", ruta_imagenes,
        "--output_path", ruta_sparse # Guarda los archivos .bin de la cámara y puntos
    ])

    # Comando 4. Corrección de imagen (Undistorter)
    # Eliminar la distorsión del lente de las fotos para la frase densa
    ejecutar_comando([
        "colmap", "image_undistorter",
        "--image_path", ruta_imagenes,
        "--input_path", os.path.join(ruta_sparse, "0"), # Toma el primer modelo generado
        "--output_path", ruta_dense,
        "--output_type", "COLMAP" # Formato de salida compatible con el siguiente paso
    ])

    # Comando 5. Estéreo de parches (Dense reconstrucción)
    # Calcula la profundidad píxel por píxel para rellenar los huecos del modelo
    ejecutar_comando([
        "colmap", "patch_match_stereo",
        "--workspace_path", ruta_dense,
        "--workspace_format", "COLMAP",
        "--PatchMatchStereo.geom_consistency", "true" # Asegura que los puntos sean coherentes en 3D
    ])

    # Comando 6. Fusión de profundidad
    # Une todos los mapas de profundidad en una sola nube de puntos dense (.ply)
    ejecutar_comando([
        "colmap", "stereo_fusion",
        "--workspace_path", ruta_dense,
        "--workspace_format", "COLMAP",
        "--input_type", "geometric", # Filtrar puntos ruidosos basándose en geometría
        "--output_path", os.path.join(ruta_dense, "fused.ply") # Archivo final de la nube
    ])
    
    # Mensajes finales de confirmación
    print("Reconstrucción completa. ")
    print("Modelo guardado en:", os.path.join(ruta_dense, "fused.ply"))