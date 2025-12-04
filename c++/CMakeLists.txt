cmake_minimum_required(VERSION 3.15)
project(advent_of_code)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Build the infra library.
file(GLOB_RECURSE INFRA_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/infra/*.cpp")
if (INFRA_SOURCES)
    add_library(infra STATIC ${INFRA_SOURCES})
    target_include_directories(infra PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/src/infra")
endif ()

# Automatically discover year directories and create targets.
file(GLOB YEAR_DIRS RELATIVE ${CMAKE_CURRENT_SOURCE_DIR}/src "${CMAKE_CURRENT_SOURCE_DIR}/src/year[0-9][0-9][0-9][0-9]")
foreach (year_dir ${YEAR_DIRS})
    string(SUBSTRING ${year_dir} 6 2 year_suffix)
    file(GLOB YEAR_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/${year_dir}/*.cpp")

    foreach (src ${YEAR_SOURCES})
        get_filename_component(src_name ${src} NAME_WE)
        string(REGEX REPLACE "day([0-9]+)" "\\1" day_number ${src_name})
        set(target_name "${year_suffix}D${day_number}")

        add_executable(${target_name} ${src})
        target_link_libraries(${target_name} PRIVATE infra)
    endforeach ()
endforeach ()
