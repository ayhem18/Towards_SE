cmake_minimum_required(VERSION 3.27)
project(LearnC__)

set(CMAKE_CXX_STANDARD 17)

add_executable(LearnC__ main.cpp
        containers.cpp
        strings.cpp
        input.cpp
        arrays.cpp
        compound_types.cpp
        DataStructures/linked_list.cpp
        header.h
        DataStructures/Stack.cpp
        DataStructures/linked_list.h)

