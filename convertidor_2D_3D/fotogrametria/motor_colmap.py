import os
import subprocess
import shutil
import open3d as o3d


def ejecutar_comando(comando):
    print("Ejecutando:", " ".join(comando))
        
    resultado = subprocess.run(comando, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
    print(resultado.stdout)
    if resultado.returncode != 0:
        print("Error:", resultado.stderr)
        raise RuntimeError("Error ejecutando COLMAP")
    return resultado


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
        "--ImageReader.single_camera", "1",  
        "--SiftExtraction.max_num_features", "12000", # Forzar más puntos
        "--SiftExtraction.estimate_affine_shape", "1",  # Ayuda con los ángulos de los costados
        "--SiftExtraction.upright", "1"
    ])

    # 2. Emparejamiento de imágenes
    ejecutar_comando([
        "colmap", "exhaustive_matcher",
        "--database_path", ruta_db,
        "--SiftMatching.guided_matching", "1"
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

    print("Reconstrucción completa. ")
    print("Modelo guardado en:", os.path.join(ruta_dense, "fused.ply"))