# process
ETCHING_ACCELERATION_FACTOR = 100000

# material properties
MATERIAL_INDEX_NAME = {
    0: "Vacuum",
    1: "Silicon",
    2: "SiO2",
    3: "PhotoResist"
}

COLOR_MAP = dict(
    Vacuum=[1.0, 1.0, 1.0, 0.1],
    Silicon=[0.8, 0.5, 0.5, 0.5],
    SiO2=[0.7, 0.7, 0.7, 0.5],
    PhotoResist=[1.0, 0.8, 0.8, 0.5],
)

# physics descriptions
REACTIVE_PARTICLE_PROCESS_TABLE_PATH = \
    "data/reactive_particle_process_table.csv"
# reactive_particle_table = {
#     "Ar40": {
#         "Silicon": {
#             "ionIoni": [
#                 {"type": "etching",
#                  "min_energy": 0.0,
#                  "probability": 1.0},
#             ]
#         },
#         "SiO2": {
#             "ionIoni": [
#                 {"type": "etching",
#                  "min_energy": 0.0,
#                  "probability": 1.0},
#             ],
#         },
#     },
# }

# geometrical parameters [micro meter]
world_length_x = 5.0/2.0
world_length_y = 1.0/2.0
world_length_z = 10.0/2.0

process_space_length_x = 5.0/2.0
process_space_length_y = 1.0/2.0
process_space_length_z = 5.0/2.0

n_voxel_x = 50
n_voxel_y = 10
n_voxel_z = 50
