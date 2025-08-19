#!/bin/sh
# echo "MYVAR is: $MYVAR" # since the variable is not set, output will be: "MYVAR is: " (empty string)
# MYVAR="hi there"
# echo "MYVAR is: $MYVAR"

# export file_name1="file1.txt"
# export file_name2="file2.txt"

# touch $file_name1 $file_name2


echo "running once"

while [ "1.2" != 1.2 ] # so basically 1.2 is indeed the same as "1.2" everything is a string in bash.
do 
    echo "will keep running forever"
done

echo "this is never going to be printed"