#!/bin/bash
#
# Core backup functionality
# This file contains the main backup and restore functions
#

# Source dependencies
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.."
source "$SCRIPT_DIR/utils/validation_utils.sh"
source "$SCRIPT_DIR/utils/compression_utils.sh"
source "$SCRIPT_DIR/utils/encryption_utils.sh"

# ============================================================================
# BACKUP FUNCTIONS
# ============================================================================

handle_backup() {
    local source_path="$1"
    local destination="$2"
    
    log_info "Starting backup operation"
    log_info "Source: $source_path"
    log_info "Destination: $destination"
    
    # Validate inputs
    validate_source_path "$source_path" || {
        log_error "Invalid source path: $source_path"
        exit 1
    }
    
    # Determine backup method based on destination
    local backup_method
    backup_method=$(determine_backup_method "$destination")
    
    log_info "Backup method: $backup_method"
    
    # Generate backup ID with timestamp
    local backup_id
    backup_id="backup_$(date '+%Y%m%d_%H%M%S')"
    
    # Create backup based on method
    case "$backup_method" in
        "local")
            create_local_backup "$source_path" "$destination" "$backup_id"
            ;;
        "ssh")
            create_ssh_backup "$source_path" "$destination" "$backup_id"
            ;;
        "s3")
            create_s3_backup "$source_path" "$destination" "$backup_id"
            ;;
        *)
            log_error "Unsupported backup method: $backup_method"
            exit 1
            ;;
    esac
    
    log_info "Backup completed successfully: $backup_id"
}

create_local_backup() {
    local source_path="$1"
    local destination="$2"
    local backup_id="$3"
    
    log_info "Creating local backup..."
    
    # Ensure destination directory exists
    mkdir -p "$destination"
    
    # Create backup file path
    local backup_file="$destination/${backup_id}.tar"
    
    # Add compression if enabled
    if [[ "$DEFAULT_COMPRESSION" != "none" ]]; then
        backup_file="${backup_file}.${DEFAULT_COMPRESSION}"
    fi
    
    # Create the backup archive
    if create_archive "$source_path" "$backup_file"; then
        # Generate checksum
        create_checksum "$backup_file"
        
        # Encrypt if enabled
        if [[ "$DEFAULT_ENCRYPTION" == "true" ]]; then
            encrypt_file "$backup_file"
        fi
        
        # Record backup metadata
        record_backup_metadata "$backup_id" "local" "$source_path" "$backup_file"
        
        log_info "Local backup created: $backup_file"
    else
        log_error "Failed to create local backup"
        return 1
    fi
}

create_ssh_backup() {
    local source_path="$1"
    local destination="$2"
    local backup_id="$3"
    
    log_info "Creating SSH backup..."
    
    # Parse SSH destination (user@host:/path)
    local ssh_user ssh_host ssh_path
    parse_ssh_destination "$destination" ssh_user ssh_host ssh_path
    
    # Test SSH connectivity
    if ! test_ssh_connection "$ssh_user" "$ssh_host"; then
        log_error "Cannot connect to SSH host: $ssh_host"
        return 1
    fi
    
    # Create remote directory if needed
    ssh "${ssh_user}@${ssh_host}" "mkdir -p '$ssh_path'"
    
    # Create local temporary backup first
    local temp_backup="$TEMP_DIR/${backup_id}.tar.gz"
    create_archive "$source_path" "$temp_backup"
    
    # Transfer to remote host
    if scp "$temp_backup" "${ssh_user}@${ssh_host}:${ssh_path}/"; then
        # Clean up temporary file
        rm -f "$temp_backup"
        
        # Record backup metadata
        record_backup_metadata "$backup_id" "ssh" "$source_path" "$destination/${backup_id}.tar.gz"
        
        log_info "SSH backup completed: $destination"
    else
        log_error "Failed to transfer backup to remote host"
        rm -f "$temp_backup"
        return 1
    fi
}

create_s3_backup() {
    local source_path="$1"
    local destination="$2"
    local backup_id="$3"
    
    log_info "Creating S3 backup..."
    
    # Validate S3 configuration
    validate_s3_config || {
        log_error "S3 configuration is invalid"
        return 1
    }
    
    # Create local temporary backup
    local temp_backup="$TEMP_DIR/${backup_id}.tar.gz"
    create_archive "$source_path" "$temp_backup"
    
    # Upload to S3
    local s3_path="${destination}/${backup_id}.tar.gz"
    if aws s3 cp "$temp_backup" "$s3_path" --storage-class "$S3_STORAGE_CLASS"; then
        # Clean up temporary file
        rm -f "$temp_backup"
        
        # Record backup metadata
        record_backup_metadata "$backup_id" "s3" "$source_path" "$s3_path"
        
        log_info "S3 backup completed: $s3_path"
    else
        log_error "Failed to upload backup to S3"
        rm -f "$temp_backup"
        return 1
    fi
}

# ============================================================================
# RESTORE FUNCTIONS
# ============================================================================

