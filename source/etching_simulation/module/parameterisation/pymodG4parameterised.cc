#include <boost/python.hpp>

using namespace boost::python;

// ====================
//   module definition
// ====================
void export_G4VPVParameterisation();
void export_G4PVParameterised();
void export_G4PhantomParameterisation();
void export_PhantomParameterisationColour();


BOOST_PYTHON_MODULE(g4parameterised) {
    export_G4VPVParameterisation();
    export_G4PVParameterised();
    export_G4PhantomParameterisation();
    export_PhantomParameterisationColour();
}
