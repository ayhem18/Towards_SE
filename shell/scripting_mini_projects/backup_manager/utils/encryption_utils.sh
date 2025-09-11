#!/bin/bash
#
# Encryption utilities
# Functions for encrypting and decrypting backup files using GPG
#

# ============================================================================
# ENCRYPTION FUNCTIONS
# ============================================================================

encrypt_file() {
    local input_file="$1"
    local output_file="${2:-${input_file}.gpg}"
    local key_id="${3:-$GPG_KEY_ID}"
    
    log_info "Encrypting file: $input_file"
    
    # Validate input file
    if [[ ! -f "$input_file" ]]; then
        log_error "Input file not found: $input_file"
        return 1
    fi
    
    # Check if GPG is available
    if ! command_exists gpg; then
        log_error "GPG not found. Encryption requires GPG to be installed."
        return 1
    fi
    
    # Determine encryption method
    local gpg_opts=()
    
    if [[ -n "$key_id" ]]; then
        # Public key encryption
        log_debug "Using public key encryption with key: $key_id"
        
        # Verify key exists
        if ! gpg --list-keys "$key_id" >/dev/null 2>&1; then
            log_error "GPG key not found: $key_id"
            return 1
        fi
        
        gpg_opts+=("--encrypt" "--recipient" "$key_id")
    else
        # Symmetric encryption (password-based)
        log_debug "Using symmetric encryption"
        gpg_opts+=("--symmetric")
    fi
    
    # Add common options
    gpg_opts+=(
        "--cipher-algo" "$GPG_CIPHER"
        "--compress-algo" "$GPG_COMPRESSION"
        "--armor"
        "--output" "$output_file"
        "$input_file"
    )
    
    # Perform encryption
    if gpg "${gpg_opts[@]}" 2>/dev/null; then
        local original_size
        original_size=$(get_file_size "$input_file")
        local encrypted_size
        encrypted_size=$(get_file_size "$output_file")
        
        log_info "File encrypted successfully"
        log_debug "Original size: $(bytes_to_human "$original_size")"
        log_debug "Encrypted size: $(bytes_to_human "$encrypted_size")"
        
        # Optionally remove original file
        if [[ "$1" == "$input_file" ]]; then
            log_debug "Removing original unencrypted file"
            rm -f "$input_file"
        fi
        
        return 0
    else
        log_error "Failed to encrypt file"
        return 1
    fi
}

decrypt_file() {
    local input_file="$1"
    local output_file="${2:-}"
    
    log_info "Decrypting file: $input_file"
    
    # Validate input file
    if [[ ! -f "$input_file" ]]; then
        log_error "Encrypted file not found: $input_file"
        return 1
    fi
    
    # Check if it's a GPG file
    if [[ "$input_file" != *.gpg ]]; then
        log_warn "File doesn't have .gpg extension: $input_file"
    fi
    
    # Determine output file name if not provided
    if [[ -z "$output_file" ]]; then
        if [[ "$input_file" == *.gpg ]]; then
            output_file="${input_file%.gpg}"
        else
            output_file="${input_file}.decrypted"
        fi
    fi
    
    # Check if GPG is available
    if ! command_exists gpg; then
        log_error "GPG not found. Decryption requires GPG to be installed."
        return 1
    fi
    
    # Perform decryption
    local gpg_opts=(
        "--decrypt"
        "--output" "$output_file"
        "$input_file"
    )
    
    if gpg "${gpg_opts[@]}" 2>/dev/null; then
        local encrypted_size
        encrypted_size=$(get_file_size "$input_file")
        local decrypted_size
        decrypted_size=$(get_file_size "$output_file")
        
        log_info "File decrypted successfully: $output_file"
        log_debug "Encrypted size: $(bytes_to_human "$encrypted_size")"
        log_debug "Decrypted size: $(bytes_to_human "$decrypted_size")"
        
        return 0
    else
        log_error "Failed to decrypt file"
        return 1
    fi
}

# ============================================================================
# KEY MANAGEMENT
# ============================================================================

list_gpg_keys() {
    log_info "Available GPG Keys"
    echo "=================="
    
    if ! command_exists gpg; then
        log_error "GPG not installed"
        return 1
    fi
    
    echo "Public keys:"
    gpg --list-keys 2>/dev/null || echo "No public keys found"
    
    echo
    echo "Private keys:"
    gpg --list-secret-keys 2>/dev/null || echo "No private keys found"
}

generate_gpg_key() {
    local name="$1"
    local email="$2"
    local comment="${3:-Backup Manager Key}"
    
    log_info "Generating new GPG key pair"
    
    if [[ -z "$name" || -z "$email" ]]; then
        log_error "Name and email are required for key generation"
        echo "Usage: generate_gpg_key <name> <email> [comment]"
        return 1
    fi
    
    if ! command_exists gpg; then
        log_error "GPG not installed"
        return 1
    fi
    
    # Create key generation batch file
    local batch_file="$TEMP_DIR/gpg_batch_$$"
    cat > "$batch_file" << EOF
Key-Type: RSA
Key-Length: 4096
Subkey-Type: RSA
Subkey-Length: 4096
Name-Real: $name
Name-Comment: $comment
Name-Email: $email
Expire-Date: 2y
Passphrase: 
%commit
%echo Key generation completed
EOF
    
    # Generate key
    if gpg --batch --generate-key "$batch_file" 2>/dev/null; then
        log_info "GPG key pair generated successfully"
        
        # Get the key ID
        local key_id
        key_id=$(gpg --list-keys --with-colons "$email" 2>/dev/null | awk -F: '/^pub/ {print $5}' | head -1)
        
        if [[ -n "$key_id" ]]; then
            log_info "Key ID: $key_id"
            echo "You can use this key ID in your configuration:"
            echo "GPG_KEY_ID=\"$key_id\""
        fi
        
        # Clean up batch file
        rm -f "$batch_file"
        return 0
    else
        log_error "Failed to generate GPG key"
        rm -f "$batch_file"
        return 1
    fi
}

