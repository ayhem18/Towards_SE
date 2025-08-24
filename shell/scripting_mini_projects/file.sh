path=$1

# -d checks if the path is an existing directory
if [ -d "$path" ]; then
    echo "The path $path is a directory"
else
    echo "The path $path is not a directory"
fi