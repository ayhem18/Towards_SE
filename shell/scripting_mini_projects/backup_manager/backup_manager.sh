#!/bin/bash
#
# Distributed Backup & Sync Manager
# Main entry point for the backup system
#
# Usage: ./backup_manager.sh [command] [options]
# Commands:
#   backup    - Create a new backup
#   restore   - Restore from backup
#   status    - Show backup status
#   config    - Manage configuration
#   cleanup   - Clean old backups
#

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source configuration and utilities
source "$SCRIPT_DIR/config/settings.conf"
source "$SCRIPT_DIR/core/backup_core.sh"
source "$SCRIPT_DIR/utils/common_utils.sh"
source "$SCRIPT_DIR/utils/logging_utils.sh"

# Initialize logging
init_logging

show_usage() {
    cat << EOF
Distributed Backup & Sync Manager

Usage: $0 [command] [options]

Commands:
    backup [source] [destination]  - Create a new backup
    restore [backup_id] [target]   - Restore from backup
    status                         - Show backup status and history
    list                          - List available backups
    config [show|edit]            - Show or edit configuration
    cleanup [days]                - Clean backups older than specified days
    test                          - Test backup system configuration
    help                          - Show this help message

Examples:
    $0 backup /home/user /backups/daily
    $0 backup /home/user s3://mybucket/backups
    $0 restore backup_20231201_143022 /tmp/restore
    $0 cleanup 30

For more information, see the README.md file.
EOF
}

main() {
    local command="${1:-help}"
    
    case "$command" in
        backup)
            shift
            handle_backup "$@"
            ;;
        restore)
            shift
            handle_restore "$@"
            ;;
        status)
            show_backup_status
            ;;
        list)
            list_backups
            ;;
        config)
            shift
            handle_config "$@"
            ;;
        cleanup)
            shift
            handle_cleanup "$@"
            ;;
        test)
            test_system
            ;;
        help|--help|-h)
            show_usage
            ;;
        *)
            echo "Error: Unknown command '$command'" >&2
            echo "Use '$0 help' for usage information." >&2
            exit 1
            ;;
    esac
}

# Trap to ensure cleanup on exit
trap cleanup_on_exit EXIT INT TERM

# Run main function with all arguments
main "$@"
