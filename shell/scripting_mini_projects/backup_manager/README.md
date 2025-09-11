# Distributed Backup & Sync Manager

A comprehensive backup solution written in Bash that supports local, remote (SSH), and cloud (S3) storage with encryption, compression, and advanced scheduling capabilities.

## Features

- **Multiple Storage Backends**: Local filesystem, SSH/rsync, AWS S3
- **Compression**: Support for gzip, bzip2, xz, or no compression
- **Encryption**: GPG encryption with public key or symmetric encryption
- **Parallel Operations**: Configurable parallel backup jobs
- **Verification**: Backup integrity checking and validation
- **Scheduling**: Cron integration for automated backups
- **Logging**: Comprehensive logging with rotation
- **Configuration**: Flexible configuration system
- **Recovery**: Full restore functionality

## Quick Start

### 1. Installation

```bash
# Clone or download the backup manager
cd /path/to/your/scripts
git clone <repository> backup_manager
cd backup_manager

# Make the main script executable
chmod +x backup_manager.sh
```

### 2. Basic Configuration

Edit `config/settings.conf` to match your environment:

```bash
# Example configuration
DEFAULT_BACKUP_METHOD="local"
DEFAULT_COMPRESSION="gzip"
LOCAL_BACKUP_DIR="/backups"
DEFAULT_RETENTION_DAYS="30"
```

### 3. First Backup

```bash
# Test the system
./backup_manager.sh test

# Create your first backup
./backup_manager.sh backup /home/user /backups/daily

# Check backup status
./backup_manager.sh status
```

## Usage

### Commands

```bash
# Create backups
./backup_manager.sh backup <source> <destination>
./backup_manager.sh backup /home/user /backups/daily
./backup_manager.sh backup /var/www user@server:/backups/
./backup_manager.sh backup /data s3://mybucket/backups/

# Restore from backup
./backup_manager.sh restore <backup_id> <target_path>
./backup_manager.sh restore backup_20231201_143022 /tmp/restore

# List and manage backups
./backup_manager.sh list                    # List all backups
./backup_manager.sh status                  # Show system status
./backup_manager.sh cleanup 30              # Clean backups older than 30 days

# Configuration
./backup_manager.sh config show             # Show current config
./backup_manager.sh config edit             # Edit configuration

# System testing
./backup_manager.sh test                    # Test system requirements
```

### Backup Destinations

#### Local Backups
```bash
./backup_manager.sh backup /source/path /local/backup/path
```

#### SSH/Remote Backups
```bash
./backup_manager.sh backup /source/path user@hostname:/remote/path
```

#### S3 Cloud Backups
```bash
# Configure AWS credentials first
aws configure

# Then backup to S3
./backup_manager.sh backup /source/path s3://bucket-name/path/
```

## Configuration

### Main Configuration File

Edit `config/settings.conf` to customize behavior:

```bash
# Backup settings
DEFAULT_BACKUP_METHOD="local"          # local, ssh, s3, auto
DEFAULT_COMPRESSION="gzip"             # gzip, bzip2, xz, none
DEFAULT_ENCRYPTION="false"             # true/false
DEFAULT_RETENTION_DAYS="30"            # Days to keep backups

# Performance settings
MAX_PARALLEL_JOBS="3"                  # Concurrent backup jobs
BANDWIDTH_LIMIT="0"                    # KB/s, 0 = unlimited

# SSH settings (for remote backups)
SSH_USER="backup"                      # Default SSH user
SSH_KEY_FILE=""                        # Path to SSH key
SSH_TIMEOUT="30"                       # Connection timeout

# S3 settings (for cloud backups)
S3_BUCKET="my-backup-bucket"           # S3 bucket name
S3_REGION="us-east-1"                  # AWS region
S3_STORAGE_CLASS="STANDARD"            # Storage class

# Encryption settings
GPG_KEY_ID=""                          # GPG key for encryption
GPG_CIPHER="AES256"                    # Encryption algorithm
```

### SSH Setup

For remote backups, set up passwordless SSH:

```bash
# Generate SSH key
ssh-keygen -t ed25519 -f ~/.ssh/backup_key

# Copy key to remote server
ssh-copy-id -i ~/.ssh/backup_key user@remote-server

# Update configuration
echo 'SSH_KEY_FILE="$HOME/.ssh/backup_key"' >> config/settings.conf
```

### GPG Encryption Setup

To enable encryption:

