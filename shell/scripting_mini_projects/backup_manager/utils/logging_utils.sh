#!/bin/bash
#
# Logging utilities
# Centralized logging system for the backup manager
#

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Log levels
declare -A LOG_LEVELS=(
    ["DEBUG"]=0
    ["INFO"]=1
    ["WARN"]=2
    ["ERROR"]=3
    ["FATAL"]=4
)

# Current log level (default to INFO)
CURRENT_LOG_LEVEL=${CURRENT_LOG_LEVEL:-1}

# Log file paths
LOG_FILE=""
ERROR_LOG_FILE=""

# ============================================================================
# LOGGING INITIALIZATION
# ============================================================================

init_logging() {
    # Ensure log directory exists
    mkdir -p "$LOG_DIR"
    
    # Set log file paths
    LOG_FILE="$LOG_DIR/backup_manager.log"
    ERROR_LOG_FILE="$LOG_DIR/backup_manager_error.log"
    
    # Create log files if they don't exist
    touch "$LOG_FILE" "$ERROR_LOG_FILE"
    
    # Rotate logs if they're too large
    rotate_logs_if_needed
    
    # Log session start
    log_info "=== Backup Manager Session Started ==="
    log_info "PID: $$"
    log_info "User: $USER"
    log_info "Working Directory: $(pwd)"
}

# ============================================================================
# LOG ROTATION
# ============================================================================

rotate_logs_if_needed() {
    # Convert MB to bytes for comparison
    local max_size_bytes=$((MAX_LOG_SIZE * 1024 * 1024))
    
    # Check and rotate main log file
    if [[ -f "$LOG_FILE" ]]; then
        local log_size
        log_size=$(get_file_size "$LOG_FILE")
        if [[ $log_size -gt $max_size_bytes ]]; then
            rotate_log_file "$LOG_FILE"
        fi
    fi
    
    # Check and rotate error log file
    if [[ -f "$ERROR_LOG_FILE" ]]; then
        local error_log_size
        error_log_size=$(get_file_size "$ERROR_LOG_FILE")
        if [[ $error_log_size -gt $max_size_bytes ]]; then
            rotate_log_file "$ERROR_LOG_FILE"
        fi
    fi
}

rotate_log_file() {
    local log_file="$1"
    local timestamp
    timestamp=$(get_filename_timestamp)
    
    # Compress and archive old log
    gzip -c "$log_file" > "${log_file}.${timestamp}.gz"
    
    # Clear the current log file
    > "$log_file"
    
    # Clean up old log files (keep only LOG_RETENTION number of files)
    find "$LOG_DIR" -name "$(basename "$log_file").*.gz" -type f | \
        sort -r | tail -n +$((LOG_RETENTION + 1)) | xargs rm -f
}

# ============================================================================
# CORE LOGGING FUNCTIONS
# ============================================================================

# Generic logging function
log_message() {
    local level="$1"
    local message="$2"
    local timestamp
    timestamp=$(get_timestamp)
    local pid=$$
    
    # Check if we should log this level
    local level_num=${LOG_LEVELS[$level]:-1}
    if [[ $level_num -lt $CURRENT_LOG_LEVEL ]]; then
        return 0
    fi
    
    # Format log message
    local formatted_message="[$timestamp] [$level] [PID:$pid] $message"
    
    # Write to appropriate log files
    echo "$formatted_message" >> "$LOG_FILE"
    
    # Also write errors to error log
    if [[ "$level" == "ERROR" || "$level" == "FATAL" ]]; then
        echo "$formatted_message" >> "$ERROR_LOG_FILE"
    fi
    
    # Output to console based on level and debug mode
    case "$level" in
        "DEBUG")
            if [[ "$DEBUG_MODE" == "true" ]]; then
                echo -e "\033[0;36m[DEBUG]\033[0m $message" >&2
            fi
            ;;
        "INFO")
            echo -e "\033[0;32m[INFO]\033[0m $message"
            ;;
        "WARN")
            echo -e "\033[0;33m[WARN]\033[0m $message" >&2
            ;;
        "ERROR")
            echo -e "\033[0;31m[ERROR]\033[0m $message" >&2
            ;;
        "FATAL")
            echo -e "\033[0;35m[FATAL]\033[0m $message" >&2
            ;;
    esac
}

