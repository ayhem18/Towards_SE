#!/bin/bash
#
# Setup script for backup manager environment variables
# This script reads the config file and sets environment variables with defaults
#

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/default_config.conf"

# Function to read config file and extract default values
read_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        # Source the config file to get default values
        source "$CONFIG_FILE"
    else
        echo "Warning: Config file not found at $CONFIG_FILE" >&2
        echo "Using hardcoded defaults" >&2
    fi
}

# Function to set environment variable with default fallback
set_env_var() {
    local var_name="$1"
    local default_var_name="$2"
    local default_value="${!default_var_name}"
    
    # If environment variable is not set, use the default value
    if [[ -z "${!var_name}" ]]; then
        export "$var_name"="$default_value"
        echo "Set $var_name=$default_value (from config)"
    else
        echo "Using existing $var_name=${!var_name} (from environment)"
    fi
}

# Read configuration file
read_config

# Set environment variables with defaults
echo "Setting up backup manager environment variables..."

# 1. Backup manager home directory
set_env_var "BACKUP_MANAGER_HOME_DIR" "_DEFAULT_BACKUP_MANAGER_HOME_DIR"

# 2. Local backup directory name
set_env_var "LOCAL_BACKUP_DIRNAME" "_DEFAULT_LOCAL_BACKUP_DIRNAME"

# 3. Remote backup directory name  
set_env_var "REMOTE_BACKUP_DIRNAME" "_DEFAULT_REMOTE_BACKUP_DIRNAME"

# 4. Cloud backup directory name
set_env_var "CLOUD_BACKUP_DIRNAME" "_DEFAULT_CLOUD_BACKUP_DIRNAME"

# 5. Default backup file extension
set_env_var "BACKUP_FILE_EXTENSION" "_DEFAULT_BACKUP_FILE_EXTENSION"

# 6. Default backup file compression
set_env_var "BACKUP_FILE_COMPRESSION" "_DEFAULT_BACKUP_FILE_COMPRESSION"

# 7. SSH keys directory name
set_env_var "SSH_KEYS_DIR_NAME" "_DEFAULT_SSH_KEYS_DIR_NAME"

# 8. Remote configs directory name
set_env_var "REMOTE_CONFIGS_DIR_NAME" "_DEFAULT_REMOTE_CONFIGS_DIR_NAME"

# 9. Connection cache directory name
set_env_var "CONNECTION_CACHE_DIR_NAME" "_DEFAULT_CONNECTION_CACHE_DIR_NAME"

# 10. Default remote home directory for relative paths
set_env_var "BACKUP_MANAGER_DEFAULT_REMOTE_HOME_DIR" "_DEFAULT_BACKUP_MANAGER_DEFAULT_REMOTE_HOME_DIR"

# Create necessary directories
echo "Creating necessary directories..."

# Create backup manager home directory
if [[ -n "$BACKUP_MANAGER_HOME_DIR" && ! -d "$BACKUP_MANAGER_HOME_DIR" ]]; then
    mkdir -p "$BACKUP_MANAGER_HOME_DIR"
    echo "Created directory: $BACKUP_MANAGER_HOME_DIR"
fi

# Create subdirectories for different backup types
full_path_local_backup="$BACKUP_MANAGER_HOME_DIR/$LOCAL_BACKUP_DIRNAME"
if [[ ! -d "$full_path_local_backup" ]]; then
    mkdir -p "$full_path_local_backup"
    echo "Created directory: $full_path_local_backup"
fi

echo "Environment setup complete!"
