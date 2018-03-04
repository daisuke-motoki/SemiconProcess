#include <boost/python.hpp>
#include "G4VPVParameterisation.hh"

using namespace boost::python;

// ====================
//   Expose to Python
// ====================

void export_G4VPVParameterisation()
{
  class_<G4VPVParameterisation, G4VPVParameterisation, boost::noncopyable>
    ("G4VPVParameterisation", "original g4 parameterisation", no_init)
    ;
}
