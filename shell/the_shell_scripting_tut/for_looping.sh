#! bin/bash

# for loop example 

# # iterating through a list of values  
# for i in 1 2 3 4 5
# do
# echo "the variable i has the value ${i}"
# done


# # iterating through all the files in the current directory ??? 
# for file_name in *
# do
#     echo "the file name is ${file_name}"
# done

# directory_path/* returns the paths to all files in the directory
# ls directory_path returns the file names in the directory

# I am still confused about the nature of the return values of commands in bash...

for file_name in $(ls ${PWD})
do 
echo "the file name is ${file_name}" 
echo "the file path is ${PWD}/${file_name}"
printf "\n"
done






