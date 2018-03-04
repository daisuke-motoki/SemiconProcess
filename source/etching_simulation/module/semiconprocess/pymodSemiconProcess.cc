#include <boost/python.hpp>
#include "PrimaryGeneratorAction.hh"
#include "PhysicsList.hh"
#include "G4ParticleGun.hh"

using namespace boost::python;

// ======================
//   Expose to Python
// ======================

BOOST_PYTHON_MODULE(g4semiconprocess) {
  class_<PrimaryGeneratorAction, PrimaryGeneratorAction*,
    bases<G4VUserPrimaryGeneratorAction> >
    ("PrimaryGeneratorAction", "semicon process primary generator action")
    // .def("GetParticleGun", &PrimaryGeneratorAction::GetParticleGun,
    //      return_internal_reference<>())
    .def("GeneratePrimaries", &PrimaryGeneratorAction::GeneratePrimaries)
    ;

  class_<PhysicsList, PhysicsList*,
    bases<G4VUserPhysicsList> >
    ("PhysicsList", "semicon process physics list")
    ;
}

