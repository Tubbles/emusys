cmake_minimum_required(VERSION 3.15)
project(emusys VERSION 0.0.1 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)

# Run conan install automatically, or display error if conan is not installed
find_program(conanexecutable "conan")
if(NOT conanexecutable)
    message(FATAL_ERROR "Conan required, install with `pip install conan`")
else()
    message(STATUS "Found conan. Installing dependencies.")
    if(NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
        message(STATUS "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
        file(DOWNLOAD "https://raw.githubusercontent.com/conan-io/cmake-conan/master/conan.cmake"
                      "${CMAKE_BINARY_DIR}/conan.cmake")
    endif()
    include(${CMAKE_BINARY_DIR}/conan.cmake)
    conan_cmake_run(CONANFILE conanfile.txt
                    BASIC_SETUP
                    BUILD missing
                    CONFIGURATION_TYPES "Release")
    set(CMAKE_MODULE_PATH "${CMAKE_BINARY_DIR}" ${CMAKE_MODULE_PATH})
endif()

# Add sources
add_subdirectory(src)

# Add dependencies
# find_package(fmt)

target_link_libraries(emusys fmt)
target_link_libraries(emusys imgui)
