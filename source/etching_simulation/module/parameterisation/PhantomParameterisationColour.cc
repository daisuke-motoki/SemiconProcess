#include "PhantomParameterisationColour.hh"

#include "globals.hh"
#include "G4VisAttributes.hh"
#include "G4Material.hh"
#include "G4VPhysicalVolume.hh"
#include "G4LogicalVolume.hh"

///////////////////////////////////////////////////////////////
PhantomParameterisationColour::PhantomParameterisationColour()
: G4PhantomParameterisation()
///////////////////////////////////////////////////////////////
{
    SetSkipEqualMaterials(true);

    //----- Add a G4VisAttributes for materials not defined in file;
    G4VisAttributes* blankAtt = new G4VisAttributes;
    blankAtt->SetVisibility( FALSE );
    fColours["Default"] = blankAtt;
}

////////////////////////////////////////////////////////////////
PhantomParameterisationColour::~PhantomParameterisationColour()
////////////////////////////////////////////////////////////////
{
}

//////////////////////////////////////////////////////////////////////////////////////
G4Material* PhantomParameterisationColour::
ComputeMaterial(const G4int copyNo, G4VPhysicalVolume * physVol, const G4VTouchable *)
//////////////////////////////////////////////////////////////////////////////////////
{
    G4Material* mate = G4PhantomParameterisation::ComputeMaterial( copyNo, physVol, 0 );
    if( physVol ) {
        G4String mateName = mate->GetName();
        std::string::size_type iuu = mateName.find("__");
        if( iuu != std::string::npos ) {
            mateName = mateName.substr( 0, iuu );
        }
        std::map<G4String,G4VisAttributes*>::const_iterator ite =
          fColours.find(mateName);

        if( ite != fColours.end() ){
            physVol->GetLogicalVolume()->SetVisAttributes( (*ite).second );
        } else {
            physVol->GetLogicalVolume()->SetVisAttributes( 
                                  (*(fColours.begin()) ).second );
            // set it as unseen
        }
    }
    
    return mate;
}
