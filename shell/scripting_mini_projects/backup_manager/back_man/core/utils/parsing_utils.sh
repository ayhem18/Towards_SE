#!/bin/bash
#
# Parsing utilities for backup manager
# Functions to parse remote paths and extract server/user information
#

# Source validation utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/validation_utils.sh"

# Parse remote path in format: user@hostname:/path
# Returns server hostname, username, and remote path
parse_remote_path() {
    local remote_path="$1"
    # local var_name: is the declaration of a local variable
    # lcaol -n var_name: means that the function should be called with placeholders
    # and the placeholders will be filled by the function call.
    local -n hostname_ref="$2"
    local -n username_ref="$3"  
    local -n remote_dir_ref="$4"
    
    # Check if it's a remote path (contains : and optionally @)
    if [[ ! "$remote_path" =~ : ]]; then
        echo "Error: Invalid remote path format. Expected user@hostname:/path" >&2
        return 1
    fi
    
    # Split by colon to separate host part and path part
    local host_part="${remote_path%%:*}"
    remote_dir_ref="${remote_path#*:}"
    
    # Check if username is specified (contains @) - now required
    if [[ "$host_part" =~ @ ]]; then
        username_ref="${host_part%@*}"
        hostname_ref="${host_part#*@}"
    else
        # Username is required
        echo "Error: Username must be specified. Expected format: user@hostname:/path" >&2
        return 1
    fi
    
    # Validate all components using dedicated validation functions
    if ! validate_user_name "$username_ref"; then
        return 1
    fi
    
    if ! validate_host "$hostname_ref"; then
        return 1
    fi
    
    # Validate and normalize the remote path
    local normalized_path
    if ! validate_remote_path "$remote_dir_ref" normalized_path; then
        return 1
    fi
    
    # Update the remote_dir_ref with the normalized absolute path
    remote_dir_ref="$normalized_path"
    
    return 0
}


