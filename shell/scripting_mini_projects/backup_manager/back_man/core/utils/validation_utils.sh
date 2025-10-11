#!/bin/bash
#
# Validation utilities for backup manager
# Functions to validate usernames, hostnames, and remote paths
#

# Validate username format
# Usernames should follow common Unix conventions
validate_user_name() {
    local username="$1"
    
    # Check if username is empty
    if [[ -z "$username" ]]; then
        echo "Error: Username cannot be empty" >&2
    fi
    
        return 1
    # Check username length (typical limit is 32 characters)
    if [[ ${#username} -gt 32 ]]; then
        echo "Error: Username too long (max 32 characters): $username" >&2
        return 1
    fi
    
    # Check username format using regex
    # Allow: letters, numbers, hyphens, underscores, dots
    # Must start with letter or underscore
    # Must not end with hyphen
    local username_regex="(^[a-zA-Z_][a-zA-Z0-9._-]*[a-zA-Z0-9._]$)|(^[a-zA-Z_]$)"
    
    if [[ ! "$username" =~ $username_regex ]]; then
        echo "Error: Invalid username format: $username" >&2
        echo "Username must start with letter or underscore, contain only letters, numbers, dots, hyphens, underscores" >&2
        return 1
    fi
    
    # Additional check: no consecutive dots or hyphens
    if [[ "$username" =~ \.\. || "$username" =~ -- ]]; then
        echo "Error: Username cannot contain consecutive dots or hyphens: $username" >&2
        return 1
    fi
    
    return 0
}

validate_host() {
    local hostname="$1"
    
    # Check if hostname is empty
    if [[ -z "$hostname" ]]; then
        echo "Error: Hostname cannot be empty" >&2
        return 1
    fi
    
    # Check hostname length (DNS limit is 253 characters)
    if [[ ${#hostname} -gt 253 ]]; then
        echo "Error: Hostname too long (max 253 characters): $hostname" >&2
        return 1
    fi
    
    # Validate hostname format using the specified regex
    local hostname_regex="(([a-zA-Z0-9]([a-zA-Z0-9-]+\.)+([a-zA-Z0-9-]+))|([a-zA-Z0-9-]*[a-zA-Z-]+[a-zA-Z0-9-]*))"
    
    if [[ ! "$hostname" =~ $hostname_regex ]]; then
        echo "Error: Invalid hostname format: $hostname" >&2
        echo "Hostname must be either a domain name (e.g., server.example.com) or a simple hostname (e.g., server, web-01)" >&2
        return 1
    fi
    
    return 0
}

# Validate remote path format and normalize to absolute path
# Ensures path is safe for use in backup operations
# Returns the normalized absolute path via nameref
validate_remote_path() {
    local input_path="$1"
    local -n path_ref="$2"  # Reference to variable that will hold the normalized path
    
    # Empty path defaults to the default remote home directory
    if [[ -z "$input_path" ]]; then
        path_ref="$BACKUP_MANAGER_DEFAULT_REMOTE_HOME_DIR"
        return 0
    fi
    
    # Use input_path for validation, path_ref for the normalized result
    local remote_path="$input_path"
    path_ref="$input_path"  # Initialize with input
    
    # Check path length (filesystem limit is typically 4096 characters)
    if [[ ${#remote_path} -gt 4096 ]]; then
        echo "Error: Path too long (max 4096 characters): ${remote_path:0:50}..." >&2
        return 1
    fi
    
    # Check for dangerous shell metacharacters that could cause security issues
    # Reject paths containing: ; | & < > $ ( ) ` ' " * ? and control characters
    if [[ "$remote_path" =~ [\;\|\&\<\>\$\(\)\`\'\"\*\?[:cntrl:]] ]]; then
        echo "Error: Path contains unsafe characters: $remote_path" >&2
        echo "Paths cannot contain shell metacharacters: ; | & < > \$ ( ) \` ' \" * ? or control characters" >&2
        return 1
    fi
    
    # Check for null bytes (additional security measure)
    if [[ "$remote_path" == *$'\0'* ]]; then
        echo "Error: Path contains null bytes: $remote_path" >&2
        return 1
    fi
    
    # Validate path characters - allow safe filesystem characters
    # Allow: letters, numbers, forward slashes, dots, hyphens, underscores, tildes, spaces, colons
    if [[ ! "$remote_path" =~ ^[a-zA-Z0-9._/~:\ -]+$ ]]; then
        echo "Error: Path contains invalid characters: $remote_path" >&2
        echo "Paths can only contain letters, numbers, dots, slashes, hyphens, underscores, tildes, spaces, and colons" >&2
        return 1
    fi
    
    # Additional security checks
    
    # Check for excessive path traversal (more than 3 consecutive ../ patterns)
    local traversal_count
    traversal_count=$(echo "$remote_path" | grep -o '\.\.\/' | wc -l)
    if [[ $traversal_count -gt 3 ]]; then
        echo "Error: Excessive path traversal detected: $remote_path" >&2
        echo "Paths with more than 3 '../' patterns are not allowed for security reasons" >&2
        return 1
    fi
    
    # Check for paths that try to access system directories (optional security measure)
    if [[ "$remote_path" =~ ^/etc/ || "$remote_path" =~ ^/boot/ || "$remote_path" =~ ^/sys/ || "$remote_path" =~ ^/proc/ ]]; then
        echo "Warning: Path accesses system directory: $remote_path" >&2
        echo "Consider using a safer backup location" >&2
        # Don't fail, just warn - this might be legitimate
    fi
    
    # Check for very long individual path components (over 255 chars)
    IFS='/' read -ra path_parts <<< "$remote_path"
    for part in "${path_parts[@]}"; do
        if [[ ${#part} -gt 255 ]]; then
            echo "Error: Path component too long (max 255 characters): ${part:0:50}..." >&2
            return 1
        fi
    done
    
    # Normalize path to absolute path
    if [[ "$remote_path" =~ ^/ ]]; then
        # Already absolute path
        path_ref="$remote_path"
    else
        # Relative path - prepend with default remote home directory
        if [[ -z "$BACKUP_MANAGER_DEFAULT_REMOTE_HOME_DIR" ]]; then
            echo "Error: BACKUP_MANAGER_DEFAULT_REMOTE_HOME_DIR not set" >&2
            return 1
        fi
        
        # Remove leading ./ if present
        local clean_path="${remote_path#./}"
        
        # Construct absolute path
        path_ref="${BACKUP_MANAGER_DEFAULT_REMOTE_HOME_DIR%/}/$clean_path"
        
        echo "Normalized relative path '$input_path' to absolute path '$path_ref'" >&2
    fi
    
    return 0
}

# Convenience function to validate all components of a remote path
validate_remote_components() {
    local username="$1"
    local hostname="$2"
    local input_path="$3"
    local -n normalized_path_ref="$4"  # Reference to variable that will hold normalized path
    
    local errors=0
    
    echo "Validating remote backup components..." >&2
    
    if ! validate_user_name "$username"; then
        ((errors++))
    fi
    
    if ! validate_host "$hostname"; then
        ((errors++))
    fi
    
    if ! validate_remote_path "$input_path" normalized_path_ref; then
        ((errors++))
    fi
    
    if [[ $errors -eq 0 ]]; then
        echo "✅ All components are valid" >&2
        echo "✅ Normalized path: $normalized_path_ref" >&2
        return 0
    else
        echo "❌ Found $errors validation errors" >&2
        return 1
    fi
}