export_gpg_key() {
    local key_id="$1"
    local output_dir="${2:-$HOME/.backup_manager_keys}"
    
    if [[ -z "$key_id" ]]; then
        log_error "Key ID is required"
        return 1
    fi
    
    log_info "Exporting GPG key: $key_id"
    
    # Create output directory
    mkdir -p "$output_dir"
    
    # Export public key
    local pub_key_file="$output_dir/${key_id}_public.asc"
    if gpg --armor --export "$key_id" > "$pub_key_file" 2>/dev/null; then
        log_info "Public key exported: $pub_key_file"
    else
        log_error "Failed to export public key"
        return 1
    fi
    
    # Export private key (with warning)
    echo "Export private key? This is sensitive! (y/N): "
    read -r response
    case "$response" in
        [yY][eE][sS]|[yY])
            local priv_key_file="$output_dir/${key_id}_private.asc"
            if gpg --armor --export-secret-keys "$key_id" > "$priv_key_file" 2>/dev/null; then
                log_info "Private key exported: $priv_key_file"
                log_warn "IMPORTANT: Keep this private key secure!"
                chmod 600 "$priv_key_file"
            else
                log_error "Failed to export private key"
                return 1
            fi
            ;;
        *)
            log_info "Private key export skipped"
            ;;
    esac
    
    return 0
}

import_gpg_key() {
    local key_file="$1"
    
    if [[ -z "$key_file" ]]; then
        log_error "Key file path is required"
        return 1
    fi
    
    if [[ ! -f "$key_file" ]]; then
        log_error "Key file not found: $key_file"
        return 1
    fi
    
    log_info "Importing GPG key from: $key_file"
    
    if gpg --import "$key_file" 2>/dev/null; then
        log_info "GPG key imported successfully"
        return 0
    else
        log_error "Failed to import GPG key"
        return 1
    fi
}

# ============================================================================
# ENCRYPTION VERIFICATION
# ============================================================================

verify_encryption() {
    local encrypted_file="$1"
    local original_file="${2:-}"
    
    log_info "Verifying encryption: $encrypted_file"
    
    if [[ ! -f "$encrypted_file" ]]; then
        log_error "Encrypted file not found: $encrypted_file"
        return 1
    fi
    
    # Test if file is actually encrypted
    if file "$encrypted_file" | grep -q "GPG"; then
        log_debug "File is GPG encrypted"
    else
        log_warn "File may not be properly encrypted"
        return 1
    fi
    
    # If original file is provided, test round-trip encryption
    if [[ -n "$original_file" && -f "$original_file" ]]; then
        log_debug "Testing round-trip encryption/decryption"
        
        local temp_decrypted="$TEMP_DIR/verify_decrypt_$$"
        
        if decrypt_file "$encrypted_file" "$temp_decrypted"; then
            # Compare checksums
            local original_checksum
            original_checksum=$(sha256sum "$original_file" | cut -d' ' -f1)
            local decrypted_checksum
            decrypted_checksum=$(sha256sum "$temp_decrypted" | cut -d' ' -f1)
            
            if [[ "$original_checksum" == "$decrypted_checksum" ]]; then
                log_info "Encryption verification passed (checksums match)"
                rm -f "$temp_decrypted"
                return 0
            else
                log_error "Encryption verification failed (checksums don't match)"
                rm -f "$temp_decrypted"
                return 1
            fi
        else
            log_error "Cannot decrypt file for verification"
            return 1
        fi
    fi
    
    log_info "Basic encryption verification passed"
    return 0
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

check_gpg_setup() {
    log_info "Checking GPG setup"
    
    if ! command_exists gpg; then
        log_error "GPG is not installed"
        echo "To install GPG:"
        echo "  Ubuntu/Debian: sudo apt-get install gnupg"
        echo "  CentOS/RHEL: sudo yum install gnupg"
        echo "  macOS: brew install gnupg"
        return 1
    fi
    
    # Check GPG version
    local gpg_version
    gpg_version=$(gpg --version | head -1)
    log_info "GPG version: $gpg_version"
    
    # Check if we have any keys
    local public_keys
    public_keys=$(gpg --list-keys 2>/dev/null | grep -c "^pub" || echo "0")
    log_info "Public keys available: $public_keys"
    
    local private_keys
    private_keys=$(gpg --list-secret-keys 2>/dev/null | grep -c "^sec" || echo "0")
    log_info "Private keys available: $private_keys"
    
    if [[ "$DEFAULT_ENCRYPTION" == "true" && "$private_keys" -eq 0 ]]; then
        log_warn "Encryption is enabled but no private keys found"
        echo "Consider generating a key pair with: generate_gpg_key <name> <email>"
    fi
    
    return 0
}
