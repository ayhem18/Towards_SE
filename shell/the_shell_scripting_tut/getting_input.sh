#! bin/bash

# getting input from the user

user_input="some_valllue"

# while [ $user_input != "bye" ] 
# the line above does not work as expected and here is why:
# so the $ operator works exactly like macros in C. it replaces the variable with whatever value is stored in the variable.
# now if the variable is a string with spaces e.g (word1 word2)
# the expression $user_input != "bye" will be evaluate as word1 word2 != "bye" 
# which would most likely raise an error. (since word1 might not represent a command in bash)

# so the solution is to wrap them around ""

while [ "$user_input" != "bye" ]

do  
    echo "I will keep listening to you until you say bye"
    
    read user_input
    
    echo "you said ${user_input}!"
done

echo "sad to see you go! bye!"






