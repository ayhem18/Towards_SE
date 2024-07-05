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
        twoPointers/file1.h
        trees/file1.h
        trees/file1.cpp
        trees/file2.cpp
        trees/common.cpp
        dp/dp1.cpp
        dp/dp1.h
        backtracking/bt1.cpp
        backtracking/bt1.h
        arrays/must_do.cpp
        arrays/must_do.h
        greedy/g1.cpp
        greedy/g1.h)
