import argparse
import pandas as pd
import Geant4 as g4

from src.material_utils import MaterialManager
from src.DeviceConstruction import DeviceConstruction
from src.VoxelDensityChanger import VoxelDensityChanger
from src.SteppingAction import SteppingAction
from g4semiconprocess import PrimaryGeneratorAction
from g4semiconprocess import PhysicsList
import settings


def main(init_filename, mac_filename=None):
    # choose the random engine
    # G4Random::setTheEngine(new CLHEP::RanecuEngine);

    # set mandatory initialization classes
    material_manager = MaterialManager()
    simulationVolume = DeviceConstruction(init_filename, material_manager)
    df_reactive_particle_table = pd.read_csv(settings.REACTIVE_PARTICLE_PROCESS_TABLE_PATH)
    sd = VoxelDensityChanger(df_reactive_particle_table, material_manager)
    simulationVolume.set_density_changer(sd)
    g4.gRunManager.SetUserInitialization(simulationVolume)
    physics_list = PhysicsList()
    g4.gRunManager.SetUserInitialization(physics_list)

    # # set user action classes
    generator = PrimaryGeneratorAction()
    g4.gRunManager.SetUserAction(generator)

    # runAction = new RunAction;
    # runManager->SetUserAction(runAction);
    # eventAction = new EventAction;
    # runManager->SetUserAction(eventAction);
    # trakingAction = new TrackingAction;
    # runManager->SetUserAction(trackingAction);
    # stepping_action = SteppingAction()
    # g4.gRunManager.SetUserAction(stepping_action)

    # # visualization manager
    # visManager = new G4VisManager.GetConcreateInstance()
    # visManager.Initialize()

    if mac_filename is not None:
        g4.gControlExecute(mac_filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='run simulation')
    parser.add_argument('-i' '--init_phantom', required=True)
    parser.add_argument('-m', '--macro')
    parser.add_argument('--version', action='version', version='0.0')
    args = parser.parse_args()
    init_filename = args.i__init_phantom
    mac_filename = args.macro
    main(init_filename=init_filename, mac_filename=mac_filename)
