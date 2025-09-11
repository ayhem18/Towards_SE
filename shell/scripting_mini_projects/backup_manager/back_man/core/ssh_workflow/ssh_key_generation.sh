#!/bin/bash
#
# SSH Key Generation and Management
# Functions to generate and manage SSH keys per remote server
#

# Source parsing utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../utils/parsing_utils.sh"

# Generate SSH key pair for a specific remote server
generate_ssh_key_pair() {
    local hostname="$1"
    local username="$2"
    
    echo "Generating SSH key pair for $username@$hostname..."
    
    # Get directory and file paths
    local key_dir=$(get_ssh_key_dir "$hostname" "$username")
    local private_key=$(get_private_key_path "$hostname" "$username")
    local public_key=$(get_public_key_path "$hostname" "$username")
    
    # Create directory if it doesn't exist
    if [[ ! -d "$key_dir" ]]; then
        mkdir -p "$key_dir"
        echo "Created SSH key directory: $key_dir"
    fi
    
    # Check if keys already exist
    if [[ -f "$private_key" ]]; then
        echo "SSH keys already exist for $username@$hostname"
        echo "Private key: $private_key"
        echo "Public key: $public_key"
        return 0
    fi
    
    # Generate SSH key pair
    local server_id=$(generate_server_id "$hostname" "$username")
    local comment="backup_manager_${server_id}_$(date +%Y%m%d)"
    
    ssh-keygen -t ed25519 \
               -f "$private_key" \
               -C "$comment" \
               -N ""  # No passphrase for automation
    
    if [[ $? -eq 0 ]]; then
        # Set proper permissions
        chmod 600 "$private_key"
        chmod 644 "$public_key"
        
        echo "✅ SSH key pair generated successfully!"
        echo "Private key: $private_key"
        echo "Public key: $public_key"
        return 0
    else
        echo "❌ Failed to generate SSH key pair"
        return 1
    fi
}

# Test SSH connection using generated keys
test_ssh_connection() {
    local hostname="$1"
    local username="$2"
    
    local private_key=$(get_private_key_path "$hostname" "$username")
    
    if [[ ! -f "$private_key" ]]; then
        echo "No SSH key found for $username@$hostname"
        return 1
    fi
    
    echo "Testing SSH connection to $username@$hostname..."
    
    # Test connection with timeout
    ssh -i "$private_key" \
        -o BatchMode=yes \
        -o ConnectTimeout=10 \
        -o StrictHostKeyChecking=no \
        -o UserKnownHostsFile=/dev/null \
        "$username@$hostname" \
        "echo 'SSH connection test successful'" 2>/dev/null
    
    local exit_code=$?
    
    if [[ $exit_code -eq 0 ]]; then
        echo "✅ SSH connection successful"
        return 0
    else
        echo "❌ SSH connection failed (exit code: $exit_code)"
        return 1
    fi
}

# Copy public key to remote server
copy_public_key_to_server() {
    local hostname="$1"
    local username="$2"
    
    local public_key=$(get_public_key_path "$hostname" "$username")
    
    if [[ ! -f "$public_key" ]]; then
        echo "No public key found for $username@$hostname"
        return 1
    fi
    
    echo "Copying public key to $username@$hostname..."
    echo "You will be prompted for the password for $username@$hostname"
    
    # Use ssh-copy-id to copy the public key
    ssh-copy-id -i "$public_key" "$username@$hostname"
    
    local exit_code=$?
    
    if [[ $exit_code -eq 0 ]]; then
        echo "✅ Public key copied successfully"
        
        # Test the connection to confirm it works
        if test_ssh_connection "$hostname" "$username"; then
            echo "✅ Passwordless SSH connection confirmed"
            return 0
        else
            echo "⚠️  Public key copied but connection test failed"
            return 1
        fi
    else
        echo "❌ Failed to copy public key"
        return 1
    fi
}

# Setup SSH connection for a new remote server
setup_ssh_connection() {
    local hostname="$1"
    local username="$2"
    
    echo "Setting up SSH connection for $username@$hostname"
    echo "================================================="
    
    # Step 1: Generate key pair if needed
    if ! generate_ssh_key_pair "$hostname" "$username"; then
        echo "Failed to generate SSH keys"
        return 1
    fi
    
    # Step 2: Test if connection already works
    if test_ssh_connection "$hostname" "$username"; then
        echo "SSH connection already established"
        return 0
    fi
    
    # Step 3: Copy public key to server
    echo
    echo "First time connecting to $hostname"
    echo "Need to copy public key for passwordless access"
    
    if copy_public_key_to_server "$hostname" "$username"; then
        echo "✅ SSH setup completed successfully"
        return 0
    else
        echo "❌ SSH setup failed"
        return 1
    fi
}
