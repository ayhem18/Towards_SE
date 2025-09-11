#!/bin/bash
#
# Common utility functions
# Shared functions used across the backup system
#

# ============================================================================
# STRING AND PATH UTILITIES
# ============================================================================

# Check if a string is empty or contains only whitespace
is_empty() {
    local str="$1"
    [[ -z "${str// }" ]]
}

# Get absolute path of a file or directory
get_absolute_path() {
    local path="$1"
    
    if [[ -d "$path" ]]; then
        (cd "$path" && pwd)
    elif [[ -f "$path" ]]; then
        (cd "$(dirname "$path")" && echo "$(pwd)/$(basename "$path")")
    else
        echo "$(cd "$(dirname "$path")" 2>/dev/null && echo "$(pwd)/$(basename "$path")")"
    fi
}

# Get file size in bytes
get_file_size() {
    local file="$1"
    
    if [[ -f "$file" ]]; then
        stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null
    else
        echo "0"
    fi
}

# Convert bytes to human readable format
bytes_to_human() {
    local bytes="$1"
    local units=("B" "KB" "MB" "GB" "TB")
    local unit=0
    
    while [[ $bytes -gt 1024 && $unit -lt ${#units[@]} ]]; do
        bytes=$((bytes / 1024))
        ((unit++))
    done
    
    echo "${bytes}${units[$unit]}"
}

# ============================================================================
# DATE AND TIME UTILITIES
# ============================================================================

# Get current timestamp in ISO format
get_timestamp() {
    date '+%Y-%m-%d %H:%M:%S'
}

# Get current timestamp for filenames (no spaces or colons)
get_filename_timestamp() {
    date '+%Y%m%d_%H%M%S'
}

# Calculate time difference in seconds
time_diff() {
    local start_time="$1"
    local end_time="$2"
    
    echo $((end_time - start_time))
}

# Format seconds into human readable duration
format_duration() {
    local total_seconds="$1"
    local hours=$((total_seconds / 3600))
    local minutes=$(((total_seconds % 3600) / 60))
    local seconds=$((total_seconds % 60))
    
    if [[ $hours -gt 0 ]]; then
        printf "%dh %02dm %02ds" "$hours" "$minutes" "$seconds"
    elif [[ $minutes -gt 0 ]]; then
        printf "%dm %02ds" "$minutes" "$seconds"
    else
        printf "%ds" "$seconds"
    fi
}

# ============================================================================
# SYSTEM UTILITIES
# ============================================================================

# Check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Get available disk space in bytes
get_disk_space() {
    local path="$1"
    
    # Use df to get available space in 1K blocks, then convert to bytes
    df -k "$path" | awk 'NR==2 {print $4 * 1024}'
}

# Check if there's enough disk space for a file
check_disk_space() {
    local file_size="$1"
    local target_path="$2"
    local buffer_percent="${3:-10}"  # 10% buffer by default
    
    local available_space
    available_space=$(get_disk_space "$target_path")
    
    # Add buffer to required space
    local required_space=$((file_size + (file_size * buffer_percent / 100)))
    
    [[ $available_space -gt $required_space ]]
}

# Get system load average
get_load_average() {
    uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | tr -d ','
}

# Check if system load is acceptable for backup operations
check_system_load() {
    local max_load="${1:-2.0}"
    local current_load
    current_load=$(get_load_average)
    
    # Use awk for floating point comparison
    awk -v current="$current_load" -v max="$max_load" 'BEGIN {exit (current > max)}'
}

# ============================================================================
# NETWORK UTILITIES
# ============================================================================

# Check if a host is reachable
ping_host() {
    local host="$1"
    local timeout="${2:-5}"
    
    ping -c 1 -W "$timeout" "$host" >/dev/null 2>&1
}

# Test internet connectivity
test_internet() {
    ping_host "8.8.8.8" 3 || ping_host "1.1.1.1" 3
}

# Parse SSH destination string (user@host:/path)
parse_ssh_destination() {
    local destination="$1"
    local -n user_ref="$2"
    local -n host_ref="$3"
    local -n path_ref="$4"
    
    # Extract user@host part
    local userhost="${destination%%:*}"
    path_ref="${destination#*:}"
    
    # Extract user and host
    if [[ "$userhost" == *"@"* ]]; then
        user_ref="${userhost%@*}"
        host_ref="${userhost#*@}"
    else
        user_ref="$USER"
        host_ref="$userhost"
    fi
}

# ============================================================================
# FILE SYSTEM UTILITIES
# ============================================================================

# Create directory with proper permissions
create_directory() {
    local dir_path="$1"
    local permissions="${2:-755}"
    
    mkdir -p "$dir_path" && chmod "$permissions" "$dir_path"
}

# Safe file removal with confirmation
safe_remove() {
    local file_path="$1"
    local force="${2:-false}"
    
    if [[ -e "$file_path" ]]; then
        if [[ "$force" == "true" ]]; then
            rm -rf "$file_path"
        else
            echo "Remove $file_path? (y/N): "
            read -r response
            case "$response" in
                [yY][eE][sS]|[yY])
                    rm -rf "$file_path"
                    ;;
                *)
                    echo "Skipped removal of $file_path"
                    return 1
                    ;;
            esac
        fi
    fi
}

# Copy file with progress (for large files)
copy_with_progress() {
    local source="$1"
    local destination="$2"
    
    if command_exists pv; then
        # Use pv (pipe viewer) for progress if available
        pv "$source" > "$destination"
    else
        # Fallback to regular cp
        cp "$source" "$destination"
    fi
}

# ============================================================================
# LOCK FILE UTILITIES
# ============================================================================

# Create a lock file to prevent concurrent operations
create_lock() {
    local lock_file="$1"
    local timeout="${2:-10}"
    
    local count=0
    while [[ $count -lt $timeout ]]; do
        if (set -C; echo $$ > "$lock_file") 2>/dev/null; then
            return 0
        fi
        
        # Check if the process holding the lock still exists
        if [[ -f "$lock_file" ]]; then
            local lock_pid
            lock_pid=$(cat "$lock_file" 2>/dev/null)
            if [[ -n "$lock_pid" ]] && ! kill -0 "$lock_pid" 2>/dev/null; then
                # Lock holder is dead, remove stale lock
                rm -f "$lock_file"
                continue
            fi
        fi
        
        sleep 1
        ((count++))
    done
    
    return 1
}

# Remove a lock file
remove_lock() {
    local lock_file="$1"
    rm -f "$lock_file"
}

# ============================================================================
# RETRY UTILITIES
# ============================================================================

# Retry a command with exponential backoff
retry_command() {
    local max_attempts="$1"
    local base_delay="${2:-1}"
    shift 2
    local command=("$@")
    
    local attempt=1
    local delay=$base_delay
    
    while [[ $attempt -le $max_attempts ]]; do
        if "${command[@]}"; then
            return 0
        fi
        
        if [[ $attempt -lt $max_attempts ]]; then
            echo "Command failed (attempt $attempt/$max_attempts). Retrying in ${delay}s..." >&2
            sleep "$delay"
            delay=$((delay * 2))
        fi
        
        ((attempt++))
    done
    
    echo "Command failed after $max_attempts attempts" >&2
    return 1
}
