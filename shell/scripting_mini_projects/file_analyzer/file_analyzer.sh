# This script is a file analyzer. Given an input_path and an output_path
# the script will iterate through the files in the input_path and copy them into dedicated folders 
# in the output_path depending on the file extension.

# Source the utility script. This makes all its functions available here.
# "$(dirname "$0")" gets the directory where this script is located,
# making the source command work regardless of where you run it from.
source "$(dirname "$0")/file_utils.sh"


# 1. create a function to get the file extension (Done in file_utils.sh)
# 2. create a function to determine the folder name based on the file extension 
# 3. a functiont to verify the conditions about the output path (if it does not exist, create it)

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



input_path=$1
output_path=$2 

# make sure that the input path is a directory
if ! is_directory "$input_path"; then
    echo "Error: input path '$input_path' is not a valid directory." >&2
    exit 1
fi


verify_output_path "$output_path"


# Iterate through the files in the input path.
# This loop is safer than `ls` as it handles filenames with spaces.
for file in "$input_path"/*
do 
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
            destination_dir="$output_path/$this_destination_folder_name"
            mkdir -p "$destination_dir"

            # copy the file to the destination folder
            echo "Copying '$filename' to '$this_destination_folder_name/'..."
            cp "$file" "$destination_dir"
        fi
    fi
done

echo "File organization complete."






