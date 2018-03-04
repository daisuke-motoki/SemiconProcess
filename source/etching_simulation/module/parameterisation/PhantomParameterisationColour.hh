#ifndef PhantomParameterisationColour_HH
#define PhantomParameterisationColour_HH

#include <map>

#include "G4PhantomParameterisation.hh"
#include "G4VisAttributes.hh"


class PhantomParameterisationColour : public G4PhantomParameterisation
{
public:  // with description
  
  PhantomParameterisationColour();
  ~PhantomParameterisationColour();
  
  virtual G4Material* ComputeMaterial(const G4int repNo, 
                                      G4VPhysicalVolume *currentVol,
                                      const G4VTouchable *parentTouch=0);
  
  inline void AddColor(G4String name, G4VisAttributes* visAtt){
        fColours[name] = visAtt;
        std::cout<<name<<visAtt->GetColor()<<std::endl;
  }

private:
  std::map<G4String,G4VisAttributes*> fColours;
};


#endif
