# - build test library

include_directories(
  ${PYTHON_INCLUDE_PATH}
  ${Boost_INCLUDE_DIRS}
  ${GEANT4_INCLUDE_DIR}
)

link_directories (${GEANT4_LIBRARY_DIR} ${Boost_LIBRARY_DIRS})

# library
set(_TARGET pyG4parameterised)
add_library(
  ${_TARGET} SHARED
  G4PhantomParameterisation.cc
  PhantomParameterisationColour.cc
  pyG4VPVParameterisation.cc
  pyG4PVParameterised.cc
  pyG4PhantomParameterisation.cc
  pyPhantomParameterisationColour.cc
  pymodG4parameterised.cc
)

set_target_properties(${_TARGET} PROPERTIES PREFIX "")
set_target_properties(${_TARGET} PROPERTIES OUTPUT_NAME "g4parameterised")
set_target_properties(${_TARGET} PROPERTIES SUFFIX ".so")

target_link_libraries (${_TARGET}
                       ${GEANT4_LIBRARIES_WITH_VIS} boost_python
                       ${PYTHON_LIBRARIES})

# install
install(TARGETS ${_TARGET} LIBRARY DESTINATION ${SEMICONPROCESS_MODULES_INSTALL_DIR})