```bash
# Generate GPG key pair
./backup_manager.sh config edit
# Set DEFAULT_ENCRYPTION="true"

# Or use the utility to generate keys
gpg --gen-key

# Get your key ID
gpg --list-keys

# Update configuration with your key ID
echo 'GPG_KEY_ID="YOUR_KEY_ID_HERE"' >> config/settings.conf
```

### AWS S3 Setup

For cloud backups:

```bash
# Install AWS CLI
pip install awscli

# Configure AWS credentials
aws configure

# Create S3 bucket
aws s3 mb s3://my-backup-bucket

# Update configuration
echo 'S3_BUCKET="my-backup-bucket"' >> config/settings.conf
```

## Scheduling Automated Backups

Use cron for scheduled backups:

```bash
# Edit crontab
crontab -e

# Add backup jobs
# Daily backup at 2 AM
0 2 * * * /path/to/backup_manager.sh backup /home/user /backups/daily

# Weekly cleanup
0 3 * * 0 /path/to/backup_manager.sh cleanup 30

# Monthly remote backup
0 4 1 * * /path/to/backup_manager.sh backup /important/data user@backup-server:/backups/
```

## Project Structure

```
backup_manager/
├── backup_manager.sh           # Main entry point
├── config/
│   └── settings.conf          # Configuration file
├── core/
│   └── backup_core.sh         # Core backup functionality
├── utils/
│   ├── common_utils.sh        # Common utilities
│   ├── logging_utils.sh       # Logging system
│   ├── validation_utils.sh    # Input validation
│   ├── compression_utils.sh   # Archive handling
│   └── encryption_utils.sh    # Encryption utilities
├── data/
│   ├── local/                 # Local backup storage
│   ├── temp/                  # Temporary files
│   └── backup_log.txt         # Backup metadata
├── logs/                      # Log files
└── tests/                     # Test scripts
```

## Advanced Features

### Backup Verification

All backups are automatically verified by default:

```bash
# Disable verification (not recommended)
echo 'VERIFY_BACKUPS="false"' >> config/settings.conf

# Manual verification
tar -tzf backup_file.tar.gz > /dev/null && echo "OK" || echo "CORRUPTED"
```

### Bandwidth Limiting

For remote backups over slow connections:

```bash
# Limit to 1MB/s
echo 'BANDWIDTH_LIMIT="1024"' >> config/settings.conf
```

### Parallel Backups

Run multiple backup jobs simultaneously:

```bash
# Allow up to 5 parallel jobs
echo 'MAX_PARALLEL_JOBS="5"' >> config/settings.conf
```

## Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   # Check file permissions
   ls -la backup_manager.sh
   chmod +x backup_manager.sh
   ```

2. **SSH Connection Failed**
   ```bash
   # Test SSH connection manually
   ssh -i ~/.ssh/backup_key user@remote-server
   
   # Check SSH configuration
   ./backup_manager.sh test
   ```

3. **GPG Encryption Errors**
   ```bash
   # List available keys
   gpg --list-keys
   
   # Test encryption
   echo "test" | gpg --encrypt --recipient your@email.com
   ```

4. **S3 Access Denied**
   ```bash
   # Check AWS credentials
   aws sts get-caller-identity
   
   # Test S3 access
   aws s3 ls s3://your-bucket/
   ```

### Debug Mode

Enable debug logging:

```bash
echo 'DEBUG_MODE="true"' >> config/settings.conf
./backup_manager.sh backup /source /dest
```

### Log Analysis

Check logs for issues:

```bash
# View recent logs
tail -f logs/backup_manager.log

# Search for errors
grep ERROR logs/backup_manager.log

# View error summary
grep -A 5 -B 5 "FAILED" logs/backup_manager.log
```

## Development and Testing

### Running Tests

```bash
# Test system requirements
./backup_manager.sh test

# Test specific components
cd tests/
./test_backup_core.sh
```

### Contributing

1. Follow the existing code style
2. Add tests for new features
3. Update documentation
4. Test on multiple systems

## Requirements

### System Requirements
- Bash 4.0 or later
- GNU tar
- Standard UNIX utilities (find, awk, sed, etc.)

### Optional Dependencies
- **GPG**: For encryption support
- **SSH/SCP**: For remote backups
- **AWS CLI**: For S3 cloud backups
- **rsync**: For efficient remote transfers
- **pv**: For progress indicators

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in `logs/`
3. Test with `./backup_manager.sh test`
4. Enable debug mode for detailed output
