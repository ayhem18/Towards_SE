 cmake_minimum_required(VERSION 3.27)
project(Cpp)

set(CMAKE_CXX_STANDARD 20)

add_executable(Cpp main.cpp
        arrays/searching.h
        arrays/searching.cpp
        arrays/prefixSum.h
        arrays/prefixSum.cpp
        utils.cpp
        utils.h
        twoPointers/file1.cpp
        twoPointers/file1.h)
