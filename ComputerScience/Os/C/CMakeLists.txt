# as the name suggests, this is the minimum version
cmake_minimum_required(VERSION 3.31.)

project(PlaygroundC 
        VERSION 0.1.0 
        DESCRIPTION "A simple playground in C"
        LANGUAGES CXX C)

set(CMAKE_C_STANDARD 17)

# put the data structures code in a library

add_library(dataStructures
        playground/dataStructures/linear/linked_list.c
)

# the library depends on the headers defined in the playground/headers/dataStructures directory 
target_include_directories(dataStructures PRIVATE playground/headers/dataStructures)

add_executable(main playground/main.c)

# add the library to the executable
target_include_directories(main PRIVATE playground/headers/dataStructures)

# add to the linker
target_link_libraries(main dataStructures)


