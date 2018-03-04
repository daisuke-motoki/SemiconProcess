#ifndef PhysicsList_h
#define PhysicsList_h 1

#include "G4VModularPhysicsList.hh"
#include "globals.hh"

class PhysicsListMessenger;
class G4VPhysicsConstructor;

////////////////////////////////////////////////
class PhysicsList: public G4VModularPhysicsList
////////////////////////////////////////////////
{
  public:
    PhysicsList();
   ~PhysicsList();

    virtual void ConstructParticle();
    virtual void ConstructProcess();

  private:
    
    G4VPhysicsConstructor* fEmPhysicsList;
    G4VPhysicsConstructor* fIonPhysicsList;
    G4String               fEmName;
};

#endif
