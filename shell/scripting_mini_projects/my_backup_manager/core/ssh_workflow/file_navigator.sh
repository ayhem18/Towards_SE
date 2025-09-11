# this script is used to locate the corresponding files for given ssh related information

# given a hostname and a username 
# find the corresponding private and public keys files
# find the corresponding server_user config file


# Generate a unique identifier for a remote server connection
# Format: hostname_username
generate_server_id() {
    local hostname="$1"
    local username="$2"
    
    # Clean hostname and username to be filesystem-safe
    local clean_hostname=$(echo "$hostname" | tr '.' '_' | tr -cd '[:alnum:]_-')
    local clean_username=$(echo "$username" | tr -cd '[:alnum:]_-')
    
    echo "${clean_hostname}_${clean_username}"
}


# Get the directory path for storing SSH keys for a specific server
get_ssh_key_dir() {
    local hostname="$1"
    local username="$2"
    
    local server_id=$(generate_server_id "$hostname" "$username")
    echo "$BACKUP_MANAGER_HOME_DIR/$SSH_KEYS_DIR_NAME/$server_id"
}

# Get the private key file path for a specific server
get_private_key_path() {
    local hostname="$1"
    local username="$2"
    
    local server_id=$(generate_server_id "$hostname" "$username")
    local key_dir=$(get_ssh_key_dir "$hostname" "$username")
    echo "${key_dir}/.private_key_${server_id}"
}

# Get the public key file path for a specific server
get_public_key_path() {
    local hostname="$1"
    local username="$2"
    
    local private_key=$(get_private_key_path "$hostname" "$username")
    echo "${private_key}.pub"
}

# Get the config file path for a specific server
get_server_config_path() {
    local hostname="$1"
    local username="$2"
    
    local server_id=$(generate_server_id "$hostname" "$username")
    echo "$BACKUP_MANAGER_HOME_DIR/$REMOTE_CONFIGS_DIR_NAME/config_${server_id}.conf"
}

