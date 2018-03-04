#include <boost/python.hpp>
#include "G4PhantomParameterisation.hh"
#include "G4VPhysicalVolume.hh"
#include "G4VSolid.hh"
#include "G4VTouchable.hh"
#include "G4Material.hh"

using namespace boost::python;

// ====================
//   Expose to Python
// ====================

namespace pyG4PhantomParameterisation {

  void(G4PhantomParameterisation::*f1_BuildContainerSolid)(G4VPhysicalVolume*)
      = &G4PhantomParameterisation::BuildContainerSolid;
  void(G4PhantomParameterisation::*f2_BuildContainerSolid)(G4VSolid*)
      = &G4PhantomParameterisation::BuildContainerSolid;
  void(G4PhantomParameterisation::*f1_SetMaterials)(boost::python::list&)
      = &G4PhantomParameterisation::SetMaterials;
  void(G4PhantomParameterisation::*f1_SetMaterialIndices)(boost::python::list&)
      = &G4PhantomParameterisation::SetMaterialIndices;
}


// static void set_materials(G4PhantomParameterisation &h, boost::python::list &x){h.set_materials(x);}


using namespace  pyG4PhantomParameterisation;

void export_G4PhantomParameterisation()
{
  class_<G4PhantomParameterisation, G4PhantomParameterisation*,
    bases<G4VPVParameterisation>, boost::noncopyable>
    ("G4PhantomParameterisation", "original phantom parameterisation", no_init)
    .def(init<>())
    .def("SetVoxelDimensions", &G4PhantomParameterisation::SetVoxelDimensions)
    .def("SetNoVoxel", &G4PhantomParameterisation::SetNoVoxel)
    .def("SetMaterials", f1_SetMaterials)
    .def("SetMaterialIndices", f1_SetMaterialIndices)
    // .def("SetMaterials", &G4PhantomParameterisation::SetMaterials)
    // .def("SetMaterialIndices", &G4PhantomParameterisation::SetMaterialIndices)
    .def("BuildContainerSolid", f1_BuildContainerSolid)
    .def("BuildContainerSolid", f2_BuildContainerSolid)
    .def("CheckVoxelsFillContainer", &G4PhantomParameterisation::CheckVoxelsFillContainer)
    .def("SetSkipEqualMaterials", &G4PhantomParameterisation::SetSkipEqualMaterials)
    .def("ComputeMaterial", &G4PhantomParameterisation::ComputeMaterial,
         return_internal_reference<>())
    ;
}
