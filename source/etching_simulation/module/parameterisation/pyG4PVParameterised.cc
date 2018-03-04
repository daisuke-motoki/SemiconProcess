#include <boost/python.hpp>
#include "G4PVParameterised.hh"
#include "G4VPVParameterisation.hh"
#include "G4PhantomParameterisation.hh"
#include "G4VPhysicalVolume.hh"
#include "G4LogicalVolume.hh"

using namespace boost::python;

// ====================
//   Expose to Python
// ====================

void export_G4PVParameterised()
{
  class_<G4PVParameterised, G4PVParameterised*, bases<G4PVReplica>, boost::noncopyable>
    ("G4PVParameterised", "original g4 parameterised", no_init)
    .def(init<const G4String&, G4LogicalVolume*, G4LogicalVolume*, const EAxis,
              const G4int, G4VPVParameterisation*, G4bool>())
    .def(init<const G4String&, G4LogicalVolume*, G4VPhysicalVolume*,
              const EAxis, const G4int, G4VPVParameterisation*, G4bool>())
    .def("SetRegularStructureId", &G4PVParameterised::SetRegularStructureId)
    ;
}
