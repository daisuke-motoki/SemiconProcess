import numpy as np
from collections import OrderedDict

import Geant4 as g4
from g4parameterised import G4PVParameterised
from g4parameterised import PhantomParameterisationColour
import settings


class DeviceConstruction(g4.G4VUserDetectorConstruction):
    """
    """
    def __init__(self, init_filename):
        """
        """
        super(DeviceConstruction, self).__init__()
        self.phantom_filename = init_filename

        self.world_physical = None
        self.world_material = None
        self.process_space_material = None

        self.original_materials = dict()

        self.materials = None
        self.material_IDs = None

        self.n_voxel_x = settings.n_voxel_x
        self.n_voxel_y = settings.n_voxel_y
        self.n_voxel_z = settings.n_voxel_z

    def __del__(self):
        """
        """
        pass

    def Construct(self):
        """
        """
        self.DefineMaterials()
        self.ReadPhantomFile()
        return self.ConstructDevice()

    def DefineMaterials(self):
        """
        """
        nist_manager = g4.G4NistManager.Instance()
        # G4Material * Si = man->FindOrBuildMaterial("G4_Si");

        # elements
        # name = g4.G4String("Oxygen")
        # symbol = g4.G4String("O")
        # z = 8.
        # a = 16.00*g4.g/g4.mole
        # O_element = g4.G4Element(name, symbol, z, a)
        O_element = nist_manager.FindOrBuildElement("O")
        Si_element = nist_manager.FindOrBuildElement("Si")
        C_element = nist_manager.FindOrBuildElement("C")
        H_element = nist_manager.FindOrBuildElement("H")

        # Vacuum
        name = "Vacuum"
        z = 1.
        a = 1.*g4.g/g4.mole
        density = 1.e-20*g4.g/g4.cm3
        Vacuum_material = g4.G4Material(name, z, a, density)

        # Silicon
        name = "Silicon"
        density = 2.3290*g4.g/g4.cm3
        ncomponents = 1
        Silicon_material = g4.G4Material(name, density, ncomponents)
        Silicon_material.AddElement(Si_element, 1)

        # SiO2
        name = "SiO2"
        density = 2.200*g4.g/g4.cm3
        ncomponents = 2
        SiO2_material = g4.G4Material(name, density, ncomponents)
        SiO2_material.AddElement(Si_element, 1./3.)
        SiO2_material.AddElement(O_element, 2./3.)

        # Photo Resist
        name = "PhotoResist"
        density = 2.200*g4.g/g4.cm3  # FIXME
        ncomponents = 2  # FIXME
        PhotoResist_material = g4.G4Material(name, density, ncomponents)
        PhotoResist_material.AddElement(C_element, 2./8.)  # FIXME
        PhotoResist_material.AddElement(H_element, 6./8.)  # FIXME

        self.world_material = Vacuum_material
        self.process_space_material = Vacuum_material
        self.original_materials["Vacuum"] = Vacuum_material
        self.original_materials["Silicon"] = Silicon_material
        self.original_materials["SiO2"] = SiO2_material
        self.original_materials["PhotoResist"] = PhotoResist_material

    def ReadPhantomFile(self, filename=None):
        """
        """
        if filename is None:
            filename = self.phantom_filename
        phantoms = np.load(filename)
        voxels = phantoms["voxel"]
        densities = phantoms["density"]
        material_IDs = list()
        materials_dict = OrderedDict()
        dict_name_ID = dict()
        new_ID = 0
        for mat_ID, density in zip(voxels, densities):
            mat_name = settings.MATERIAL_ID_NAME[mat_ID]
            original = self.original_materials[mat_name]
            original_dens = original.GetDensity() * g4.cm3/g4.g
            if density == -1:
                mat_name = "{}__{}".format(mat_name, original_dens)
                density = original_dens
            else:
                mat_name = "{}__{}".format(mat_name, density)

            material = None
            try:
                material = materials_dict[mat_name]
            except:
                material = self.BuildMaterialWithChangingDensity(original,
                                                                 density,
                                                                 mat_name)
                materials_dict[mat_name] = material
                dict_name_ID[mat_name] = new_ID
                new_ID += 1

            mat_ID = dict_name_ID[mat_name]
            material_IDs.append(mat_ID)

        self.materials = list(materials_dict.values())
        self.material_IDs = material_IDs

    @staticmethod
    def BuildMaterialWithChangingDensity(original, density, name):
        """
        """
        elems = original.GetElementVector()
        nelem = len(elems)
        new_material = g4.G4Material(name, density*g4.g/g4.cm3, nelem)
        for i in range(nelem):
            frac = original.GetFractionVector()[i]
            elem = original.GetElement(i)
            new_material.AddElement(elem, frac)
        return new_material

    def ConstructDevice(self):
        """
        """
        # make colours
        white = g4.G4Color(1.0, 1.0, 1.0)
        orange = g4.G4Color(.75, .55, 0.0)
        world_visatt = g4.G4VisAttributes(True, white)
        process_space_visatt = g4.G4VisAttributes(False, orange)

        # ========
        #  World
        # ========
        world_length_x = settings.world_length_x*g4.micrometer
        world_length_y = settings.world_length_y*g4.micrometer
        world_length_z = settings.world_length_z*g4.micrometer

        world_solid = g4.G4Box("world_solid",
                               world_length_x,
                               world_length_y,
                               world_length_z)

        world_logical = g4.G4LogicalVolume(world_solid,
                                           self.world_material,
                                           "world_logical")
        world_logical.SetVisAttributes(world_visatt)

        self.world_physical = g4.G4PVPlacement(g4.G4Transform3D(),
                                               world_logical,
                                               "world_physical",
                                               None,
                                               False,
                                               0)

        # ===============
        #  process space
        # ===============
        process_space_length_x = settings.process_space_length_x*g4.micrometer
        process_space_length_y = settings.process_space_length_y*g4.micrometer
        process_space_length_z = settings.process_space_length_z*g4.micrometer

        process_space_solid = g4.G4Box("process_space_solid",
                                       process_space_length_x,
                                       process_space_length_y,
                                       process_space_length_z)

        process_space_logical = g4.G4LogicalVolume(process_space_solid,
                                                   self.process_space_material,
                                                   "process_space_logical")
        process_space_logical.SetVisAttributes(process_space_visatt)

        process_space_pos = g4.G4ThreeVector(0, 0, -process_space_length_z)
        process_space_physical = g4.G4PVPlacement(None,
                                                  process_space_pos,
                                                  "process_space_physical",
                                                  process_space_logical,
                                                  self.world_physical,
                                                  False,
                                                  0,
                                                  True)

        # ========================
        #  process wafer phantom
        # ========================
        voxel_length_x = process_space_length_x / self.n_voxel_x
        voxel_length_y = process_space_length_y / self.n_voxel_y
        voxel_length_z = process_space_length_z / self.n_voxel_z
        voxel_solid = g4.G4Box("voxel_solid",
                               voxel_length_x,
                               voxel_length_y,
                               voxel_length_z)
        voxel_logical = g4.G4LogicalVolume(
            voxel_solid, self.process_space_material, "voxel_logical")
        # voxel_logical.SetVisAttributes(g4.G4VisAttributes(G4VisAttributes::GetInvisible()))

        wafer = PhantomParameterisationColour()
        # set color
        for mat_name, color in settings.COLOR_MAP.items():
            cred = color[0]
            cgreen = color[1]
            cblue = color[2]
            copacity = color[3]
            g4_color = g4.G4Color(cred, cgreen, cblue, copacity)
            visAtt = g4.G4VisAttributes(g4_color)
            # visAtt.SetForceSolid(True)
            visAtt.SetVisibility(True)
            wafer.AddColor(mat_name, visAtt)

        wafer.SetVoxelDimensions(voxel_length_x,
                                 voxel_length_y,
                                 voxel_length_z)
        wafer.SetNoVoxel(self.n_voxel_x,
                         self.n_voxel_y,
                         self.n_voxel_z)
        wafer.SetMaterials(self.materials)
        wafer.SetMaterialIndices(self.material_IDs)
        wafer.BuildContainerSolid(process_space_physical)
        wafer.CheckVoxelsFillContainer(process_space_solid.GetXHalfLength(),
                                       process_space_solid.GetYHalfLength(),
                                       process_space_solid.GetZHalfLength())

        n_voxel = self.n_voxel_x * self.n_voxel_y * self.n_voxel_z
        wafer_physical = G4PVParameterised("wafer_physical",
                                           voxel_logical,
                                           process_space_logical,
                                           g4.G4global.EAxis.kXAxis,
                                           n_voxel,
                                           wafer,
                                           False)
        wafer_physical.SetRegularStructureId(1)

        return self.world_physical
