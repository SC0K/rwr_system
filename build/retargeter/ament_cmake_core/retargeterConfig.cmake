# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_retargeter_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED retargeter_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(retargeter_FOUND FALSE)
  elseif(NOT retargeter_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(retargeter_FOUND FALSE)
  endif()
  return()
endif()
set(_retargeter_CONFIG_INCLUDED TRUE)

# output package information
if(NOT retargeter_FIND_QUIETLY)
  message(STATUS "Found retargeter: 0.1.0 (${retargeter_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'retargeter' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${retargeter_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(retargeter_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${retargeter_DIR}/${_extra}")
endforeach()
