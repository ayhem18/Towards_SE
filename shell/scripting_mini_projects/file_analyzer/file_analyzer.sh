script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/file_utils.sh"

input_path=$1
output_path=$2

verify_output_path "$output_path"

migrate_directory "$input_path" "$output_path"

echo "File organization complete."