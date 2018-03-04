#ifndef PrimaryGeneratorAction_h
#define PrimaryGeneratorAction_h 1

#include "G4VUserPrimaryGeneratorAction.hh"
//#include "G4ParticleGun.hh"
#include "G4GeneralParticleSource.hh"


class PrimaryGeneratorAction : public G4VUserPrimaryGeneratorAction
{
public:

  PrimaryGeneratorAction();    
  ~PrimaryGeneratorAction();
  
  void GeneratePrimaries(G4Event*);
  // G4ParticleGun* GetParticleGun() const;

private:

  // G4ParticleGun*           fParticleGun;
  G4GeneralParticleSource* fParticleGun;
};

// inline G4ParticleGun* PrimaryGeneratorAction::GetParticleGun() const
// { return fParticleGun; }
#endif
