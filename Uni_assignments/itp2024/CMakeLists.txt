cmake_minimum_required(VERSION 3.27)
project(itp2024)

set(CMAKE_CXX_STANDARD 14)

include_directories(labs)

add_executable(itp2024
        labs/objects.cpp
        labs/objects.h
        main.cpp)
