# this script greets the user by name (based on the time of day)

# 1. create a function to return the greeting depending on the time of day
# 2. create a variable to store the current time
# 3. create a variable to store the user's name
# 4. call the function with the current time and the user's name
# 5. print the greeting


get_greeting()
{

    # get the current time
    current_time=$(date +%T)

    # extract only the hour from the current time
    hour=${current_time:0:2}



    # the morning is between 6 and 12 (both inclusive)

    # the afternoon is between 12 and 18 (both inclusive)

    # the evening is between 18 and 21 (both inclusive)

    # the night is between 21 and 06 (both inclusive)

    greeting=""

    # let's start with the night: 
    if [ $hour -ge 21 ] || [ $hour -lt 6 ]; then
        greeting="Good night"
    # then the morning:
    elif [ $hour -ge 6 ] && [ $hour -lt 12 ]; then
        greeting="Good morning"
    # then the afternoon:
    elif [ $hour -ge 12 ] && [ $hour -lt 18 ]; then
        greeting="Good afternoon"
    # then the evening:
    else
        greeting="Good evening"
    fi

    # one way to get the greeting is to echo it
    # the "return" statement does not work the same way in other programming languages
    echo $greeting

    # the return statement indicates whether the call was successful or not
    return 0
}


# 1. read the user's name
echo "Enter your name: "
read user_name

# 2. call the function to get the greeting
greeting=$(get_greeting)

# 3. print the greeting
echo "$greeting, $user_name!"