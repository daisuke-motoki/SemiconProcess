# - add lib components

set(SEMICONPROCESS_MODULES_INSTALL_DIR ${CMAKE_INSTALL_LIBDIR})

# lib for g4py
add_subdirectory(module/parameterisation)
add_subdirectory(module/semiconprocess)
