#include "PrimaryGeneratorAction.hh"
#include "G4SystemOfUnits.hh"

/////////////////////////////////////////////////
PrimaryGeneratorAction::PrimaryGeneratorAction()
/////////////////////////////////////////////////
{
  // fParticleGun  = new G4ParticleGun();
  //
  // // default gun parameters
  // fParticleGun->SetParticleEnergy(10.*keV);
  // fParticleGun->SetParticleMomentumDirection(G4ThreeVector(0.,0.,-1.));
  // fParticleGun->SetParticlePosition(G4ThreeVector(0.,0.,0.4*um));
  fParticleGun = new G4GeneralParticleSource();
}

//////////////////////////////////////////////////
PrimaryGeneratorAction::~PrimaryGeneratorAction()
//////////////////////////////////////////////////
{
  delete fParticleGun;
}

/////////////////////////////////////////////////////////////////
void PrimaryGeneratorAction::GeneratePrimaries(G4Event* anEvent)
/////////////////////////////////////////////////////////////////
{
  fParticleGun->GeneratePrimaryVertex(anEvent);
}
