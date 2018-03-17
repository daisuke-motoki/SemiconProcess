from Geant4 import G4VSensitiveDetector
from Geant4 import eV, nanometer
import numpy as np
import settings


class VoxelDensityChanger(G4VSensitiveDetector):
    """
    """
    def __init__(self,
                 df_reactive_particle_table,
                 material_manager):
        """
        """
        super(VoxelDensityChanger, self).__init__("VoxelDensity")
        self.df_reactive_particle_table = df_reactive_particle_table
        self.material_manager = material_manager
        self.energy_threshold = 10.0 * eV
        self.nm3 = 1/nanometer**3

    @staticmethod
    def _select_process_of_particle(particle, df_process_table):
        """
        """
        particle_name = str(particle.GetParticleName())
        reactive_material_table = df_process_table[
            df_process_table["particle_name"] == particle_name
        ]

        return reactive_material_table, particle_name

    def _select_process_of_material(self, material, df_process_table):
        """
        """
        mat_names, fracs = \
            self.material_manager.get_original_material_names(
                str(material.GetName())
            )
        cum_sum = np.cumsum(fracs/np.sum(fracs))
        # get first index of True
        ind = (cum_sum > np.random.rand()).argmax()
        target_mat_name = mat_names[ind]
        reactive_process_table = df_process_table[
            df_process_table["material_name"] == target_mat_name
        ]

        return reactive_process_table, target_mat_name

    @staticmethod
    def _select_process_of_initiation(df_process_table, process):
        """
        """
        process_name = str(process.GetProcessName())
        reactive_process_table = df_process_table[
            df_process_table["initiation_process_name"] == process_name
        ]

        return reactive_process_table, process_name

    @staticmethod
    def _select_process_of_min_energy(energy, df_process_table):
        """
        """
        reactive_process_table = df_process_table[
            df_process_table["min_energy[keV]"] <= energy
        ]
        return reactive_process_table, energy

    @staticmethod
    def _select_process(df_process_table):
        """
        """
        cum_sum = df_process_table["probability"].cumsum() / df_process_table["probability"].sum()
        ind = (cum_sum > np.random.rand()).idxmax()

        return df_process_table.ix[ind]

    def ProcessHits(self, step, rohist):
        """
        """
        # check dedx
        dedx = step.GetTotalEnergyDeposit()
        if dedx < self.energy_threshold:
            return

        # check particle
        track = step.GetTrack()
        particle = track.GetDynamicParticle().GetDefinition()
        df_process_table, particle_name = self._select_process_of_particle(
            particle, self.df_reactive_particle_table)
        if len(df_process_table) == 0:
            return

        # determine material interacted
        touchable = track.GetTouchable()
        logical = touchable.GetVolume().GetLogicalVolume()
        material = logical.GetMaterial()
        df_process_table, material_name = self._select_process_of_material(
            material, df_process_table)
        if len(df_process_table) == 0:
            return

        # check process
        post_step = step.GetPostStepPoint()
        post_process = post_step.GetProcessDefinedStep()
        df_process_table, process_name = self._select_process_of_initiation(
            df_process_table, post_process)
        if len(df_process_table) == 0:
            return

        # check minimum energy
        df_process_table, _ = self._select_process_of_min_energy(
            dedx, df_process_table)
        if len(df_process_table) == 0:
            return

        # dicide which process will be applied
        df_process_table = self._select_process(df_process_table)
        if len(df_process_table) == 0:
            return

        # apply process
        process_type = df_process_table["process_type"]
        if process_type == "etching":
            mat_names, fracs = \
                self.material_manager.get_original_material_names(
                    str(material.GetName())
                )
            volume = logical.GetSolid().GetCubicVolume()
            reduce_frac = df_process_table["etching_rate[1/nm3]"] / (volume * self.nm3)
            reduce_frac *= settings.ETCHING_ACCELERATION_FACTOR
            target_frac_ind = mat_names.index(material_name)
            fracs[target_frac_ind] -= reduce_frac
            replace_material_name = df_process_table["replace_material_name"]
            if replace_material_name in mat_names:
                ind = mat_names.index(replace_material_name)
                fracs[ind] += reduce_frac
            else:
                mat_names.append(replace_material_name)
                fracs.append(reduce_frac)

            new_material, is_created = \
                self.material_manager.get_or_create_mixed_material(mat_names,
                                                                   fracs)
            logical.SetMaterial(new_material)
            voxel_id = touchable.GetReplicaNumber()
            post_pos = post_step.GetPosition()
            print("{}: {}: etching to {}".format(voxel_id, post_pos, new_material.GetName()))
        elif process_type == "deposition":
            pass
        else:
            raise TypeError("Unknown process type : {}".format(process_type))
