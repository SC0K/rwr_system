# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_logger_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED logger_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(logger_FOUND FALSE)
  elseif(NOT logger_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(logger_FOUND FALSE)
  endif()
  return()
endif()
set(_logger_CONFIG_INCLUDED TRUE)

# output package information
if(NOT logger_FIND_QUIETLY)
  message(STATUS "Found logger: 0.1.0 (${logger_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'logger' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${logger_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(logger_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${logger_DIR}/${_extra}")
endforeach()
