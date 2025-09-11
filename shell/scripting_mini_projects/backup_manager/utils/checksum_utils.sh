#!/bin/bash
#
# Checksum utilities
# Functions for creating and verifying file checksums
#

# ============================================================================
# CHECKSUM CREATION
# ============================================================================

create_checksum() {
    local file_path="$1"
    local algorithm="${2:-$CHECKSUM_ALGORITHM}"
    local checksum_file="${3:-${file_path}.${algorithm}}"
    
    log_debug "Creating $algorithm checksum for: $file_path"
    
    if [[ ! -f "$file_path" ]]; then
        log_error "File not found: $file_path"
        return 1
    fi
    
    # Generate checksum based on algorithm
    local checksum_command
    case "$algorithm" in
        "md5")
            checksum_command="md5sum"
            ;;
        "sha1")
            checksum_command="sha1sum"
            ;;
        "sha256")
            checksum_command="sha256sum"
            ;;
        "sha512")
            checksum_command="sha512sum"
            ;;
        *)
            log_error "Unsupported checksum algorithm: $algorithm"
            return 1
            ;;
    esac
    
    # Check if command exists
    if ! command_exists "$checksum_command"; then
        log_error "Checksum command not found: $checksum_command"
        return 1
    fi
    
    # Create checksum
    if "$checksum_command" "$file_path" > "$checksum_file"; then
        log_debug "Checksum created: $checksum_file"
        return 0
    else
        log_error "Failed to create checksum"
        return 1
    fi
}

# ============================================================================
# CHECKSUM VERIFICATION
# ============================================================================

verify_checksum() {
    local file_path="$1"
    local checksum_file="${2:-}"
    local algorithm="${3:-$CHECKSUM_ALGORITHM}"
    
    log_debug "Verifying checksum for: $file_path"
    
    # Determine checksum file if not provided
    if [[ -z "$checksum_file" ]]; then
        checksum_file="${file_path}.${algorithm}"
    fi
    
    if [[ ! -f "$checksum_file" ]]; then
        log_error "Checksum file not found: $checksum_file"
        return 1
    fi
    
    # Determine verification command
    local checksum_command
    case "$algorithm" in
        "md5")
            checksum_command="md5sum"
            ;;
        "sha1")
            checksum_command="sha1sum"
            ;;
        "sha256")
            checksum_command="sha256sum"
            ;;
        "sha512")
            checksum_command="sha512sum"
            ;;
        *)
            log_error "Unsupported checksum algorithm: $algorithm"
            return 1
            ;;
    esac
    
    # Verify checksum
    if "$checksum_command" -c "$checksum_file" >/dev/null 2>&1; then
        log_debug "Checksum verification passed"
        return 0
    else
        log_error "Checksum verification failed"
        return 1
    fi
}
