#!/bin/bash
#
# Compression utilities
# Functions for creating and extracting compressed archives
#

# ============================================================================
# ARCHIVE CREATION
# ============================================================================

create_archive() {
    local source_path="$1"
    local archive_path="$2"
    local compression="${3:-$DEFAULT_COMPRESSION}"
    
    log_info "Creating archive: $archive_path"
    log_debug "Source: $source_path, Compression: $compression"
    
    local tar_opts=()
    local archive_dir
    archive_dir=$(dirname "$archive_path")
    
    # Ensure archive directory exists
    mkdir -p "$archive_dir"
    
    # Determine compression options
    case "$compression" in
        "gzip")
            tar_opts+=("-z")
            ;;
        "bzip2")
            tar_opts+=("-j")
            ;;
        "xz")
            tar_opts+=("-J")
            ;;
        "none")
            # No compression
            ;;
        *)
            log_error "Unsupported compression method: $compression"
            return 1
            ;;
    esac
    
    # Add common tar options
    tar_opts+=("-c" "-f" "$archive_path")
    
    # Add exclude patterns if needed
    if [[ "$INCLUDE_HIDDEN" != "true" ]]; then
        tar_opts+=("--exclude=.*")
    fi
    
    # Handle symbolic links
    if [[ "$FOLLOW_SYMLINKS" == "true" ]]; then
        tar_opts+=("-h")
    fi
    
    # Add progress reporting if available
    if command_exists pv && [[ -t 1 ]]; then
        # Calculate source size for progress
        local source_size
        source_size=$(du -sb "$source_path" 2>/dev/null | cut -f1)
        
        if [[ -n "$source_size" && $source_size -gt 0 ]]; then
            tar "${tar_opts[@]}" -C "$(dirname "$source_path")" "$(basename "$source_path")" | \
                pv -s "$source_size" > /dev/null
        else
            tar "${tar_opts[@]}" -C "$(dirname "$source_path")" "$(basename "$source_path")"
        fi
    else
        # Create archive without progress
        tar "${tar_opts[@]}" -C "$(dirname "$source_path")" "$(basename "$source_path")"
    fi
    
    local exit_code=$?
    
    if [[ $exit_code -eq 0 ]]; then
        local archive_size
        archive_size=$(get_file_size "$archive_path")
        log_info "Archive created successfully: $(bytes_to_human "$archive_size")"
        return 0
    else
        log_error "Failed to create archive (exit code: $exit_code)"
        return 1
    fi
}

# ============================================================================
# ARCHIVE EXTRACTION
# ============================================================================

extract_archive() {
    local archive_path="$1"
    local target_path="$2"
    local preserve_structure="${3:-true}"
    
    log_info "Extracting archive: $archive_path"
    log_debug "Target: $target_path, Preserve structure: $preserve_structure"
    
    # Validate archive file
    if ! validate_backup_file "$archive_path"; then
        return 1
    fi
    
    # Create target directory
    mkdir -p "$target_path"
    
    # Determine archive type and compression
    local file_type
    file_type=$(file "$archive_path" 2>/dev/null)
    
    local tar_opts=()
    
    # Detect compression type
    if [[ "$file_type" =~ gzip ]]; then
        tar_opts+=("-z")
    elif [[ "$file_type" =~ bzip2 ]]; then
        tar_opts+=("-j")
    elif [[ "$file_type" =~ XZ ]]; then
        tar_opts+=("-J")
    fi
    
    # Add extraction options
    tar_opts+=("-x" "-f" "$archive_path" "-C" "$target_path")
    
    # Preserve permissions and timestamps
    tar_opts+=("-p")
    
    # Add verbose output if debug is enabled
    if [[ "$DEBUG_MODE" == "true" ]]; then
        tar_opts+=("-v")
    fi
    
    # Extract with progress if possible
    if command_exists pv && [[ -t 1 ]]; then
        local archive_size
        archive_size=$(get_file_size "$archive_path")
        pv "$archive_path" | tar "${tar_opts[@]}" --exclude="$archive_path"
    else
        tar "${tar_opts[@]}"
    fi
    
    local exit_code=$?
    
    if [[ $exit_code -eq 0 ]]; then
        log_info "Archive extracted successfully to: $target_path"
        return 0
    else
        log_error "Failed to extract archive (exit code: $exit_code)"
        return 1
    fi
}

