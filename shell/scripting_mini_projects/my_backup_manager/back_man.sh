#!/bin/bash

# Get script directory and source setup to load environment variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/setup.sh"

# the script should be able to delete old backups 

# so for now let's implement these few commands:

# 1. encrypt: 
## a. first argument is the file to encrypt 
## b. second argument is the location of the output file
## c. type of encryption 

# 2. compress:
## a. first argument is the file to compress 
## b. second argument is the location of the output file
## c. type of compression 

# 3. backup:
## a. first argument is the file or directory to backup
## b. second argument is the location of the backup
## c. type of backup

# 4. set:
## type of setting (specific set of possible values: enums)
## the value of the setting

# Interactive loop to test environment variables
echo "========================================"
echo "Environment variables loaded successfully!"
echo "========================================"
echo "BACKUP_MANAGER_HOME_DIR: $BACKUP_MANAGER_HOME_DIR"
echo "LOCAL_BACKUP_DIRNAME: $LOCAL_BACKUP_DIRNAME"
echo "REMOTE_BACKUP_DIRNAME: $REMOTE_BACKUP_DIRNAME"
echo "CLOUD_BACKUP_DIRNAME: $CLOUD_BACKUP_DIRNAME"
echo "BACKUP_FILE_EXTENSION: $BACKUP_FILE_EXTENSION"
echo "BACKUP_FILE_COMPRESSION: $BACKUP_FILE_COMPRESSION"
echo "========================================"

while true; do
    echo
    echo "Commands:"
    echo "  env     - Show all environment variables"
    echo "  dirs    - Show created directories"
    echo "  test    - Test a custom command"
    echo "  exit    - Exit the script"
    echo
    read -p "Enter command: " command
    
    case "$command" in
        env)
            echo "Current environment variables:"
            env | grep -E "(BACKUP_|DEFAULT_)" | sort
            ;;
        dirs)
            echo "Checking created directories:"
            ls -la "$BACKUP_MANAGER_HOME_DIR" 2>/dev/null || echo "Home directory not found"
            ;;
        test)
            read -p "Enter test command (e.g., 'echo \$BACKUP_MANAGER_HOME_DIR'): " test_cmd
            eval "$test_cmd"
            ;;
        exit)
            echo "Goodbye!"
            break
            ;;
        *)
            echo "Unknown command: $command"
            ;;
    esac
done
