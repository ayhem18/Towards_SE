#!/bin/bash
#
# SSH Connection Config Management
# Functions to create and manage per-server configuration files
#

# Source parsing utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../utils/parsing_utils.sh"
source "$SCRIPT_DIR/file_navigator.sh"

# Create or update server configuration file
create_server_config() {
    local hostname="$1"
    local username="$2"
    local password="${3:-}"  # Optional password parameter
    
    local config_file=$(get_server_config_path "$hostname" "$username")
    local config_dir=$(dirname "$config_file")
    
    # Create config directory if it doesn't exist
    if [[ ! -d "$config_dir" ]]; then
        mkdir -p "$config_dir"
        echo "Created config directory: $config_dir"
    fi
    
    # Create configuration file
    cat > "$config_file" << EOF
# Configuration for remote server connection
# Generated on: $(date)
# Server ID: $(generate_server_id "$hostname" "$username")

# Connection details
HOSTNAME="$hostname"
USERNAME="$username"
REMOTE_PATH=""

# SSH key paths
PRIVATE_KEY_PATH="$(get_private_key_path "$hostname" "$username")"
PUBLIC_KEY_PATH="$(get_public_key_path "$hostname" "$username")"

# Connection status
LAST_CONNECTION=""
KEY_COPIED="false"
CONNECTION_STATUS="unknown"

# Backup settings for this server
COMPRESSION_ENABLED="true"
ENCRYPTION_ENABLED="false"
BACKUP_COUNT="0"

# Connection history
CREATED_DATE="$(date '+%Y-%m-%d %H:%M:%S')"
LAST_UPDATED="$(date '+%Y-%m-%d %H:%M:%S')"
EOF

    # Set secure permissions for config file
    chmod 600 "$config_file"
    
    echo "Created server config: $config_file"
    return 0
}

# Update server config with connection status
update_connection_status() {
    local hostname="$1"
    local username="$2"
    local status="$3"  # "connected", "failed", "key_copied", etc.
    
    local config_file=$(get_server_config_path "$hostname" "$username")
    
    if [[ ! -f "$config_file" ]]; then
        echo "Config file not found: $config_file"
        return 1
    fi
    
    # Update specific fields in config
    sed -i "s/CONNECTION_STATUS=.*/CONNECTION_STATUS=\"$status\"/" "$config_file"
    sed -i "s/LAST_CONNECTION=.*/LAST_CONNECTION=\"$(date '+%Y-%m-%d %H:%M:%S')\"/" "$config_file"
    sed -i "s/LAST_UPDATED=.*/LAST_UPDATED=\"$(date '+%Y-%m-%d %H:%M:%S')\"/" "$config_file"
    
    if [[ "$status" == "connected" ]]; then
        sed -i "s/KEY_COPIED=.*/KEY_COPIED=\"true\"/" "$config_file"
    fi
    
    echo "Updated connection status for $username@$hostname: $status"
    return 0
}

# Read server configuration
read_server_config() {
    local hostname="$1"
    local username="$2"
    
    local config_file=$(get_server_config_path "$hostname" "$username")
    
    if [[ ! -f "$config_file" ]]; then
        echo "No configuration found for $username@$hostname"
        return 1
    fi
    
    # Source the config file to load variables
    source "$config_file"
    
    echo "Configuration for $username@$hostname:"
    echo "======================================"
    echo "Hostname: $HOSTNAME"
    echo "Username: $USERNAME"
    echo "Key Copied: $KEY_COPIED"
    echo "Connection Status: $CONNECTION_STATUS"
    echo "Last Connection: $LAST_CONNECTION"
    echo "Private Key: $PRIVATE_KEY_PATH"
    echo "Public Key: $PUBLIC_KEY_PATH"
    echo "Created: $CREATED_DATE"
    echo "Last Updated: $LAST_UPDATED"
    
    return 0
}

# Check if server config exists
server_config_exists() {
    local hostname="$1"
    local username="$2"
    
    local config_file=$(get_server_config_path "$hostname" "$username")
    
    if [[ -f "$config_file" ]]; then
        return 0  # Config exists
    else
        return 1  # Config doesn't exist
    fi
}

# List all server configurations
list_server_configs() {
    local config_dir="$BACKUP_MANAGER_HOME_DIR/$REMOTE_CONFIGS_DIR_NAME"
    
    if [[ ! -d "$config_dir" ]]; then
        echo "No server configurations found"
        return 1
    fi
    
    echo "Remote Server Configurations:"
    echo "============================="
    
    local count=0
    for config_file in "$config_dir"/config_*.conf; do
        if [[ -f "$config_file" ]]; then
            # Source config to get details
            source "$config_file"
            
            ((count++))
            echo "$count. $USERNAME@$HOSTNAME"
            echo "   Status: $CONNECTION_STATUS"
            echo "   Last Connection: $LAST_CONNECTION"
            echo "   Config File: $(basename "$config_file")"
            echo
        fi
    done
    
    if [[ $count -eq 0 ]]; then
        echo "No server configurations found"
        return 1
    fi
    
    echo "Total configurations: $count"
    return 0
}

# Get connection info for a server (returns 0 if configured, 1 if not)
get_server_connection_info() {
    local hostname="$1"
    local username="$2"
    local -n status_ref="$3"
    local -n last_connection_ref="$4"
    local -n key_copied_ref="$5"
    
    local config_file=$(get_server_config_path "$hostname" "$username")
    
    if [[ ! -f "$config_file" ]]; then
        status_ref="not_configured"
        last_connection_ref=""
        key_cocpied_ref="false"
        return 1
    fi
    
    # Source config to get values
    source "$config_file"
    
    status_ref="$CONNECTION_STATUS"
    last_connection_ref="$LAST_CONNECTION"
    key_copied_ref="$KEY_COPIED"
    
    return 0
}
