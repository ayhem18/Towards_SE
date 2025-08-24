#!/bin/bash

# let's play around with more variables

# so basically there are a few special variables in bash 

# $#: number of arguments passed to the script
# $*: all the arguments passed to the script
# $i: the i-th argument passed to the script

# # can we iterate through the arguments ? 
# for arg in $@
# do 
#     echo "arg: $arg"
# done


# # is there a way to iterate while displaying the index ?
# btw the variable "1", "2" are the actual variables !!!


# num_args=$# 
# for i in $(seq 1 $num_args)
# do
#     echo "arg $i: ${!i}"
# done


# we can set default values for variables

:- `whoami`
