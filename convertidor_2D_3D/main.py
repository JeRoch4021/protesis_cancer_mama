import os
from procesamiento.eliminacion_fondo import quitar_fondo
from procesamiento.escalado import escalar_imagenes
from fotogrametria.motor_colmap import reconstruir_modelo_colmap

# ----------- USO ------------
if __name__ == "__main__":
    directorio_base = os.getcwd()
    fotos_originales = os.path.join(directorio_base, "imagenes")
    fotos_sin_fondo = os.path.join(directorio_base, "imagenes_sin_fondo")
    fotos_reescaladas = os.path.join(directorio_base, "imagenes_reescaladas")

    quitar_fondo(fotos_originales, fotos_sin_fondo)
    escalar_imagenes(fotos_sin_fondo, fotos_reescaladas)

    reconstruir_modelo_colmap(
        ruta_imagenes = fotos_reescaladas,
        ruta_proyecto = ".\\modelo_3D"
    )

    # # Convertir nube de puntos a malla STL
    # generar_malla_stl(
    #     ply_file = ".\\modelo_3D\\dense\\fused.ply",
    #     stl_file = ".\\modelo_3D\\dense\\modelo.stl"
    # )