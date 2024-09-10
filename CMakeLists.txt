cmake_minimum_required(VERSION 3.15)
project(emusys VERSION 0.0.1 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)

option(BACKEND_SDL2 "Use SDL2/OpenGL for backend" ON)
option(BACKEND_GLFW "Use GLFW/OpenGL for backend" OFF)

set(CONAN_COMMIT_HASH 43e385830ee35377dbd2dcbe8d5a9e750301ea00)

# Run conan install automatically, or display error if conan is not installed
find_program(conanexecutable "conan")
if(NOT conanexecutable)
    message(FATAL_ERROR "Conan required, install with `pip install conan`")
else()
    message(STATUS "Found conan. Installing dependencies.")
    if(NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
        message(STATUS "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
        file(DOWNLOAD "https://raw.githubusercontent.com/conan-io/cmake-conan/${CONAN_COMMIT_HASH}/conan.cmake"
                      "${CMAKE_BINARY_DIR}/conan.cmake")
    endif()
    include(${CMAKE_BINARY_DIR}/conan.cmake)
    conan_cmake_run(CONANFILE conanfile.yml
                    BASIC_SETUP
                    BUILD missing
                    CONFIGURATION_TYPES "Release")
    set(CMAKE_MODULE_PATH "${CMAKE_BINARY_DIR}" ${CMAKE_MODULE_PATH})
endif()

# -- Add sources --
set(SRC_FILES "")
set(LIBRARIES "")
set(INCL_DIRS "${CMAKE_BINARY_DIR}/import")
# file(GLOB_RECURSE SRC_FILES src/*.cc ${CMAKE_BINARY_DIR}/import/*.cpp)

# Also add any imported includes

# -- Add dependencies --
# fmt
find_package(fmt REQUIRED)

# SDL2
if(BACKEND_SDL2)
    set(SDL_WAYLAND "OFF")
    find_package(SDL2 REQUIRED)
    list(APPEND INCL_DIRS
        ${SDL2_INCLUDE_DIRS})
    list(APPEND LIBRARIES
        ${SDL2_LIBRARIES})
endif()

# GLFW
if(BACKEND_GLFW)
    find_package(GLFW REQUIRED)
    find_package(OpenGL REQUIRED)
    list(APPEND INCL_DIRS
        ${OPENGL_INCLUDE_DIRS})
    list(APPEND LIBRARIES
        ${OPENGL_LIBRARIES})
endif()

# ImGUI
# find_package(imgui REQUIRED)
list(APPEND LIBRARIES
    "imgui")
if(BACKEND_SDL2)
    list(APPEND SRC_FILES
        "import/imgui_bindings/imgui_impl_sdl.cpp"
        "import/imgui_bindings/imgui_impl_sdlrenderer.cpp")
elseif(BACKEND_GLFW)
    list(APPEND SRC_FILES
        "import/imgui_bindings/imgui_impl_glfw.cpp"
        "import/imgui_bindings/imgui_impl_opengl3.cpp")
else()
    message(FATAL_ERROR "No backend selected")
endif()

# Our stuffs
add_subdirectory(src)

# Finally
add_executable(emusys ${SRC_FILES})

target_include_directories(emusys PRIVATE ${CMAKE_BINARY_DIR}/import ${INCL_DIRS})

target_link_libraries(emusys ${LIBRARIES})
