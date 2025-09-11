# This script is a file analyzer. Given an input_path and an output_path
# the script will iterate through the files in the input_path and copy them into dedicated folders 
# in the output_path depending on the file extension.

# Source the utility script. This makes all its functions available here.
# Use BASH_SOURCE to get the directory where this script is located,
# making the source command work regardless of how it's called.

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/file_utils.sh"


get_destination_folder_name() 
{   
    # this function expects 1 input: 
    # 1. the file extension
    file_extension=$1

    case $file_extension in
        "txt")
            destination_folder_name="text_files"
            ;;
        "jpg" | "jpeg" | "png" | "gif")
            destination_folder_name="images"
            ;;
        "mp3" | "wav" | "ogg")
            destination_folder_name="audio"
            ;;
        "mp4" | "avi" | "mkv")
            destination_folder_name="videos"
            ;;
        "pdf" | "doc" | "docx" | "xls" | "xlsx" | "ppt" | "pptx")
            destination_folder_name="documents"
            ;;
        "zip" | "rar" | "7z")
            destination_folder_name="archives"
            ;;
        "exe" | "dmg" | "pkg")
            destination_folder_name="executables"
            ;;
        *)
            destination_folder_name="other"
            ;;
    esac

    echo $destination_folder_name
}


verify_output_path()
{
    local path="$1"
    # If the path exists but is not a directory, it's an error.
    if [ -e "$path" ] && ! is_directory "$path"; then
        echo "Error: Output path '$path' exists but is not a directory." >&2
        exit 1
    fi
    # If the path doesn't exist, create it. The -p flag is important.
    # It creates parent directories as needed and doesn't fail if it already exists.
    mkdir -p "$path"

}

# define a function to copy the files to the destination folder
migrate_directory()
{
    local source_path="$1"
    local destination_path="$2"


    # Standard way to check if directory is empty
    if [ -z "$(ls -A "$source_path")" ]; then
        echo "$source_path is empty"
        return 0
    else
        echo "$source_path is not empty"
    fi

    # Use a safer loop that handles glob expansion properly
    for file in "$source_path"/*
    do
        # Double-check that the file actually exists (handles edge cases)
        # the line isn't necessary... but well, it doesn't hurt to be a bit paranoid.
        [ ! -e "$file" ] && continue

        # Check if the item is actually a file (and not a directory)
        if [ -f "$file" ]; then
            # We need the filename part of the path to get the extension.
            filename=$(basename "$file")
            
            # get the file extension
            this_file_extension=$(get_file_extension "$filename")

            # Proceed only if the file has an extension
            if [ -n "$this_file_extension" ]; then
                # get the destination folder name
                this_destination_folder_name=$(get_destination_folder_name "$this_file_extension")

                # create the destination folder if it does not exist
                destination_dir="$destination_path/$this_destination_folder_name"
                mkdir -p "$destination_dir"

                # see if the last command was successful
                if [ $? -ne 0 ]; then
                    echo "The destination folder was not created successfully"
                    exit 1
                fi

                # copy the file to the destination folder
                echo "Copying '$filename' to '$this_destination_folder_name/'..."
                cp "$file" "$destination_dir"
            fi
        else
            # at this point, we know that the file is a directory (since files exist, it's either -f or -d)
            # get the directory name
            dirname=$(basename "$file")
            
            # create the new destination path: destination_path/dirname
            new_destination_path="$destination_path/$dirname"
            mkdir -p "$new_destination_path"
            
            # call the function recursively with the current directory and new destination path
            migrate_directory "$file" "$new_destination_path"
        fi
    done
}
