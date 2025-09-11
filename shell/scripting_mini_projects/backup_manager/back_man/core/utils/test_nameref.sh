#!/bin/bash

# Simple demonstration of nameref behavior
demo_function() {
    local input="$1"
    local -n result1_ref="$2"  # nameref pointing to whatever variable name is passed as $2
    local -n result2_ref="$3"  # nameref pointing to whatever variable name is passed as $3
    
    echo "Inside function: Setting values..."
    result1_ref="Hello"        # This sets the variable that result1_ref points to
    result2_ref="World"        # This sets the variable that result2_ref points to
    
    echo "Inside function: result1_ref=$result1_ref, result2_ref=$result2_ref"
    return 0
}

# Usage example
echo "=== Testing nameref behavior ==="
my_var1=""
my_var2=""

echo "Before function call: my_var1='$my_var1', my_var2='$my_var2'"

# Call the function, passing variable NAMES (not values)
demo_function "test_input" my_var1 my_var2

echo "After function call: my_var1='$my_var1', my_var2='$my_var2'"
