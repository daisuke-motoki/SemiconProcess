import numpy as np
import settings


if __name__ == "__main__":
    filename = "initial_wafer_phantoms.npz"
    shape = (5, 2, 10)
    material_id_name = settings.MATERIAL_INDEX_NAME
    vacuum_mat_id = 0
    z_layer_materials = {
        "Silicon": [0, 2],
        "SiO2": [2, 4],
        "PhotoResist": [4, 5],
    }
    excavation_zyx = [
        [[4, 5], [0, 2], [0, 4]],
        [[4, 5], [0, 2], [5, 6]],
        [[4, 5], [0, 2], [7, 8]],
        [[4, 5], [0, 2], [9, 10]],
    ]

    material_name_id = dict()
    for key, name in material_id_name.items():
        material_name_id[name] = key

    voxels = np.zeros((shape[0], shape[1], shape[2], len(material_id_name)))
    # fill materials
    for mat_name, z_range in z_layer_materials.items():
        mat_id = material_name_id[mat_name]
        voxels[z_range[0]:z_range[1], :, :, mat_id] = 1.0
    # excavation
    assign_vacuum = [0.]*len(material_id_name)
    assign_vacuum[vacuum_mat_id] = 1.0
    for z_range, y_range, x_range in excavation_zyx:
        voxels[z_range[0]:z_range[1],
               y_range[0]:y_range[1],
               x_range[0]:x_range[1]] = assign_vacuum

    voxels = voxels.reshape(-1, len(material_id_name))
    np.savez_compressed(filename, voxel=voxels)
