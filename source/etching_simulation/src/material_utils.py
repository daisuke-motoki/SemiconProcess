from collections import OrderedDict
import Geant4 as g4


class MaterialManager(object):
    """
    """
    def __init__(self):
        """
        """
        self.base_materials = OrderedDict()
        self.mixed_materials = OrderedDict()

    def get_or_create_mixed_material(self, mat_names, fractions):
        """
        """
        mixed_name = self.get_mixtured_material_name(mat_names, fractions)

        is_created = False
        material = self.mixed_materials.get(mixed_name, None)
        if material is None:
            base_materials = [self.get_base_material(name)
                              for name in mat_names]
            material = self.build_mixtured_material(mixed_name,
                                                    base_materials,
                                                    fractions)
            self.add_mixed_material(mixed_name, material)
            is_created = True

        return material, is_created

    def get_base_material(self, name):
        """
        """
        material = self.base_materials.get(name, None)
        if material is None:
            raise ValueError("{} does not exist.".format(name))
        return material

    def add_base_material(self, name, material):
        """
        """
        if name in self.base_materials:
            raise ValueError("{} have already existed.".foramt(name))

        self.base_materials[name] = material

        return True

    def get_mixed_material(self, name):
        """
        """
        material = self.mixed_materials.get(name, None)
        if material is None:
            raise ValueError("{} does not exist.".format(name))
        return material

    def get_all_mixed_materials(self):
        """
        """
        return self.mixed_materials.values()

    def add_mixed_material(self, name, material):
        """
        """
        if name in self.mixed_materials:
            raise ValueError("{} have already existed.".foramt(name))

        self.mixed_materials[name] = material

        return True

    @staticmethod
    def get_original_material_names(name):
        """
        """
        name_fracs = name.split("__")
        names = [name_frac.split(":")[0] for name_frac in name_fracs]
        fracs = [float(name_frac.split(":")[1]) for name_frac in name_fracs]
        return names, fracs

    @staticmethod
    def get_mixtured_material_name(mat_names, fractions):
        """
        """
        names = ["{}:{}".format(name, fraction)
                 for name, fraction in zip(mat_names, fractions)
                 if fraction > 0.0]
        return "__".join(names)

    @staticmethod
    def build_mixtured_material(name, base_materials, fractions):
        """
        """
        density = 0.
        for base_mat, fraction in zip(base_materials, fractions):
            density += base_mat.GetDensity() * fraction
        ncomponents = len(base_materials)
        new_material = g4.G4Material(name, density, ncomponents)
        for base_mat, fraction in zip(base_materials, fractions):
            new_material.AddMaterial(base_mat, fraction)

        return new_material
