#!/bin/sh
# echo "MYVAR is: $MYVAR" # since the variable is not set, output will be: "MYVAR is: " (empty string)
# MYVAR="hi there"
# echo "MYVAR is: $MYVAR"

# export file_name1="file1.txt"
# export file_name2="file2.txt"

# touch $file_name1 $file_name2


#################### CHECKING FLOAT AND STRING VARIABELS EQUALITY  ####################

# echo "running once"

# while [ "1.2" != 1.2 ] # so basically 1.2 is indeed the same as "1.2" everything is a string in bash.
# do 
#     echo "will keep running forever"
# done

# echo "this is never going to be printed"



#################### playin around with equality operators and loops  ####################


# it seems that there is a bit more to this than I thought
# there are a few comparison operators in bash 
# -eq for equality
# -ne for inequality
# -gt for greater than
# -lt for less than
# -ge for greater than or equal to
# -le for less than or equal to


# X = -1
# echo "enter a number"
# read X

# # the [ expression ] is a bash command to evaluate the expression

# while [ $X -lt 0 ] 
# # the real question is: what if the user enters a non-number ?
# # an error occurs and the script moves to the next code block
# do 
#     echo "You have entered the number ${X}"
#     printf "\n"
#     echo "enter a number"
#     read X
# done

# # regardless of the user's input, this line will be executed
# echo "You have finally entered a number greater than 0"



#################### playing around with case statements  ####################



some_var=""
echo "enter a string"
read some_var

# save the length of a string in a variable
var_length=${#some_var} 

case $var_length in 
    0) 
        echo "You entered nothing"
        ;;
    1) 
        echo "You entered a single character"
        ;;
    2) 
        echo "You entered 2 characters"
        ;;
    3) 
        echo "You entered 3 characters"
        ;;
    *)
        echo "You entered more than 3 characters"
        ;;
esac


