import open3d as o3d

def generar_malla_stl(ply_file, stl_file):
    print(f"Cargando nube de puntos desde {ply_file}...")
    nube = o3d.io.read_point_cloud(ply_file)

    print("Estimando normales...")
    nube.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
        radius=0.05, max_nn=30))

    print("Reconstruyendo malla con Poisson...")
    malla, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        nube, depth=9
    )

    print("Limpiando malla...")
    bbox = nube.get_axis_aligned_bounding_box()
    malla = malla.crop(bbox)

    print("Recalculando normales de la malla...")
    malla.compute_vertex_normals()

    print(f"Guardando malla en {stl_file}...")
    o3d.io.write_triangle_mesh(stl_file, malla)

if __name__ == "__main__":

    # Convertir nube de puntos a malla STL
    generar_malla_stl(
        ply_file = ".\\modelo_3D\\dense\\fused.ply",
        stl_file = ".\\modelo_3D\\dense\\modelo.stl"
    )