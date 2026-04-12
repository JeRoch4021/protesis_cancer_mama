import os
import subprocess
import shutil
from PIL import Image
import open3d as o3d

def ejecutar_comando(comando):
    print("Ejecutando:", " ".join(comando))
        
    resultado = subprocess.run(comando, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
    print(resultado.stdout)
    if resultado.returncode != 0:
        print("Error:", resultado.stderr)
        raise RuntimeError("Error ejecutando COLMAP")
    return resultado

def escalar_imagenes(carpeta_origen, carpeta_destino, nuevo_ancho = 1024):
    if os.path.exists(carpeta_destino):
        print(f"Limpiando carpeta de imágenes reescaladas: {carpeta_destino}")
        shutil.rmtree(carpeta_destino)

    os.makedirs(carpeta_destino, exist_ok=True)

    for nombre_archivo in os.listdir(carpeta_origen):
        ruta_original = os.path.join(carpeta_origen, nombre_archivo)
        ruta_destino = os.path.join(carpeta_destino, nombre_archivo)

        try:
            with Image.open(ruta_original) as img:
                # Mantener proporción al redimensionar
                proporcion = nuevo_ancho / img.width
                nuevo_alto = int(img.height * proporcion)
                imagen_redimensionada = img.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
                imagen_redimensionada.save(ruta_destino)
        except Exception as e:
            print(f"No se pudo escalar {nombre_archivo}: {e}")

def reconstruir_modelo_colmap(ruta_imagenes, ruta_proyecto, limpiar = True):
    ruta_db = os.path.join(ruta_proyecto, "database.db")
    ruta_sparse = os.path.join(ruta_proyecto, "sparse")
    ruta_dense = os.path.join(ruta_proyecto, "dense")

    # Crear carpeta principal y subcarpetas
    if limpiar and os.path.exists(ruta_proyecto):
        print(f"Limpiando carpeta existente: {ruta_proyecto}")
        shutil.rmtree(ruta_proyecto)

    os.makedirs(ruta_sparse, exist_ok=True)
    os.makedirs(ruta_dense, exist_ok=True)

    # 1. Extracción de características
    ejecutar_comando([
        "colmap", "feature_extractor",
        "--database_path", ruta_db,
        "--image_path", ruta_imagenes,
        "--ImageReader.single_camera", "1"
    ])

    # 2. Emparejamiento de imágenes
    ejecutar_comando([
        "colmap", "exhaustive_matcher",
        "--database_path", ruta_db
    ])

    # 3. Reconstrucción Estructura desde Movimiento (SfM)
    ejecutar_comando([
        "colmap", "mapper",
        "--database_path", ruta_db,
        "--image_path", ruta_imagenes,
        "--output_path", ruta_sparse
    ])

    # 4. Preparar para reconstrucción densa
    ejecutar_comando([
        "colmap", "image_undistorter",
        "--image_path", ruta_imagenes,
        "--input_path", os.path.join(ruta_sparse, "0"),
        "--output_path", ruta_dense,
        "--output_type", "COLMAP"
    ])

    # 5. Reconstrucción densa (depth maps)
    ejecutar_comando([
        "colmap", "patch_match_stereo",
        "--workspace_path", ruta_dense,
        "--workspace_format", "COLMAP",
        "--PatchMatchStereo.geom_consistency", "true"
    ])

    # 6. Fusión de profundidad
    ejecutar_comando([
        "colmap", "stereo_fusion",
        "--workspace_path", ruta_dense,
        "--workspace_format", "COLMAP",
        "--input_type", "geometric",
        "--output_path", os.path.join(ruta_dense, "fused.ply")
    ])

    # Generar malla con Poisson Mesher
    ejecutar_comando([
        "colmap", "poisson_mesher",
        "--input_path", os.path.join(ruta_proyecto, "dense", "fused.ply"),
        "--output_path", os.path.join(ruta_proyecto, "dense", "mesh.ply")
    ])

    print("Reconstrucción completa. ")
    print("Modelo guardado en:", os.path.join(ruta_dense, "fused.ply"))


# ----------- USO ------------
if __name__ == "__main__":
    carpeta_original = ".\\imagenes"
    carpeta_reescalada = ".\\imagenes_reescaladas"

    escalar_imagenes(carpeta_original, carpeta_reescalada, nuevo_ancho = 1024)

    reconstruir_modelo_colmap(
        ruta_imagenes = carpeta_reescalada,
        ruta_proyecto = ".\\modelo_3D",
        limpiar = True
    )