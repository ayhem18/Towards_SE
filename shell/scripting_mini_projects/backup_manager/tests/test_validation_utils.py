import os
import shutil
import string
import random
import unittest
import tempfile
import subprocess

class TestValidationUtils(unittest.TestCase):
    """
    Test suite for the validation utility functions in validation_utils.sh.
    This test class focuses on testing the individual validation functions:
    - validate_user_name()
    - validate_host()
    - validate_remote_path()
    - validate_remote_components()
    """

    def setUp(self):
        """
        Set up test environment for each test.
        """
        self.test_dir = tempfile.mkdtemp(prefix="validation_utils_tests_")
        
    def tearDown(self):
        """
        Clean up after each test.
        """
        shutil.rmtree(self.test_dir)

    def _run_shell_function(self, function_call: str):
        """
        Helper method to source validation_utils.sh and run a function call.
        Returns the completed subprocess result object.
        """
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'back_man', 'core', 'utils', 'validation_utils.sh'))
        
        # Set up environment and test functions
        test_setup = '''
        # Set up environment variable for testing
        export BACKUP_MANAGER_DEFAULT_REMOTE_HOME_DIR="~"
        
        # Test wrapper for validate_user_name
        test_validate_user_name() {
            local username="$1"
            if validate_user_name "$username"; then
                echo "SUCCESS"
            else
                echo "FAILED"
            fi
        }
        
        # Test wrapper for validate_host
        test_validate_host() {
            local hostname="$1"
            if validate_host "$hostname"; then
                echo "SUCCESS"
            else
                echo "FAILED"
            fi
        }
        
        # Test wrapper for validate_remote_path
        test_validate_remote_path() {
            local input_path="$1"
            local normalized_path
            if validate_remote_path "$input_path" normalized_path; then
                echo "SUCCESS"
                echo "NORMALIZED_PATH:$normalized_path"
            else
                echo "FAILED"
            fi
        }
        
        # Test wrapper for validate_remote_components
        test_validate_remote_components() {
            local username="$1"
            local hostname="$2"
            local input_path="$3"
            local normalized_path
            if validate_remote_components "$username" "$hostname" "$input_path" normalized_path; then
                echo "SUCCESS"
                echo "NORMALIZED_PATH:$normalized_path"
            else
                echo "FAILED"
            fi
        }
        '''
        
        command = f"source {script_path}; {test_setup} {function_call}"
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

        return result

    def _parse_test_output(self, output):
        """
        Parse the test output to extract success status and normalized path if present.
        Returns tuple: (success, normalized_path)
        """
        lines = output.strip().split('\n')
        if not lines or lines[0] not in ["SUCCESS", "FAILED"]:
            return False, None
            
        success = lines[0] == "SUCCESS"
        normalized_path = None
        
        for line in lines[1:]:
            if line.startswith("NORMALIZED_PATH:"):
                normalized_path = line[16:]  # Remove "NORMALIZED_PATH:" prefix
                
        return success, normalized_path

    # ============================================================================
    # USERNAME VALIDATION TESTS
    # ============================================================================

    def test_validate_user_name_valid_usernames(self):
        """Test validate_user_name with valid usernames."""
        valid_usernames = [
            "user",
            "admin",
            "backup",
            "test_user",
            "user123",
            "user-name",
            "user.name",
            "_user",
            "u",  # Single character
            "very_long_username_but_valid",
            "User123",  # Mixed case
            "deploy_2024",
            "backup-daily",
        ]
        
        for username in valid_usernames:
            with self.subTest(username=username):
                result = self._run_shell_function(f'test_validate_user_name "{username}"')
                success, _ = self._parse_test_output(result.stdout)
                self.assertTrue(success, f"Username should be valid: {username}")

    @unittest.skip("skipping for now")
    def test_validate_user_name_invalid_usernames(self):
        """Test validate_user_name with invalid usernames."""
        invalid_usernames = [
            "",  # Empty username
            "123user",  # Starts with number
            "-user",  # Starts with hyphen
            "user-",  # Ends with hyphen (depending on regex)
            "user..name",  # Consecutive dots
            "user--name",  # Consecutive hyphens
            "a" * 33,  # Too long (over 32 chars)
            "user@name",  # Contains @
            "user name",  # Contains space
            "user;name",  # Contains semicolon
            "user$name",  # Contains dollar sign
        ]
        
        for username in invalid_usernames:
            with self.subTest(username=username):
                result = self._run_shell_function(f'test_validate_user_name "{username}"')
                success, _ = self._parse_test_output(result.stdout)
                self.assertFalse(success, f"Username should be invalid: {username}")

    @unittest.skip("skipping for now")
    def test_validate_user_name_edge_cases(self):
        """Test validate_user_name with edge cases."""
        edge_cases = [
            ("a", True),  # Single letter
            ("_", True),  # Single underscore
            ("user1", True),  # Letter + number
            ("1", False),  # Single number
            ("-", False),  # Single hyphen
            (".", False),  # Single dot
            ("a" * 32, True),  # Exactly 32 chars (max length)
        ]
        
        for username, should_be_valid in edge_cases:
            with self.subTest(username=username):
                result = self._run_shell_function(f'test_validate_user_name "{username}"')
                success, _ = self._parse_test_output(result.stdout)
                if should_be_valid:
                    self.assertTrue(success, f"Username should be valid: {username}")
                else:
                    self.assertFalse(success, f"Username should be invalid: {username}")

    # ============================================================================
    # HOSTNAME VALIDATION TESTS
    # ============================================================================
    @unittest.skip("skipping for now")
    def test_validate_host_valid_hostnames(self):
        """Test validate_host with valid hostnames."""
        valid_hostnames = [
            "server",
            "web-01",
            "backup-server",
            "localhost",
            "api.example.com",
            "db.company.org",
            "server123",
            "web01.site99.com",
            "192.168.1.1",  # IP addresses are valid
            "10.0.0.1",
            "127.0.0.1",
            "node-01.cluster.local",
            "very-long-hostname.example.com",
        ]
        
        for hostname in valid_hostnames:
            with self.subTest(hostname=hostname):
                result = self._run_shell_function(f'test_validate_host "{hostname}"')
                success, _ = self._parse_test_output(result.stdout)
                self.assertTrue(success, f"Hostname should be valid: {hostname}")

    @unittest.skip("skipping for now")
    def test_validate_host_invalid_hostnames(self):
        """Test validate_host with invalid hostnames."""
        invalid_hostnames = [
            "",  # Empty hostname
            "::1",  # IPv6 not allowed
            "2001:db8::1",  # IPv6 not allowed
            "server_name",  # Underscores not allowed
            "web_server",  # Underscores not allowed
            "server..com",  # Double dots
            "123",  # Numbers only
            "456",  # Numbers only
            "server with spaces",  # Spaces not allowed
            "server;name",  # Semicolon not allowed
            "server$name",  # Dollar sign not allowed
            "a" * 254,  # Too long (over 253 chars)
        ]
        
        for hostname in invalid_hostnames:
            with self.subTest(hostname=hostname):
                result = self._run_shell_function(f'test_validate_host "{hostname}"')
                success, _ = self._parse_test_output(result.stdout)
                self.assertFalse(success, f"Hostname should be invalid: {hostname}")

    @unittest.skip("skipping for now")
    def test_validate_host_edge_cases(self):
        """Test validate_host with edge cases."""
        edge_cases = [
            ("a", True),  # Single letter
            ("1", False),  # Single number
            ("a.b", True),  # Minimal domain
            ("a" * 253, False),  # Exactly at length limit (might be too long)
            ("localhost", True),  # Common hostname
        ]
        
        for hostname, should_be_valid in edge_cases:
            with self.subTest(hostname=hostname):
                result = self._run_shell_function(f'test_validate_host "{hostname}"')
                success, _ = self._parse_test_output(result.stdout)
                if should_be_valid:
                    self.assertTrue(success, f"Hostname should be valid: {hostname}")
                else:
                    self.assertFalse(success, f"Hostname should be invalid: {hostname}")

    # ============================================================================
    # REMOTE PATH VALIDATION TESTS  
    # ============================================================================

    @unittest.skip("skipping for now")
    def test_validate_remote_path_absolute_paths(self):
        """Test validate_remote_path with absolute paths (should remain unchanged)."""
        test_cases = [
            ("/home/user", "/home/user"),
            ("/var/backups", "/var/backups"),
            ("/opt/data/files", "/opt/data/files"),
            ("/tmp", "/tmp"),
            ("/", "/"),
            ("~/already/home", "~/already/home"),
        ]
        
        for input_path, expected_path in test_cases:
            with self.subTest(input_path=input_path):
                result = self._run_shell_function(f'test_validate_remote_path "{input_path}"')
                success, normalized_path = self._parse_test_output(result.stdout)
                self.assertTrue(success, f"Absolute path should be valid: {input_path}")
                self.assertEqual(normalized_path, expected_path, f"Path should remain unchanged: {input_path}")

    @unittest.skip("skipping for now")
    def test_validate_remote_path_relative_paths(self):
        """Test validate_remote_path with relative paths (should be normalized to absolute)."""
        test_cases = [
            ("backup", "~/backup"),
            ("documents/files", "~/documents/files"),
            ("./relative", "~/relative"),
            ("data", "~/data"),
            ("nested/deep/path", "~/nested/deep/path"),
        ]
        
        for input_path, expected_path in test_cases:
            with self.subTest(input_path=input_path):
                result = self._run_shell_function(f'test_validate_remote_path "{input_path}"')
                success, normalized_path = self._parse_test_output(result.stdout)
                self.assertTrue(success, f"Relative path should be valid: {input_path}")
                self.assertEqual(normalized_path, expected_path, f"Path should be normalized: {input_path}")

    @unittest.skip("skipping for now")
    def test_validate_remote_path_empty_path(self):
        """Test validate_remote_path with empty path (should default to ~)."""
        result = self._run_shell_function('test_validate_remote_path ""')
        success, normalized_path = self._parse_test_output(result.stdout)
        self.assertTrue(success, "Empty path should be valid")
        self.assertEqual(normalized_path, "~", "Empty path should default to ~")

    @unittest.skip("skipping for now")
    def test_validate_remote_path_special_characters(self):
        """Test validate_remote_path with special characters."""
        valid_paths = [
            "/path/with-hyphens",
            "/path/with_underscores", 
            "/path/with.dots",
            "/path with spaces",  # Spaces are allowed
            "/path:with:colons",  # Colons are allowed
            "relative-path",
            "path_with_underscores",
        ]
        
        for path in valid_paths:
            with self.subTest(path=path):
                result = self._run_shell_function(f'test_validate_remote_path "{path}"')
                success, _ = self._parse_test_output(result.stdout)
                self.assertTrue(success, f"Path with special chars should be valid: {path}")

    @unittest.skip("skipping for now")
    def test_validate_remote_path_dangerous_characters(self):
        """Test validate_remote_path with dangerous shell metacharacters (should fail)."""
        dangerous_paths = [
            "/path;rm -rf /",  # Semicolon (command injection)
            "/path|dangerous",  # Pipe
            "/path>file",  # Redirect
            "/path<file",  # Redirect
            "/path$(rm -rf /)",  # Command substitution
            "/path`command`",  # Backtick command substitution
            "/path&background",  # Background process
            "/path*wildcard",  # Wildcard
            "/path?wildcard",  # Wildcard
            "path'quote",  # Single quote
            'path"quote',  # Double quote
        ]
        
        for path in dangerous_paths:
            with self.subTest(path=path):
                result = self._run_shell_function(f'test_validate_remote_path "{path}"')
                success, _ = self._parse_test_output(result.stdout)
                self.assertFalse(success, f"Dangerous path should be invalid: {path}")

    @unittest.skip("skipping for now")
    def test_validate_remote_path_path_traversal(self):
        """Test validate_remote_path with path traversal patterns."""
        # Moderate path traversal should be allowed
        moderate_traversal = [
            "../parent",
            "../../grandparent", 
            "../../../great-grandparent",
            "/path/../other",
        ]
        
        for path in moderate_traversal:
            with self.subTest(path=path):
                result = self._run_shell_function(f'test_validate_remote_path "{path}"')
                success, _ = self._parse_test_output(result.stdout)
                self.assertTrue(success, f"Moderate traversal should be valid: {path}")
        
        # Excessive path traversal should be rejected
        excessive_traversal = [
            "../../../../../../../../etc/passwd",  # Many ../
            "../" * 10 + "deep",  # Many traversals
        ]
        
        for path in excessive_traversal:
            with self.subTest(path=path):
                result = self._run_shell_function(f'test_validate_remote_path "{path}"')
                success, _ = self._parse_test_output(result.stdout)
                self.assertFalse(success, f"Excessive traversal should be invalid: {path}")

    @unittest.skip("skipping for now")
    def test_validate_remote_path_length_limits(self):
        """Test validate_remote_path with various path lengths."""
        # Valid length path
        normal_path = "/home/user/documents/project/file.txt"
        result = self._run_shell_function(f'test_validate_remote_path "{normal_path}"')
        success, _ = self._parse_test_output(result.stdout)
        self.assertTrue(success, "Normal length path should be valid")
        
        # Very long path (should fail)
        very_long_path = "/home/" + "a" * 4100  # Over 4096 chars
        result = self._run_shell_function(f'test_validate_remote_path "{very_long_path}"')
        success, _ = self._parse_test_output(result.stdout)
        self.assertFalse(success, "Very long path should be invalid")
        
        # Long path component (should fail)
        long_component = "/home/" + "a" * 260  # Over 255 chars for single component
        result = self._run_shell_function(f'test_validate_remote_path "{long_component}"')
        success, _ = self._parse_test_output(result.stdout)
        self.assertFalse(success, "Path with long component should be invalid")

    # ============================================================================
    # COMBINED VALIDATION TESTS
    # ============================================================================

    @unittest.skip("skipping for now")
    def test_validate_remote_components_all_valid(self):
        """Test validate_remote_components with all valid components."""
        test_cases = [
            ("user", "server", "/home/backup", "/home/backup"),
            ("admin", "web.example.com", "documents", "~/documents"),
            ("backup", "192.168.1.1", "", "~"),
            ("deploy", "api-server", "./relative", "~/relative"),
        ]
        
        for username, hostname, input_path, expected_path in test_cases:
            with self.subTest(username=username, hostname=hostname, path=input_path):
                result = self._run_shell_function(f'test_validate_remote_components "{username}" "{hostname}" "{input_path}"')
                success, normalized_path = self._parse_test_output(result.stdout)
                self.assertTrue(success, f"All valid components should pass: {username}@{hostname}:{input_path}")
                self.assertEqual(normalized_path, expected_path, "Path should be normalized correctly")

    @unittest.skip("skipping for now")
    def test_validate_remote_components_invalid_username(self):
        """Test validate_remote_components with invalid username."""
        invalid_cases = [
            ("", "server", "/path"),  # Empty username
            ("123user", "server", "/path"),  # Invalid username format
            ("user@invalid", "server", "/path"),  # Username with @
        ]
        
        for username, hostname, path in invalid_cases:
            with self.subTest(username=username):
                result = self._run_shell_function(f'test_validate_remote_components "{username}" "{hostname}" "{path}"')
                success, _ = self._parse_test_output(result.stdout)
                self.assertFalse(success, f"Invalid username should fail: {username}")

    @unittest.skip("skipping for now")
    def test_validate_remote_components_invalid_hostname(self):
        """Test validate_remote_components with invalid hostname."""
        invalid_cases = [
            ("user", "", "/path"),  # Empty hostname
            ("user", "server_name", "/path"),  # Invalid hostname format
            ("user", "::1", "/path"),  # IPv6 not allowed
        ]
        
        for username, hostname, path in invalid_cases:
            with self.subTest(hostname=hostname):
                result = self._run_shell_function(f'test_validate_remote_components "{username}" "{hostname}" "{path}"')
                success, _ = self._parse_test_output(result.stdout)
                self.assertFalse(success, f"Invalid hostname should fail: {hostname}")

    @unittest.skip("skipping for now")
    def test_validate_remote_components_invalid_path(self):
        """Test validate_remote_components with invalid path."""
        invalid_cases = [
            ("user", "server", "/path;rm -rf /"),  # Dangerous path
            ("user", "server", "/path|malicious"),  # Pipe in path
            ("user", "server", "a" * 5000),  # Too long path
        ]
        
        for username, hostname, path in invalid_cases:
            with self.subTest(path=path):
                result = self._run_shell_function(f'test_validate_remote_components "{username}" "{hostname}" "{path}"')
                success, _ = self._parse_test_output(result.stdout)
                self.assertFalse(success, f"Invalid path should fail: {path}")

    @unittest.skip("skipping for now")
    def test_validate_remote_components_multiple_errors(self):
        """Test validate_remote_components with multiple invalid components."""
        # All invalid
        result = self._run_shell_function('test_validate_remote_components "123invalid" "server_bad" "/path;dangerous"')
        success, _ = self._parse_test_output(result.stdout)
        self.assertFalse(success, "Multiple invalid components should fail")

    # ============================================================================
    # RANDOM TESTING
    # ============================================================================
    @unittest.skip("skipping for now")
    def test_validate_functions_random_valid_inputs(self):
        """Test all validation functions with random valid inputs."""
        valid_usernames = ["user", "admin", "backup", "deploy", "test_user", "_service"]
        valid_hostnames = ["server", "web-01", "api.example.com", "192.168.1.1", "localhost"]
        valid_paths = ["/home/user", "/var/data", "documents", "backup/daily", ""]
        
        for _ in range(20):  # Test 20 random combinations
            username = random.choice(valid_usernames)
            hostname = random.choice(valid_hostnames)
            path = random.choice(valid_paths)
            
            with self.subTest(username=username, hostname=hostname, path=path):
                # Test individual functions
                result = self._run_shell_function(f'test_validate_user_name "{username}"')
                success, _ = self._parse_test_output(result.stdout)
                self.assertTrue(success, f"Valid username should pass: {username}")
                
                result = self._run_shell_function(f'test_validate_host "{hostname}"')
                success, _ = self._parse_test_output(result.stdout)
                self.assertTrue(success, f"Valid hostname should pass: {hostname}")
                
                result = self._run_shell_function(f'test_validate_remote_path "{path}"')
                success, _ = self._parse_test_output(result.stdout)
                self.assertTrue(success, f"Valid path should pass: {path}")
                
                # Test combined function
                result = self._run_shell_function(f'test_validate_remote_components "{username}" "{hostname}" "{path}"')
                success, _ = self._parse_test_output(result.stdout)
                self.assertTrue(success, f"All valid components should pass: {username}@{hostname}:{path}")


if __name__ == '__main__':
    unittest.main()
