# Librerías utilizadas para el archivo
import os
from procesamiento.eliminacion_fondo import quitar_fondo
from procesamiento.escalado import escalar_imagenes
from fotogrametria.motor_colmap import reconstruir_modelo_colmap

# ----------- USO ------------
if __name__ == "__main__":
    directorio_base = os.getcwd()
    fotos_originales = os.path.join(directorio_base, "interfaz_grafica", "Imagenes_capturas")
    fotos_sin_fondo = os.path.join(directorio_base, "convertidor_2D_3D", "imagenes_sin_fondo")
    fotos_reescaladas = os.path.join(directorio_base, "convertidor_2D_3D", "imagenes_reescaladas")

    quitar_fondo(fotos_originales, fotos_sin_fondo)
    escalar_imagenes(fotos_sin_fondo, fotos_reescaladas)

    reconstruir_modelo_colmap(
        ruta_imagenes = fotos_reescaladas,
        ruta_proyecto = os.path.join(directorio_base, "convertidor_2D_3D", "modelo_3D")
    )

    # # Convertir nube de puntos a malla STL
    # generar_malla_stl(
    #     ply_file = ".\\modelo_3D\\dense\\fused.ply",
    #     stl_file = ".\\modelo_3D\\dense\\modelo.stl"
    # )