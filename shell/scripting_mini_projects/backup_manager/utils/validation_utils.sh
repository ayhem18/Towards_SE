#!/bin/bash
#
# Validation utilities
# Functions to validate inputs, configurations, and system requirements
#

# ============================================================================
# PATH VALIDATION
# ============================================================================

validate_source_path() {
    local path="$1"
    
    if [[ -z "$path" ]]; then
        log_error "Source path cannot be empty"
        return 1
    fi
    
    if [[ ! -e "$path" ]]; then
        log_error "Source path does not exist: $path"
        return 1
    fi
    
    if [[ ! -r "$path" ]]; then
        log_error "Source path is not readable: $path"
        return 1
    fi
    
    log_debug "Source path validation passed: $path"
    return 0
}

validate_destination_path() {
    local path="$1"
    local create_if_missing="${2:-true}"
    
    if [[ -z "$path" ]]; then
        log_error "Destination path cannot be empty"
        return 1
    fi
    
    # Check if it's an S3 path
    if [[ "$path" =~ ^s3:// ]]; then
        return 0  # S3 paths are validated separately
    fi
    
    # Check if it's an SSH path
    if [[ "$path" =~ ^[^@]+@[^:]+: ]]; then
        return 0  # SSH paths are validated separately
    fi
    
    # For local paths
    if [[ -e "$path" ]]; then
        if [[ ! -d "$path" ]]; then
            log_error "Destination exists but is not a directory: $path"
            return 1
        fi
        
        if [[ ! -w "$path" ]]; then
            log_error "Destination directory is not writable: $path"
            return 1
        fi
    else
        if [[ "$create_if_missing" == "true" ]]; then
            if ! mkdir -p "$path" 2>/dev/null; then
                log_error "Cannot create destination directory: $path"
                return 1
            fi
        else
            log_error "Destination directory does not exist: $path"
            return 1
        fi
    fi
    
    log_debug "Destination path validation passed: $path"
    return 0
}

# ============================================================================
# CONFIGURATION VALIDATION
# ============================================================================

validate_config() {
    log_info "Validating configuration..."
    
    local errors=0
    
    # Validate directories
    for dir in "$LOCAL_BACKUP_DIR" "$TEMP_DIR" "$LOG_DIR"; do
        if ! mkdir -p "$dir" 2>/dev/null; then
            log_error "Cannot create required directory: $dir"
            ((errors++))
        fi
    done
    
    # Validate compression setting
    if [[ "$DEFAULT_COMPRESSION" != "none" && "$DEFAULT_COMPRESSION" != "gzip" && 
          "$DEFAULT_COMPRESSION" != "bzip2" && "$DEFAULT_COMPRESSION" != "xz" ]]; then
        log_error "Invalid compression method: $DEFAULT_COMPRESSION"
        ((errors++))
    fi
    
    # Validate numeric settings
    if ! [[ "$DEFAULT_RETENTION_DAYS" =~ ^[0-9]+$ ]] || [[ "$DEFAULT_RETENTION_DAYS" -eq 0 ]]; then
        log_error "Invalid retention days: $DEFAULT_RETENTION_DAYS"
        ((errors++))
    fi
    
    if ! [[ "$MAX_PARALLEL_JOBS" =~ ^[0-9]+$ ]] || [[ "$MAX_PARALLEL_JOBS" -eq 0 ]]; then
        log_error "Invalid max parallel jobs: $MAX_PARALLEL_JOBS"
        ((errors++))
    fi
    
    # Validate SSH settings if SSH user is specified
    if [[ -n "$SSH_USER" ]]; then
        if [[ -n "$SSH_KEY_FILE" && ! -f "$SSH_KEY_FILE" ]]; then
            log_error "SSH key file not found: $SSH_KEY_FILE"
            ((errors++))
        fi
        
        if ! [[ "$SSH_TIMEOUT" =~ ^[0-9]+$ ]]; then
            log_error "Invalid SSH timeout: $SSH_TIMEOUT"
            ((errors++))
        fi
    fi
    
    # Validate GPG settings if encryption is enabled
    if [[ "$DEFAULT_ENCRYPTION" == "true" ]]; then
        if ! command_exists gpg; then
            log_error "GPG is required for encryption but not installed"
            ((errors++))
        elif [[ -n "$GPG_KEY_ID" ]]; then
            if ! gpg --list-keys "$GPG_KEY_ID" >/dev/null 2>&1; then
                log_error "GPG key not found: $GPG_KEY_ID"
                ((errors++))
            fi
        fi
    fi
    
    if [[ $errors -eq 0 ]]; then
        log_info "Configuration validation passed"
        return 0
    else
        log_error "Configuration validation failed with $errors errors"
        return 1
    fi
}

# ============================================================================
# SYSTEM REQUIREMENTS VALIDATION
# ============================================================================

validate_system_requirements() {
    log_info "Validating system requirements..."
    
    local errors=0
    local warnings=0
    
    # Check required commands
    local required_commands=("tar" "gzip" "find" "awk" "sed")
    for cmd in "${required_commands[@]}"; do
        if ! command_exists "$cmd"; then
            log_error "Required command not found: $cmd"
            ((errors++))
        fi
    done
    
    # Check optional but recommended commands
    local optional_commands=("gpg" "ssh" "scp" "rsync" "curl" "aws")
    for cmd in "${optional_commands[@]}"; do
        if ! command_exists "$cmd"; then
            log_warn "Optional command not found: $cmd (some features may not work)"
            ((warnings++))
        fi
    done
    
    # Check disk space
    local available_space
    available_space=$(get_disk_space "$LOCAL_BACKUP_DIR")
    local min_space=$((1024 * 1024 * 1024))  # 1GB minimum
    
    if [[ $available_space -lt $min_space ]]; then
        log_error "Insufficient disk space. Available: $(bytes_to_human "$available_space"), Minimum: $(bytes_to_human "$min_space")"
        ((errors++))
    fi
    
    # Check system load
    if ! check_system_load "5.0"; then
        log_warn "High system load detected. Backup operations may be slow."
        ((warnings++))
    fi
    
    # Check permissions
    if [[ ! -w "$LOCAL_BACKUP_DIR" ]]; then
        log_error "No write permission to backup directory: $LOCAL_BACKUP_DIR"
        ((errors++))
    fi
    
    if [[ $errors -eq 0 ]]; then
        log_info "System requirements validation passed"
        if [[ $warnings -gt 0 ]]; then
            log_info "Note: $warnings warnings found (see above)"
        fi
        return 0
    else
        log_error "System requirements validation failed with $errors errors"
        return 1
    fi
}

# ============================================================================
# SSH VALIDATION
# ============================================================================

validate_ssh_config() {
    local user="$1"
    local host="$2"
    local key_file="${3:-}"
    
    log_debug "Validating SSH configuration for $user@$host"
    
    # Check if SSH client is available
    if ! command_exists ssh; then
        log_error "SSH client not found"
        return 1
    fi
    
    # Check SSH key file if specified
    if [[ -n "$key_file" ]]; then
        if [[ ! -f "$key_file" ]]; then
            log_error "SSH key file not found: $key_file"
            return 1
        fi
        
        if [[ ! -r "$key_file" ]]; then
            log_error "SSH key file not readable: $key_file"
            return 1
        fi
        
        # Check key file permissions (should be 600 or 400)
        local perms
        perms=$(stat -c%a "$key_file" 2>/dev/null || stat -f%Lp "$key_file" 2>/dev/null)
        if [[ "$perms" != "600" && "$perms" != "400" ]]; then
            log_warn "SSH key file has loose permissions: $perms (recommended: 600)"
        fi
    fi
    
    log_debug "SSH configuration validation passed"
    return 0
}

test_ssh_connection() {
    local user="$1"
    local host="$2"
    local key_file="${3:-$SSH_KEY_FILE}"
    local timeout="${4:-$SSH_TIMEOUT}"
    
    log_debug "Testing SSH connection to $user@$host"
    
    local ssh_opts=("-o" "ConnectTimeout=$timeout" "-o" "BatchMode=yes" "-o" "StrictHostKeyChecking=no")
    
    if [[ -n "$key_file" ]]; then
        ssh_opts+=("-i" "$key_file")
    fi
    
    # Test connection with a simple command
    if ssh "${ssh_opts[@]}" "$user@$host" "echo 'SSH connection test successful'" >/dev/null 2>&1; then
        log_debug "SSH connection test passed"
        return 0
    else
        log_error "SSH connection test failed"
        return 1
    fi
}

# ============================================================================
# S3 VALIDATION
# ============================================================================

validate_s3_config() {
    log_debug "Validating S3 configuration"
    
    # Check if AWS CLI is available
    if ! command_exists aws; then
        log_error "AWS CLI not found (required for S3 operations)"
        return 1
    fi
    
    # Check if AWS credentials are configured
    if ! aws sts get-caller-identity >/dev/null 2>&1; then
        log_error "AWS credentials not configured. Run 'aws configure' first."
        return 1
    fi
    
    # Check S3 bucket configuration
    if [[ -z "$S3_BUCKET" ]]; then
        log_error "S3_BUCKET not configured"
        return 1
    fi
    
    # Test S3 bucket access
    if ! aws s3 ls "s3://$S3_BUCKET/" >/dev/null 2>&1; then
        log_error "Cannot access S3 bucket: $S3_BUCKET"
        return 1
    fi
    
    log_debug "S3 configuration validation passed"
    return 0
}

# ============================================================================
# BACKUP SPECIFIC VALIDATION
# ============================================================================

validate_backup_id() {
    local backup_id="$1"
    
    if [[ -z "$backup_id" ]]; then
        log_error "Backup ID cannot be empty"
        return 1
    fi
    
    # Check backup ID format (should be backup_YYYYMMDD_HHMMSS)
    if [[ ! "$backup_id" =~ ^backup_[0-9]{8}_[0-9]{6}$ ]]; then
        log_warn "Backup ID format unusual: $backup_id (expected: backup_YYYYMMDD_HHMMSS)"
    fi
    
    return 0
}

validate_backup_file() {
    local backup_file="$1"
    
    if [[ ! -f "$backup_file" ]]; then
        log_error "Backup file not found: $backup_file"
        return 1
    fi
    
    if [[ ! -r "$backup_file" ]]; then
        log_error "Backup file not readable: $backup_file"
        return 1
    fi
    
    # Check if it's a valid archive file
    local file_type
    file_type=$(file "$backup_file" 2>/dev/null)
    
    if [[ "$file_type" =~ (tar|gzip|bzip2|xz|ZIP) ]]; then
        log_debug "Backup file validation passed: $backup_file"
        return 0
    else
        log_warn "Backup file may not be a valid archive: $backup_file"
        return 1
    fi
}