# ============================================================================
# ARCHIVE VERIFICATION
# ============================================================================

verify_archive() {
    local archive_path="$1"
    
    log_debug "Verifying archive integrity: $archive_path"
    
    if [[ ! -f "$archive_path" ]]; then
        log_error "Archive file not found: $archive_path"
        return 1
    fi
    
    # Determine archive type
    local file_type
    file_type=$(file "$archive_path" 2>/dev/null)
    
    local tar_opts=("-t" "-f" "$archive_path")
    
    # Add compression options
    if [[ "$file_type" =~ gzip ]]; then
        tar_opts=("-t" "-z" "-f" "$archive_path")
    elif [[ "$file_type" =~ bzip2 ]]; then
        tar_opts=("-t" "-j" "-f" "$archive_path")
    elif [[ "$file_type" =~ XZ ]]; then
        tar_opts=("-t" "-J" "-f" "$archive_path")
    fi
    
    # Test archive integrity
    if tar "${tar_opts[@]}" >/dev/null 2>&1; then
        log_debug "Archive verification passed: $archive_path"
        return 0
    else
        log_error "Archive verification failed: $archive_path"
        return 1
    fi
}

# ============================================================================
# ARCHIVE INFORMATION
# ============================================================================

get_archive_info() {
    local archive_path="$1"
    
    if [[ ! -f "$archive_path" ]]; then
        log_error "Archive file not found: $archive_path"
        return 1
    fi
    
    echo "Archive Information:"
    echo "==================="
    echo "File: $archive_path"
    echo "Size: $(bytes_to_human "$(get_file_size "$archive_path")")"
    echo "Type: $(file "$archive_path" | cut -d: -f2- | sed 's/^ *//')"
    echo "Modified: $(stat -c%y "$archive_path" 2>/dev/null || stat -f%Sm "$archive_path" 2>/dev/null)"
    echo
    
    # List contents (first 20 entries)
    echo "Contents (first 20 entries):"
    echo "============================"
    
    local file_type
    file_type=$(file "$archive_path" 2>/dev/null)
    
    local tar_opts=("-t" "-f" "$archive_path")
    
    if [[ "$file_type" =~ gzip ]]; then
        tar_opts=("-t" "-z" "-f" "$archive_path")
    elif [[ "$file_type" =~ bzip2 ]]; then
        tar_opts=("-t" "-j" "-f" "$archive_path")
    elif [[ "$file_type" =~ XZ ]]; then
        tar_opts=("-t" "-J" "-f" "$archive_path")
    fi
    
    tar "${tar_opts[@]}" 2>/dev/null | head -20
    
    # Count total entries
    local total_entries
    total_entries=$(tar "${tar_opts[@]}" 2>/dev/null | wc -l)
    echo
    echo "Total entries: $total_entries"
}

# ============================================================================
# COMPRESSION TESTING
# ============================================================================

test_compression_methods() {
    local test_file="$1"
    
    if [[ ! -f "$test_file" ]]; then
        log_error "Test file not found: $test_file"
        return 1
    fi
    
    local original_size
    original_size=$(get_file_size "$test_file")
    
    echo "Compression Test Results"
    echo "======================="
    echo "Original file: $test_file"
    echo "Original size: $(bytes_to_human "$original_size")"
    echo
    
    local temp_dir="$TEMP_DIR/compression_test_$$"
    mkdir -p "$temp_dir"
    
    # Test different compression methods
    local methods=("none" "gzip" "bzip2" "xz")
    
    for method in "${methods[@]}"; do
        echo "Testing $method compression..."
        
        local test_archive="$temp_dir/test_${method}.tar"
        if [[ "$method" != "none" ]]; then
            test_archive="${test_archive}.${method}"
        fi
        
        local start_time
        start_time=$(date +%s)
        
        if create_archive "$(dirname "$test_file")" "$test_archive" "$method"; then
            local end_time
            end_time=$(date +%s)
            local duration
            duration=$((end_time - start_time))
            
            local compressed_size
            compressed_size=$(get_file_size "$test_archive")
            local ratio
            ratio=$((compressed_size * 100 / original_size))
            
            printf "  %-8s: %s (%d%%) in %ds\n" \
                "$method" \
                "$(bytes_to_human "$compressed_size")" \
                "$ratio" \
                "$duration"
        else
            echo "  $method: FAILED"
        fi
    done
    
    # Clean up
    rm -rf "$temp_dir"
}
