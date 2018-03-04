import numpy as np
import settings


if __name__ == "__main__":
    filename = "initial_wafer_phantoms.npz"
    shape = (5, 10, 10)
    material_names = settings.MATERIAL_ID_NAME
    default = 0
    voxels = np.array([default] * (shape[0] * shape[1] * shape[2]))
    voxels = voxels.reshape(shape)

    silicon_z = [(0, 2)]
    silicon_x = [(0, 10)]
    silicon_y = [(0, 10)]
    sio2_z = [(2, 3)]
    sio2_x = [(0, 10)]
    sio2_y = [(0, 10)]
    resist_z = [(3, 4), (3, 4)]
    resist_x = [(2, 4), (6, 8)]
    resist_y = [(0, 10), (0, 10)]

    material_assign = dict()
    material_assign[1] = [silicon_x, silicon_y, silicon_z]
    # material_assign[2] = [sio2_x, sio2_y, sio2_z]
    # material_assign[3] = [resist_x, resist_y, resist_z]
    for name_ind, vertexes in material_assign.items():
        for i in range(len(vertexes[0])):
            x0 = vertexes[0][i][0]
            x1 = vertexes[0][i][1]
            y0 = vertexes[1][i][0]
            y1 = vertexes[1][i][1]
            z0 = vertexes[2][i][0]
            z1 = vertexes[2][i][1]
            voxels[z0:z1, y0:y1, x0:x1] = name_ind

    voxels = voxels.flatten()
    densities = np.array([-1.]*len(voxels))
    np.savez_compressed(filename, voxel=voxels, density=densities)
