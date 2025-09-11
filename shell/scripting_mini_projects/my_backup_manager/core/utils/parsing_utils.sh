#!/bin/bash
#
# Parsing utilities for backup manager
# Functions to parse remote paths and extract server/user information
#

# Parse remote path in format: user@hostname:/path
# Returns server hostname, username, and remote path
parse_remote_path() {
    local remote_path="$1"
    local -n hostname_ref="$2"
    local -n username_ref="$3"  
    local -n remote_dir_ref="$4"
    
    # Check if it's a remote path (contains : and optionally @)
    if [[ ! "$remote_path" =~ : ]]; then
        echo "Error: Invalid remote path format. Expected user@hostname:/path or hostname:/path" >&2
        return 1
    fi
    
    # Split by colon to separate host part and path part
    local host_part="${remote_path%%:*}"
    remote_dir_ref="${remote_path#*:}"
    
    # Check if username is specified (contains @)
    if [[ "$host_part" =~ @ ]]; then
        username_ref="${host_part%@*}"
        hostname_ref="${host_part#*@}"
    else
        # No username specified, use current user
        username_ref="$USER"
        hostname_ref="$host_part"
    fi
    
    # Validate that we have all required components
    if [[ -z "$hostname_ref" ]]; then
        echo "Error: No hostname found in remote path" >&2
        return 1
    fi
    
    if [[ -z "$remote_dir_ref" ]]; then
        echo "Error: No remote directory specified" >&2
        return 1
    fi
    
    return 0
}


