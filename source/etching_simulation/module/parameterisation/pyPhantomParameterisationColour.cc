#include <boost/python.hpp>
#include "G4PhantomParameterisation.hh"
#include "PhantomParameterisationColour.hh"
#include "G4VPhysicalVolume.hh"
#include "G4VTouchable.hh"
#include "G4VisAttributes.hh"

using namespace boost::python;

// ====================
//   Expose to Python
// ====================

void export_PhantomParameterisationColour()
{
  class_<PhantomParameterisationColour, PhantomParameterisationColour*,
    bases<G4PhantomParameterisation>, boost::noncopyable>
    ("PhantomParameterisationColour", "phantom parameterisation with different color", no_init)
    .def(init<>())
    .def("AddColor", &PhantomParameterisationColour::AddColor)
    .def("ComputeMaterial", &PhantomParameterisationColour::ComputeMaterial,
         return_internal_reference<>())
    ;
}
