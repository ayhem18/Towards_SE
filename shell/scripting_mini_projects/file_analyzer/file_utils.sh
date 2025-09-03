# this script contains a few functions to help with file operations

# A function for use in an 'if' statement should use 'return' to signal its status.
# return 0  => success (true)
# return 1+ => failure (false)
is_directory() 
{
    # this function expects 1 input: 
    # 1. the path to the file or directory
    local path="$1"

    # first check if the path exists
    if [ -e "$path" ]; then
        # then check if it is a directory
        if [ -d "$path" ]; then
            return 0 # It exists and is a directory.
        else
            return 1 # It exists but is NOT a directory.
        fi
    else
        # at this point, the path does not exist
        # A non-existent path is considered a directory path if it ends with "/"
        if [[ "${path: -1}" == "/" ]]; then
            return 0 # Looks like a directory path.
        else
            return 1 # Does not look like a directory path.
        fi
    fi 
}

# This function checks if a path points to a file or a potential file.
is_file()
{
    local path="$1"

    # first check if the path exists
    if [ -e "$path" ]; then
        if [ -f "$path" ]; then
            return 0 # It exists and is a file.
        else
            return 1 # It exists but is NOT a file (e.g. a directory)
        fi
    else
        # If it doesn't exist, it's a potential file path *unless* it's a
        # potential directory path. We can simply return the opposite of is_directory.
        ! is_directory "$path"
    fi
}


# # --- Example Usage ---
# # Try running:
# # ./file_utils.sh /home
# # ./file_utils.sh /home/
# # ./file_utils.sh /home/non_existent_file.txt
# # ./file_utils.sh /home/non_existent_dir/

# p="$1"
# echo "Checking path: $p"

# if is_directory "$p"; then
#     echo "-> The path is a directory"
# else
#     echo "-> The path is NOT a directory"
# fi

# if is_file "$p"; then
#     echo "-> The path is a file"
# else
#     echo "-> The path is NOT a file"
# fi



get_file_extension()
{   
    # Extract file extension using parameter expansion.
    # A file has NO extension if:
    # 1. Empty string
    # 2. No dots at all
    # 3. Starts with dot and has no other dots (hidden files like .bashrc)
    local filename="$1"

    # although the 2 first conditions can be written in a single if statement, they are left seperate for readability.

    # Condition 1: Empty string
    if [[ -z "$filename" ]]; then
        echo ""
        return
    fi

    # Condition 2: No dots at all
    if [[ "$filename" != *.* ]]; then
        echo ""
        return
    fi

    # Condition 3: Starts with dot and has no other dots
    if [[ "${filename:0:1}" == "." ]]; then
        # Remove the first character (the leading dot)
        local after_first_dot="${filename:1}"
        # If what remains has no dots, then no extension
        if [[ "$after_first_dot" != *.* ]]; then
            echo ""
            return
        fi
    fi

    # If we reach here, the file has an extension
    echo "${filename##*.}"
}


# --- Example Usage ---
# You can uncomment this block to test this file directly.
# p=$1
# if is_file "$p"; then
#     # We need to get just the filename, not the whole path
#     fname=$(basename "$p")
#     extension=$(get_file_extension "$fname")
#     if [ -n "$extension" ]; then
#         echo "The file extension is: '$extension'"
#     else
#         echo "The file has no extension."
#     fi
# else
#     echo "The path is not a file."
# fi