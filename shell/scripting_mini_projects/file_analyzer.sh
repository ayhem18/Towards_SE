# This script is a file analyzer. Given an input_path and an output_path
# the script will iterate through the files in the input_path and copy them into dedicated folders 
# in the output_path depending on the file extension.


# 1. create a function to get the file extension
# 2. create a function to determine the folder name based on the file extension 
# 3. a functiont to verify the conditions about the output path (if it does not exist, create it)


get_file_extension()
{   
    # how to solve this ?
    # basically split the file_name by the "." character and take the last part: it should be the file extension
    # the file must at least have one "." character

    file_name=$1

    # check if the file name is empty
    if [ -z "$file_name" ]; then
        echo "Error: file name is empty"
        return 1
    fi

    # check if there is at least one "." character 
    if [[ "$file_name" != *"."* ]]; then
        echo "Error: file name does not have a file extension"
        return 1
    fi

    # count the number of "." characters
    num_dots=$(echo $file_name | grep -o "\." | wc -l)

    i=($num_dots + 1)
    
    # get the file extension
    file_extension=$(echo $file_name | cut -d '.' -f $i)
    echo $file_extension
}


verify_output_path()
{
 
    output_path=$1
    # the output path does not need to exist. However, it cannot be a file
    if [ ! -f "$output_path" ]; then
        echo "Error: output path is a file"
        exit 1
    fi

    # at this point, we know the the output_path isn't a file, so if it is not a directory, we need to create it 
    if [ ! -d "$output_path" ]; then
        mkdir -p $output_path
    fi
}




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




input_path=$1
output_path=$2 

# make sure that the input path is a directory
if [ ! -d "$input_path" ]; then
    echo "Error: input path is not a directory"
    exit 1
fi


# iterate through the files in the input path
for file in $(ls $input_path)
do 

    # get the file extension
    this_file_extension=$(get_file_extension $file)

    # get the destination folder name
    this_destination_folder_name=$(get_destination_folder_name $this_file_extension)

    # create the destination folder if it does not exist
    if [ ! -d "$output_path/$this_destination_folder_name" ]; then
        mkdir -p $output_path/$this_destination_folder_name
    fi

    # copy the file to the destination folder
    cp $input_path/$file $output_path/$this_destination_folder_name

done