handle_restore() {
    local backup_id="$1"
    local target_path="$2"
    
    log_info "Starting restore operation"
    log_info "Backup ID: $backup_id"
    log_info "Target path: $target_path"
    
    # Find backup metadata
    local backup_info
    backup_info=$(get_backup_metadata "$backup_id")
    
    if [[ -z "$backup_info" ]]; then
        log_error "Backup not found: $backup_id"
        exit 1
    fi
    
    # Parse backup information
    local backup_method backup_location
    backup_method=$(echo "$backup_info" | cut -d'|' -f2)
    backup_location=$(echo "$backup_info" | cut -d'|' -f4)
    
    log_info "Backup method: $backup_method"
    log_info "Backup location: $backup_location"
    
    # Restore based on backup method
    case "$backup_method" in
        "local")
            restore_local_backup "$backup_location" "$target_path"
            ;;
        "ssh")
            restore_ssh_backup "$backup_location" "$target_path"
            ;;
        "s3")
            restore_s3_backup "$backup_location" "$target_path"
            ;;
        *)
            log_error "Unsupported backup method: $backup_method"
            exit 1
            ;;
    esac
    
    log_info "Restore completed successfully"
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

determine_backup_method() {
    local destination="$1"
    
    if [[ "$destination" =~ ^s3:// ]]; then
        echo "s3"
    elif [[ "$destination" =~ ^[^@]+@[^:]+: ]]; then
        echo "ssh"
    else
        echo "local"
    fi
}

record_backup_metadata() {
    local backup_id="$1"
    local method="$2"
    local source="$3"
    local location="$4"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Create metadata directory if it doesn't exist
    mkdir -p "$SCRIPT_DIR/data"
    
    # Append to backup log
    echo "$backup_id|$method|$source|$location|$timestamp" >> "$SCRIPT_DIR/data/backup_log.txt"
}

get_backup_metadata() {
    local backup_id="$1"
    local backup_log="$SCRIPT_DIR/data/backup_log.txt"
    
    if [[ -f "$backup_log" ]]; then
        grep "^$backup_id|" "$backup_log"
    fi
}

show_backup_status() {
    log_info "Backup System Status"
    echo "===================="
    
    # Show configuration
    echo "Configuration:"
    echo "  Default method: $DEFAULT_BACKUP_METHOD"
    echo "  Compression: $DEFAULT_COMPRESSION"
    echo "  Encryption: $DEFAULT_ENCRYPTION"
    echo
    
    # Show recent backups
    echo "Recent backups:"
    if [[ -f "$SCRIPT_DIR/data/backup_log.txt" ]]; then
        tail -10 "$SCRIPT_DIR/data/backup_log.txt" | while IFS='|' read -r id method source location timestamp; do
            echo "  $timestamp - $id ($method)"
        done
    else
        echo "  No backups found"
    fi
}

list_backups() {
    log_info "Available Backups"
    echo "=================="
    
    if [[ -f "$SCRIPT_DIR/data/backup_log.txt" ]]; then
        printf "%-20s %-8s %-30s %s\n" "BACKUP ID" "METHOD" "SOURCE" "TIMESTAMP"
        printf "%-20s %-8s %-30s %s\n" "--------" "------" "------" "---------"
        while IFS='|' read -r id method source location timestamp; do
            printf "%-20s %-8s %-30s %s\n" "$id" "$method" "$(basename "$source")" "$timestamp"
        done < "$SCRIPT_DIR/data/backup_log.txt"
    else
        echo "No backups found"
    fi
}

handle_config() {
    local action="${1:-show}"
    
    case "$action" in
        "show")
            log_info "Current Configuration"
            echo "====================="
            cat "$SCRIPT_DIR/config/settings.conf" | grep -v '^#' | grep -v '^$'
            ;;
        "edit")
            "${EDITOR:-nano}" "$SCRIPT_DIR/config/settings.conf"
            ;;
        *)
            log_error "Unknown config action: $action"
            echo "Usage: config [show|edit]"
            exit 1
            ;;
    esac
}

handle_cleanup() {
    local retention_days="${1:-$DEFAULT_RETENTION_DAYS}"
    
    log_info "Cleaning up backups older than $retention_days days"
    
    # Implementation for cleanup will be added later
    echo "Cleanup functionality will be implemented in Phase 2"
}

test_system() {
    log_info "Testing backup system configuration"
    
    # Test directory permissions
    echo "✓ Testing directory permissions..."
    mkdir -p "$LOCAL_BACKUP_DIR" "$TEMP_DIR" "$LOG_DIR"
    
    # Test compression tools
    echo "✓ Testing compression tools..."
    if command -v gzip >/dev/null 2>&1; then
        echo "  - gzip: available"
    else
        echo "  - gzip: missing"
    fi
    
    # Test encryption tools
    echo "✓ Testing encryption tools..."
    if command -v gpg >/dev/null 2>&1; then
        echo "  - gpg: available"
    else
        echo "  - gpg: missing"
    fi
    
    echo "System test completed"
}

cleanup_on_exit() {
    # Clean up temporary files
    if [[ -d "$TEMP_DIR" ]]; then
        find "$TEMP_DIR" -name "backup_*" -type f -delete 2>/dev/null || true
    fi
}
