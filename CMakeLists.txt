cmake_minimum_required(VERSION 3.24)
project(advent_of_code)

set(CMAKE_CXX_STANDARD 20)

add_executable(22D1 src/year2022/c++/day1.cpp)
add_executable(22D2 src/year2022/c++/day2.cpp src/year2022/c++/infra.h src/year2022/c++/infra.cpp)
