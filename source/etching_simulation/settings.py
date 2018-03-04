
COLOR_MAP = dict(
    Vacuum=[1.0, 1.0, 1.0, 0.1],
    Silicon=[0.8, 0.5, 0.5, 0.5],
    SiO2=[0.7, 0.7, 0.7, 0.5],
    PhotoResist=[1.0, 0.8, 0.8, 0.5],
)

MATERIAL_ID_NAME = {
    0: "Vacuum",
    1: "Silicon",
    2: "SiO2",
    3: "PhotoResist"
}

# geometrical parameters [micro meter]
world_length_x = 10.0/2.0
world_length_y = 10.0/2.0
world_length_z = 10.0/2.0

process_space_length_x = 10.0/2.0
process_space_length_y = 10.0/2.0
process_space_length_z = 5.0/2.0

n_voxel_x = 10
n_voxel_y = 10
n_voxel_z = 5
