import os
import shutil
import string
import random
import unittest
import tempfile
import subprocess

class TestFileUtils(unittest.TestCase):
    """
    Test suite for the shell script functions in file_utils.sh.
    This test class calls the shell script functions directly from Python
    using the subprocess module, checking their exit codes and output.
    """

    def setUp(self):
        """
        Set up a temporary environment for each test.
        This runs before every single test method.
        """
        self.test_dir = tempfile.mkdtemp(prefix="file_utils_tests_")
        # Create dummy files and directories for testing
        self.existing_dir = os.path.join(self.test_dir, "existing_dir")
        self.existing_file = os.path.join(self.existing_dir, "file.txt")
        os.makedirs(self.existing_dir)
        with open(self.existing_file, "w") as f:
            f.write("test")

    def tearDown(self):
        """
        Clean up the temporary environment after each test.
        This runs after every single test method.
        """
        shutil.rmtree(self.test_dir)


    def _run_shell_function(self, function_call: str):
        """
        Helper method to source file_utils.sh and run a function call.
        Returns the completed subprocess result object.
        """
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'file_utils.sh'))
        # The command sources the script, then executes the function call
        # inside the temporary test directory to ensure paths are resolved correctly.
        command = f"source {script_path}; {function_call}"
        return subprocess.run(
            ['bash', '-c', command],
            capture_output=True,
            text=True,
            cwd=self.test_dir  # Run the command from inside our temp directory
        )

    def _get_random_valid_extension(self):
        """
        Generate a random valid file extension from a predefined set.
        """
        extensions = [
            'txt', 'py', 'json', 'xml', 'yaml', 'yml', 'csv', 'log',
            'jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg',
            'mp3', 'wav', 'ogg', 'flac', 'mp4', 'avi', 'mkv', 'mov',
            'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
            'zip', 'tar', 'gz', 'rar', '7z', 'bz2',
            'exe', 'dmg', 'pkg', 'deb', 'rpm',
            'html', 'css', 'js', 'ts', 'php', 'cpp', 'c', 'h',
            'sh', 'bat', 'ps1', 'sql', 'conf', 'ini', 'cfg'
        ]
        return random.choice(extensions)
    
    def _get_random_filename_base(self, length=None):
        """
        Generate a random filename base (without extension).
        """
        if length is None:
            length = random.randint(3, 15)
        return ''.join(random.choices(string.ascii_letters + string.digits + '_-', k=length))
    
    def _generate_random_filename_with_extension(self):
        """
        Generate a random filename with a valid extension.
        Returns tuple: (filename, expected_extension)
        """
        base = self._get_random_filename_base()
        ext = self._get_random_valid_extension()
        return f"{base}.{ext}", ext
    
    def _generate_random_filename_multiple_dots(self):
        """
        Generate a random filename with multiple dots.
        Returns tuple: (filename, expected_extension)
        """
        # Generate 2-4 parts separated by dots
        num_parts = random.randint(2, 4)
        parts = []
        for i in range(num_parts - 1):
            parts.append(self._get_random_filename_base(length=random.randint(3, 8)))
        
        # Last part is the extension
        extension = self._get_random_valid_extension()
        parts.append(extension)
        
        filename = '.'.join(parts)
        return filename, extension



    # --- Tests for is_file ---
    # @unittest.skip("skip for now")
    def test_is_file_existing_files(self):
        """Test is_file with multiple existing files."""
        for i in range(20):
            with self.subTest(iteration=i):
                # Create a random file
                filename, _ = self._generate_random_filename_with_extension()
                filepath = os.path.join(self.existing_dir, filename)
                with open(filepath, 'w') as f:
                    f.write("test content")
                
                result = self._run_shell_function(f'is_file "{filepath}"')
                self.assertEqual(result.returncode, 0, 
                    f"is_file should return true for existing file: {filename}")

    # @unittest.skip("skip for now")
    def test_is_file_existing_directories(self):
        """Test is_file with multiple existing directories."""
        for i in range(10):
            with self.subTest(iteration=i):
                # Create a random directory
                dirname = self._get_random_filename_base()
                dirpath = os.path.join(self.existing_dir, dirname)
                os.makedirs(dirpath)
                
                result = self._run_shell_function(f'is_file "{dirpath}"')
                self.assertNotEqual(result.returncode, 0, 
                    f"is_file should return false for existing directory: {dirname}")

    # @unittest.skip("skip for now")
    def test_is_file_non_existent_file_paths(self):
        """Test is_file with multiple non-existent file paths."""
        for i in range(15):
            with self.subTest(iteration=i):
                # Generate a random filename that doesn't exist
                filename, _ = self._generate_random_filename_with_extension()
                filepath = os.path.join(self.existing_dir, filename)
                
                result = self._run_shell_function(f'is_file "{filepath}"')
                self.assertEqual(result.returncode, 0, 
                    f"is_file should return true for non-existent file path: {filename}")
    
    # @unittest.skip("skip for now")
    def test_is_file_non_existent_directory_paths(self):
        """Test is_file with multiple non-existent directory paths."""
        for i in range(10):
            with self.subTest(iteration=i):
                # Generate a random directory name with trailing slash
                dirname = self._get_random_filename_base()
                dirpath = os.path.join(self.existing_dir, dirname + "/")
                
                result = self._run_shell_function(f'is_file "{dirpath}"')
                self.assertNotEqual(result.returncode, 0, 
                    f"is_file should return false for non-existent directory path: {dirname}/")

    # --- Tests for is_directory ---
    @unittest.skip("skip for now")
    def test_is_directory_existing_directories(self):
        """Test is_directory with multiple existing directories."""
        for i in range(15):
            with self.subTest(iteration=i):
                # Create a random directory
                dirname = self._get_random_filename_base()
                dirpath = os.path.join(self.existing_dir, dirname)
                os.makedirs(dirpath)
                
                result = self._run_shell_function(f'is_directory "{dirpath}"')
                self.assertEqual(result.returncode, 0, 
                    f"is_directory should return true for existing directory: {dirname}")

    # @unittest.skip("skip for now")
    def test_is_directory_existing_files(self):
        """Test is_directory with multiple existing files."""
        for i in range(15):
            with self.subTest(iteration=i):
                # Create a random file
                filename, _ = self._generate_random_filename_with_extension()
                filepath = os.path.join(self.existing_dir, filename)
                with open(filepath, 'w') as f:
                    f.write("test")
                
                result = self._run_shell_function(f'is_directory "{filepath}"')
                self.assertNotEqual(result.returncode, 0, 
                    f"is_directory should return false for existing file: {filename}")

    # @unittest.skip("skip for now")
    def test_is_directory_non_existent_paths_with_slash(self):
        """Test is_directory with multiple non-existent paths ending in slash."""
        for i in range(10):
            with self.subTest(iteration=i):
                # Generate a random directory name with trailing slash
                dirname = self._get_random_filename_base()
                dirpath = os.path.join(self.existing_dir, dirname + "/")
                
                result = self._run_shell_function(f'is_directory "{dirpath}"')
                self.assertEqual(result.returncode, 0, 
                    f"is_directory should return true for non-existent path with slash: {dirname}/")

    # @unittest.skip("skip for now")
    def test_is_directory_non_existent_paths_without_slash(self):
        """Test is_directory with multiple non-existent paths without slash."""
        for i in range(10):
            with self.subTest(iteration=i):
                # Generate a random name without slash
                name = self._get_random_filename_base()
                path = os.path.join(self.existing_dir, name)
                
                result = self._run_shell_function(f'is_directory "{path}"')
                self.assertNotEqual(result.returncode, 0, 
                    f"is_directory should return false for non-existent path without slash: {name}")

    # --- Tests for get_file_extension ---
    
    # @unittest.skip("skip for now")
    def test_get_file_extension_simple_files(self):
        """Test get_file_extension with random files having valid extensions."""
        # Test with various edge cases first
        edge_cases = [
            ("myfile", ""),  # No extension
            (".bashrc", ""),  # Hidden file, no extension
            (".config.yaml", "yaml"),  # Hidden file with extension
            ("", ""),  # Empty string
            ("file.", ""),  # Ends with dot but no extension
        ]
        
        for filename, expected_ext in edge_cases:
            with self.subTest(filename=filename):
                result = self._run_shell_function(f'get_file_extension "{filename}"')
                self.assertEqual(result.stdout.strip(), expected_ext,
                    f"Failed for edge case: '{filename}'")
        
        # Test with 50 random valid files
        for i in range(50):
            with self.subTest(iteration=i):
                filename, expected_ext = self._generate_random_filename_with_extension()
                result = self._run_shell_function(f'get_file_extension "{filename}"')
                self.assertEqual(result.stdout.strip(), expected_ext,
                    f"Failed for random file: '{filename}' (expected: '{expected_ext}')")

    @unittest.skip("skip for now")
    def test_get_file_extension_multiple_dots(self):
        """Test get_file_extension with random files containing multiple dots."""
        # Test some known multi-dot cases first
        known_cases = [
            ("archive.tar.gz", "gz"),
            ("backup.sql.bz2", "bz2"),
            ("config.yaml.backup", "backup"),
            ("my.file.name.txt", "txt"),
            ("version.1.2.3.json", "json"),
        ]
        
        for filename, expected_ext in known_cases:
            with self.subTest(filename=filename):
                result = self._run_shell_function(f'get_file_extension "{filename}"')
                self.assertEqual(result.stdout.strip(), expected_ext,
                    f"Failed for known multi-dot case: '{filename}'")
        
        # Test with 30 random multi-dot files
        for i in range(30):
            with self.subTest(iteration=i):
                filename, expected_ext = self._generate_random_filename_multiple_dots()
                result = self._run_shell_function(f'get_file_extension "{filename}"')
                self.assertEqual(result.stdout.strip(), expected_ext,
                    f"Failed for random multi-dot file: '{filename}' (expected: '{expected_ext}')")


if __name__ == '__main__':
    unittest.main()