# ============================================================================
# CONVENIENCE LOGGING FUNCTIONS
# ============================================================================

log_debug() {
    log_message "DEBUG" "$1"
}

log_info() {
    log_message "INFO" "$1"
}

log_warn() {
    log_message "WARN" "$1"
}

log_error() {
    log_message "ERROR" "$1"
}

log_fatal() {
    log_message "FATAL" "$1"
}

# ============================================================================
# SPECIALIZED LOGGING FUNCTIONS
# ============================================================================

# Log command execution with timing
log_command() {
    local description="$1"
    shift
    local command=("$@")
    
    log_info "Executing: $description"
    log_debug "Command: ${command[*]}"
    
    local start_time
    start_time=$(date +%s)
    
    # Execute command and capture exit code
    local exit_code=0
    "${command[@]}" || exit_code=$?
    
    local end_time
    end_time=$(date +%s)
    local duration
    duration=$(time_diff "$start_time" "$end_time")
    local formatted_duration
    formatted_duration=$(format_duration "$duration")
    
    if [[ $exit_code -eq 0 ]]; then
        log_info "Command completed successfully in $formatted_duration"
    else
        log_error "Command failed with exit code $exit_code after $formatted_duration"
    fi
    
    return $exit_code
}

# Log backup operation progress
log_progress() {
    local current="$1"
    local total="$2"
    local item="$3"
    
    local percentage=$((current * 100 / total))
    log_info "Progress: $current/$total ($percentage%) - $item"
}

# Log file operation
log_file_operation() {
    local operation="$1"
    local source="$2"
    local destination="${3:-}"
    local size="${4:-}"
    
    local message="$operation: $source"
    if [[ -n "$destination" ]]; then
        message="$message -> $destination"
    fi
    if [[ -n "$size" ]]; then
        local human_size
        human_size=$(bytes_to_human "$size")
        message="$message ($human_size)"
    fi
    
    log_info "$message"
}

# Log system resource usage
log_system_resources() {
    local load_avg
    load_avg=$(get_load_average)
    
    local disk_usage
    disk_usage=$(df -h "$LOCAL_BACKUP_DIR" | awk 'NR==2 {print $5}')
    
    local memory_usage
    memory_usage=$(free | awk 'NR==2{printf "%.1f%%", $3*100/$2}')
    
    log_debug "System Resources - Load: $load_avg, Disk: $disk_usage, Memory: $memory_usage"
}

# ============================================================================
# LOG ANALYSIS FUNCTIONS
# ============================================================================

# Show recent log entries
show_recent_logs() {
    local lines="${1:-20}"
    local level="${2:-}"
    
    echo "Recent log entries:"
    echo "==================="
    
    if [[ -n "$level" ]]; then
        grep "\[$level\]" "$LOG_FILE" | tail -n "$lines"
    else
        tail -n "$lines" "$LOG_FILE"
    fi
}

# Show error summary
show_error_summary() {
    echo "Error Summary:"
    echo "============="
    
    if [[ -f "$ERROR_LOG_FILE" ]]; then
        # Count errors by type
        echo "Error counts:"
        grep -o "\[ERROR\].*" "$ERROR_LOG_FILE" | \
            sed 's/\[ERROR\] //' | \
            cut -d' ' -f1 | \
            sort | uniq -c | sort -nr
        
        echo
        echo "Recent errors:"
        tail -n 10 "$ERROR_LOG_FILE"
    else
        echo "No errors found"
    fi
}

# Search logs for specific patterns
search_logs() {
    local pattern="$1"
    local context_lines="${2:-3}"
    
    echo "Searching logs for: $pattern"
    echo "============================="
    
    grep -n -C "$context_lines" "$pattern" "$LOG_FILE" || {
        echo "No matches found"
        return 1
    }
}
