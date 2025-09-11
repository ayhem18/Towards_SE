import os
import shutil
import string
import random
import unittest
import tempfile
import subprocess

class TestParsingUtils(unittest.TestCase):
    """
    Test suite for the parsing utility functions in parsing_utils.sh.
    This test class focuses on testing the parse_remote_path function
    which needs to handle various hostname, username, and path combinations.
    """

    def setUp(self):
        """
        Set up test environment for each test.
        """
        self.test_dir = tempfile.mkdtemp(prefix="parsing_utils_tests_")
        
    def tearDown(self):
        """
        Clean up after each test.
        """
        shutil.rmtree(self.test_dir)

    def _run_shell_function(self, function_call: str):
        """
        Helper method to source parsing_utils.sh and run a function call.
        Returns the completed subprocess result object.
        """
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'back_man', 'core', 'utils', 'parsing_utils.sh'))
        # Test function that calls parse_remote_path and outputs the results
        test_function = '''
        # Set up environment variable for testing
        export BACKUP_MANAGER_DEFAULT_REMOTE_HOME_DIR="~"
        
        test_parse_remote_path() {
            local remote_path="$1"
            local hostname username remote_dir
            
            if parse_remote_path "$remote_path" hostname username remote_dir; then
                echo "SUCCESS"
                echo "HOSTNAME:$hostname"
                echo "USERNAME:$username"
                echo "REMOTE_DIR:$remote_dir"
            else
                echo "FAILED"
            fi
        }
        '''
        command = f"source {script_path}; {test_function} \n {function_call}"
        result = subprocess.run(
            ['bash', '-c', command],
            capture_output=True,
            text=True,
            cwd=self.test_dir
        )

        if result.returncode != 0 or result.stderr:
            print(f"Command failed with return code {result.returncode}")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            print(f"Command: {command}")
            print(f"Working directory: {self.test_dir}")
            print(f"Script path: {script_path}")
            print(f"Script exists: {os.path.exists(script_path)}")

        return result

    def _parse_test_output(self, output):
        """
        Parse the test output to extract hostname, username, and remote_dir.
        Returns tuple: (success, hostname, username, remote_dir)
        """
        lines = output.strip().split('\n')
        if not lines or lines[0] != "SUCCESS":
            return False, None, None, None
            
        hostname = username = remote_dir = None
        for line in lines[1:]:
            if line.startswith("HOSTNAME:"):
                hostname = line[9:]  # Remove "HOSTNAME:" prefix
            elif line.startswith("USERNAME:"):
                username = line[9:]  # Remove "USERNAME:" prefix
            elif line.startswith("REMOTE_DIR:"):
                remote_dir = line[11:]  # Remove "REMOTE_DIR:" prefix
                
        return True, hostname, username, remote_dir

    def _get_valid_hostname(self):
        """Generate a valid hostname for testing (matching the regex)."""
        valid_hostnames = [
            "server1",
            "backup-server", 
            "web01.example.com",
            "db.company.org",
            "localhost",
            "ubuntu-server",
            "node-01.cluster.local",
            "web-server",
            "api",
            "database-01",
            # IP addresses are also valid according to the regex
            "192.168.1.100",
            "10.0.0.1",
            "127.0.0.1"
        ]
        return random.choice(valid_hostnames)
    
    def _get_invalid_hostname(self):
        """Generate invalid hostnames that should fail regex validation."""
        invalid_hostnames = [
            "::1",            # IPv6 not allowed
            "2001:db8::1",    # IPv6 not allowed
            "server_with_underscores",  # Underscores not allowed
            "server..com",    # Double dots not allowed
            "123",            # Numbers only not allowed
            "",               # Empty hostname
            "server with spaces",  # Spaces not allowed
            "web_server",     # Underscores not allowed
        ]
        return random.choice(invalid_hostnames)

    def _get_valid_username(self):
        """Generate a valid username for testing."""
        valid_usernames = [
            "user",
            "admin",
            "backup",
            "deploy",
            "ubuntu",
            "root",
            "jenkins",
            "postgres",
            "nginx"
        ]
        return random.choice(valid_usernames)

    def _get_valid_path(self):
        """Generate a valid remote path for testing."""
        valid_paths = [
            "/home/user",
            "/var/backups",
            "/tmp",
            "/opt/data",
            "/home/user/documents",
            "/srv/backup/daily",
            "/mnt/storage/files",
            "~/backups",
            "relative/path"
        ]
        return random.choice(valid_paths)

    # --- Test valid remote path formats ---
    
    def test_parse_remote_path_standard_format(self):
        """Test parsing standard user@hostname:/path format with absolute paths."""
        test_cases = [
            ("user@server:/home/backup", "server", "user", "/home/backup"),
            ("admin@192.168.1.1:/var/data", "192.168.1.1", "admin", "/var/data"),
            ("deploy@web.example.com:/opt/files", "web.example.com", "deploy", "/opt/files"),
            ("root@localhost:/tmp", "localhost", "root", "/tmp"),
        ]
        
        for remote_path, expected_host, expected_user, expected_dir in test_cases:
            with self.subTest(remote_path=remote_path):
                result = self._run_shell_function(f'test_parse_remote_path "{remote_path}"')
                success, hostname, username, remote_dir = self._parse_test_output(result.stdout)
                
                self.assertTrue(success, f"Parsing should succeed for: {remote_path}")
                self.assertEqual(hostname, expected_host)
                self.assertEqual(username, expected_user)
                self.assertEqual(remote_dir, expected_dir)

    def test_parse_remote_path_relative_to_absolute(self):
        """Test parsing relative paths that should be converted to absolute paths."""
        test_cases = [
            ("user@server:backup", "server", "user", "~/backup"),
            ("admin@server:documents/files", "server", "admin", "~/documents/files"),
            ("user@server:./relative", "server", "user", "~/relative"),
            ("user@server:", "server", "user", "~"),  # Empty path
        ]
        
        for remote_path, expected_host, expected_user, expected_dir in test_cases:
            with self.subTest(remote_path=remote_path):
                result = self._run_shell_function(f'test_parse_remote_path "{remote_path}"')
                success, hostname, username, remote_dir = self._parse_test_output(result.stdout)
                
                self.assertTrue(success, f"Parsing should succeed for: {remote_path}")
                self.assertEqual(hostname, expected_host)
                self.assertEqual(username, expected_user)
                self.assertEqual(remote_dir, expected_dir)

    def test_parse_remote_path_no_username_should_fail(self):
        """Test that parsing hostname:/path format fails (username now required)."""
        test_cases = [
            "server:/home/backup",
            "web.example.com:/opt/files", 
            "backup-server:/tmp",
        ]
        
        for remote_path in test_cases:
            with self.subTest(remote_path=remote_path):
                result = self._run_shell_function(f'test_parse_remote_path "{remote_path}"')
                success, _, _, _ = self._parse_test_output(result.stdout)
                
                self.assertFalse(success, f"Parsing should fail for path without username: {remote_path}")

    def test_parse_remote_path_random_valid_combinations(self):
        """Test parsing with 50 random valid combinations."""
        for i in range(50):
            with self.subTest(iteration=i):
                hostname = self._get_valid_hostname()
                username = self._get_valid_username()
                path = self._get_valid_path()
                
                # Only test with username (now required)
                remote_path = f"{username}@{hostname}:{path}"
                expected_user = username
                
                # Determine expected normalized path
                if path.startswith('/'):
                    expected_path = path  # Already absolute
                else:
                    expected_path = f"~/{path}" if path else "~"
                
                result = self._run_shell_function(f'test_parse_remote_path "{remote_path}"')
                success, parsed_hostname, parsed_username, parsed_dir = self._parse_test_output(result.stdout)
                
                self.assertTrue(success, f"Parsing should succeed for: {remote_path}")
                self.assertEqual(parsed_hostname, hostname)
                self.assertEqual(parsed_dir, expected_path)
                self.assertEqual(parsed_username, expected_user)

    # --- Test edge cases and tricky scenarios ---
    
    def test_parse_remote_path_valid_hostnames(self):
        """Test parsing with valid hostnames that match our regex."""
        valid_cases = [
            # Hostnames with numbers
            ("user@server123:/path", "server123", "user", "/path"),
            ("user@web01.site99.com:/path", "web01.site99.com", "user", "/path"),
            
            # Hostnames with hyphens
            ("user@backup-server:/path", "backup-server", "user", "/path"),
            ("user@multi-word-hostname:/path", "multi-word-hostname", "user", "/path"),
            
            # Domain names
            ("user@api.example.com:/path", "api.example.com", "user", "/path"),
            ("user@db.company.org:/path", "db.company.org", "user", "/path"),
            
            # Simple hostnames
            ("user@localhost:/path", "localhost", "user", "/path"),
            ("user@server:/path", "server", "user", "/path"),
            
            # IP addresses (valid according to regex)
            ("user@192.168.1.1:/path", "192.168.1.1", "user", "/path"),
            ("user@10.0.0.1:/path", "10.0.0.1", "user", "/path"),
        ]
        
        for remote_path, expected_host, expected_user, expected_dir in valid_cases:
            with self.subTest(remote_path=remote_path):
                result = self._run_shell_function(f'test_parse_remote_path "{remote_path}"')
                success, hostname, username, remote_dir = self._parse_test_output(result.stdout)
                
                self.assertTrue(success, f"Parsing should succeed for valid hostname: {remote_path}")
                self.assertEqual(hostname, expected_host)
                self.assertEqual(username, expected_user)
                self.assertEqual(remote_dir, expected_dir)

    def test_parse_remote_path_invalid_hostnames(self):
        """Test parsing with invalid hostnames that should fail regex validation."""
        invalid_cases = [
            # IPv6 addresses (not allowed by our regex)
            "user@::1:/path",
            "user@2001:db8::1:/path",
            
            # Invalid characters
            "user@server_name:/path",  # Underscores not allowed
            "user@web_server:/path",   # Underscores not allowed
            "user@server..com:/path",  # Double dots
            
            # Numbers only
            "user@123:/path",          # Numbers only not allowed
            "user@456:/path",
            
            # Other invalid formats
            "user@ :/path",            # Spaces
            "user@:/path",             # Empty hostname
        ]
        
        for remote_path in invalid_cases:
            with self.subTest(remote_path=remote_path):
                result = self._run_shell_function(f'test_parse_remote_path "{remote_path}"')
                success, _, _, _ = self._parse_test_output(result.stdout)
                
                self.assertFalse(success, f"Parsing should fail for invalid hostname: {remote_path}")

    def test_parse_remote_path_tricky_usernames(self):
        """Test parsing with tricky but valid usernames."""
        tricky_cases = [
            # Usernames with numbers
            ("user123@server:/path", "server", "user123", "/path"),
            ("admin2@server:/path", "server", "admin2", "/path"),
            
            # Usernames with special characters (common ones)
            ("user-name@server:/path", "server", "user-name", "/path"),
            ("user_name@server:/path", "server", "user_name", "/path"),
            ("user.name@server:/path", "server", "user.name", "/path"),
        ]
        
        for remote_path, expected_host, expected_user, expected_dir in tricky_cases:
            with self.subTest(remote_path=remote_path):
                result = self._run_shell_function(f'test_parse_remote_path "{remote_path}"')
                success, hostname, username, remote_dir = self._parse_test_output(result.stdout)
                
                self.assertTrue(success, f"Parsing should succeed for tricky username: {remote_path}")
                self.assertEqual(hostname, expected_host)
                self.assertEqual(username, expected_user)
                self.assertEqual(remote_dir, expected_dir)

    def test_parse_remote_path_tricky_paths(self):
        """Test parsing with tricky but valid paths."""
        tricky_cases = [
            # Paths with spaces (though this might cause issues in practice)
            ('user@server:/path with spaces', "server", "user", "/path with spaces"),
            
            # Paths with special characters (absolute)
            ("user@server:/path/with-hyphens", "server", "user", "/path/with-hyphens"),
            ("user@server:/path/with_underscores", "server", "user", "/path/with_underscores"),
            ("user@server:/path/with.dots", "server", "user", "/path/with.dots"),
            
            # Relative paths (should be normalized to absolute)
            ("user@server:relative/path", "server", "user", "~/relative/path"),
            ("user@server:documents", "server", "user", "~/documents"),
            
            # Home directory path (already absolute)
            ("user@server:~/home/path", "server", "user", "~/home/path"),
            
            # Empty path (should default to ~)
            ("user@server:", "server", "user", "~"),
        ]
        
        for remote_path, expected_host, expected_user, expected_dir in tricky_cases:
            with self.subTest(remote_path=remote_path):
                result = self._run_shell_function(f'test_parse_remote_path "{remote_path}"')
                success, hostname, username, remote_dir = self._parse_test_output(result.stdout)
                
                self.assertTrue(success, f"Parsing should succeed for tricky path: {remote_path}")
                self.assertEqual(hostname, expected_host)
                self.assertEqual(username, expected_user)
                self.assertEqual(remote_dir, expected_dir)

    # --- Test invalid formats that should fail ---
    
    # @unittest.skip("Skipping invalid formats test as it is not required")
    def test_parse_remote_path_invalid_formats(self):
        """Test parsing with invalid formats that should fail."""
        invalid_cases = [
            # No colon (not a remote path)
            "just-a-local-path",
            "/local/absolute/path", 
            "relative/local/path",
            
            # No username (now required)
            "server:/path",
            "example.com:/path",
            
            # Multiple @ symbols
            "user@@server:/path",
            "user@server@backup:/path",
            
            # Empty components
            "@server:/path",  # No username
            "user@:/path",    # No hostname
            
            # Just colon
            ":",
            
            # Colon at start
            ":path",
            
            # Multiple colons (though this might be valid for IPv6)
            "user@server:path:extra",
        ]
        
        for invalid_path in invalid_cases:
            with self.subTest(invalid_path=invalid_path):
                result = self._run_shell_function(f'test_parse_remote_path "{invalid_path}"')
                success, _, _, _ = self._parse_test_output(result.stdout)
                
                self.assertFalse(success, f"Parsing should fail for invalid format: {invalid_path}")

    def test_parse_remote_path_edge_cases(self):
        """Test parsing with extreme edge cases that should still work."""
        edge_cases = [
            # Single character components (absolute path)
            ("a@b:/c", "b", "a", "/c"),
            
            # Single character components (relative path)
            ("a@b:c", "b", "a", "~/c"),
            
            # Long but valid hostnames
            ("user@very-long-hostname.example.com:/path", "very-long-hostname.example.com", "user", "/path"),
            
            # Relative path with dot prefix
            ("user@server:./documents", "server", "user", "~/documents"),
        ]
        
        for remote_path, expected_host, expected_user, expected_dir in edge_cases:
            with self.subTest(remote_path=remote_path):
                result = self._run_shell_function(f'test_parse_remote_path "{remote_path}"')
                success, hostname, username, remote_dir = self._parse_test_output(result.stdout)
                
                self.assertTrue(success, f"Parsing should succeed for edge case: {remote_path}")
                self.assertEqual(hostname, expected_host)
                self.assertEqual(username, expected_user)
                self.assertEqual(remote_dir, expected_dir)


if __name__ == '__main__':
    unittest.main()
