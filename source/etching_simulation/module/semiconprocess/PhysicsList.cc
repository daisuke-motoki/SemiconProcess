#include "PhysicsList.hh"

#include "G4EmStandardPhysics.hh"
#include "G4EmStandardPhysics_option4.hh"
#include "G4EmStandardPhysicsSS.hh"
#include "G4EmStandardPhysicsWVI.hh"
#include "G4EmParameters.hh"

#include "G4IonPhysics.hh"
#include "G4IonPhysicsPHP.hh"
#include "G4IonQMDPhysics.hh"
#include "G4IonINCLXXPhysics.hh"
#include "G4IonBinaryCascadePhysics.hh"

#include "G4SystemOfUnits.hh"

//////////////////////////////////////////////////////
PhysicsList::PhysicsList() : G4VModularPhysicsList(),
  fEmPhysicsList(0), fIonPhysicsList(0)
//////////////////////////////////////////////////////
{


  // EM physics
  fEmName = G4String("emstandard_opt4");
  // fEmPhysicsList = new G4EmStandardPhysics_option4();
  // fEmPhysicsList = new G4EmStandardPhysicsSS();
  fEmPhysicsList = new G4EmStandardPhysicsWVI();

  // Ion physics
  fIonPhysicsList = new G4IonPhysics();

  //extend energy range of PhysicsTables
  G4EmParameters* param = G4EmParameters::Instance();
  param->SetMinEnergy(10*eV);  
  param->SetMaxEnergy(1000*GeV);
  param->SetLowestElectronEnergy(10*eV);
  param->SetLowestMuHadEnergy(10*eV);

}

////////////////////////////
PhysicsList::~PhysicsList()
////////////////////////////
{
}

//////////////////////////////////////
void PhysicsList::ConstructParticle()
//////////////////////////////////////
{
  fEmPhysicsList->ConstructParticle();
  fIonPhysicsList->ConstructParticle();
}

/////////////////////////////////////
void PhysicsList::ConstructProcess()
/////////////////////////////////////
{
  // transportation
  //
  AddTransportation();
  
  // electromagnetic Physics List
  //
  fEmPhysicsList->ConstructProcess();
  fIonPhysicsList->ConstructProcess();
}
