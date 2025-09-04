from math import exp
import os
from re import A
import shutil
import random
import string
import unittest
import tempfile
import subprocess

@unittest.skip("skip for now")
class TestGetDestinationFolder(unittest.TestCase):
    """
    Test suite for the shell script functions in file_analyzer_utils.sh.
    This test class calls the shell script functions directly from Python
    using the subprocess module, checking their exit codes and output.
    """

    def setUp(self):
        """
        Set up a temporary environment for each test.
        This runs before every single test method.
        """
        self.test_dir = tempfile.mkdtemp(prefix="file_analyzer_tests_")
        # Create dummy files and directories for testing
        self.existing_dir = os.path.join(self.test_dir, "existing_dir")
        os.makedirs(self.existing_dir)

    def tearDown(self):
        """
        Clean up the temporary environment after each test.
        This runs after every single test method.
        """
        shutil.rmtree(self.test_dir)

    def _run_shell_function(self, function_call: str):
        """
        Helper method to source file_analyzer.sh and run a function call.
        Returns the completed subprocess result object.
        """
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'file_analyzer_utils.sh'))
        # The command sources the script, then executes the function call
        # inside the temporary test directory to ensure paths are resolved correctly.
        command = f"source {script_path}; {function_call}"
        return subprocess.run(
            ['bash', '-c', command],
            capture_output=True,
            text=True,
            cwd=self.test_dir  # Run the command from inside our temp directory
        )

    # --- Tests for get_destination_folder_name ---
    
    def test_get_destination_folder_name_text_files(self):
        """Test get_destination_folder_name for text file extensions."""
        text_extensions = ["txt"]
        for ext in text_extensions:
            with self.subTest(extension=ext):
                result = self._run_shell_function(f'get_destination_folder_name "{ext}"')
                self.assertEqual(result.stdout.strip(), "text_files",
                    f"Extension '{ext}' should map to 'text_files'")

    def test_get_destination_folder_name_images(self):
        """Test get_destination_folder_name for image file extensions."""
        image_extensions = ["jpg", "jpeg", "png", "gif"]
        for ext in image_extensions:
            with self.subTest(extension=ext):
                result = self._run_shell_function(f'get_destination_folder_name "{ext}"')
                self.assertEqual(result.stdout.strip(), "images",
                    f"Extension '{ext}' should map to 'images'")

    def test_get_destination_folder_name_audio(self):
        """Test get_destination_folder_name for audio file extensions."""
        audio_extensions = ["mp3", "wav", "ogg"]
        for ext in audio_extensions:
            with self.subTest(extension=ext):
                result = self._run_shell_function(f'get_destination_folder_name "{ext}"')
                self.assertEqual(result.stdout.strip(), "audio",
                    f"Extension '{ext}' should map to 'audio'")

    def test_get_destination_folder_name_videos(self):
        """Test get_destination_folder_name for video file extensions."""
        video_extensions = ["mp4", "avi", "mkv"]
        for ext in video_extensions:
            with self.subTest(extension=ext):
                result = self._run_shell_function(f'get_destination_folder_name "{ext}"')
                self.assertEqual(result.stdout.strip(), "videos",
                    f"Extension '{ext}' should map to 'videos'")

    def test_get_destination_folder_name_documents(self):
        """Test get_destination_folder_name for document file extensions."""
        document_extensions = ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx"]
        for ext in document_extensions:
            with self.subTest(extension=ext):
                result = self._run_shell_function(f'get_destination_folder_name "{ext}"')
                self.assertEqual(result.stdout.strip(), "documents",
                    f"Extension '{ext}' should map to 'documents'")

    def test_get_destination_folder_name_archives(self):
        """Test get_destination_folder_name for archive file extensions."""
        archive_extensions = ["zip", "rar", "7z"]
        for ext in archive_extensions:
            with self.subTest(extension=ext):
                result = self._run_shell_function(f'get_destination_folder_name "{ext}"')
                self.assertEqual(result.stdout.strip(), "archives",
                    f"Extension '{ext}' should map to 'archives'")

    def test_get_destination_folder_name_executables(self):
        """Test get_destination_folder_name for executable file extensions."""
        executable_extensions = ["exe", "dmg", "pkg"]
        for ext in executable_extensions:
            with self.subTest(extension=ext):
                result = self._run_shell_function(f'get_destination_folder_name "{ext}"')
                self.assertEqual(result.stdout.strip(), "executables",
                    f"Extension '{ext}' should map to 'executables'")

    def test_get_destination_folder_name_other(self):
        """Test get_destination_folder_name for unknown/other file extensions."""
        # Test some known "other" extensions
        other_extensions = ["xyz", "unknown", "custom", "weird", "123"]
        for ext in other_extensions:
            with self.subTest(extension=ext):
                result = self._run_shell_function(f'get_destination_folder_name "{ext}"')
                self.assertEqual(result.stdout.strip(), "other",
                    f"Extension '{ext}' should map to 'other'")

    def test_get_destination_folder_name_randomized_other(self):
        """Test get_destination_folder_name with random unknown extensions."""
        for i in range(20):
            # Generate a random extension that's not in any known category
            random_ext = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(2, 5)))
            # Make sure it's not accidentally a known extension
            known_extensions = {
                "txt", "jpg", "jpeg", "png", "gif", "mp3", "wav", "ogg",
                "mp4", "avi", "mkv", "pdf", "doc", "docx", "xls", "xlsx",
                "ppt", "pptx", "zip", "rar", "7z", "exe", "dmg", "pkg"
            }
            if random_ext not in known_extensions:
                with self.subTest(iteration=i, extension=random_ext):
                    result = self._run_shell_function(f'get_destination_folder_name "{random_ext}"')
                    self.assertEqual(result.stdout.strip(), "other",
                        f"Random extension '{random_ext}' should map to 'other'")

    def test_get_destination_folder_name_edge_cases(self):
        """Test get_destination_folder_name with edge cases."""
        edge_cases = [
            ("", "other"),  # Empty extension
            ("TXT", "other"),  # Uppercase (case sensitive)
            ("Jpg", "other"),  # Mixed case
            ("txt ", "other"),  # Extension with trailing space
            (" txt", "other"),  # Extension with leading space
        ]
        
        for ext, expected_folder in edge_cases:
            with self.subTest(extension=repr(ext)):
                result = self._run_shell_function(f'get_destination_folder_name "{ext}"')
                self.assertEqual(result.stdout.strip(), expected_folder,
                    f"Edge case extension {repr(ext)} should map to '{expected_folder}'")

    def test_get_destination_folder_name_comprehensive_mapping(self):
        """Test comprehensive mapping of all known extensions to verify completeness."""
        # Define the complete mapping
        extension_mapping = {
            # Text files
            "txt": "text_files",
            
            # Images
            "jpg": "images", "jpeg": "images", "png": "images", "gif": "images",
            
            # Audio
            "mp3": "audio", "wav": "audio", "ogg": "audio",
            
            # Videos
            "mp4": "videos", "avi": "videos", "mkv": "videos",
            
            # Documents
            "pdf": "documents", "doc": "documents", "docx": "documents",
            "xls": "documents", "xlsx": "documents", "ppt": "documents", "pptx": "documents",
            
            # Archives
            "zip": "archives", "rar": "archives", "7z": "archives",
            
            # Executables
            "exe": "executables", "dmg": "executables", "pkg": "executables",
        }
        
        for ext, expected_folder in extension_mapping.items():
            with self.subTest(extension=ext):
                result = self._run_shell_function(f'get_destination_folder_name "{ext}"')
                self.assertEqual(result.stdout.strip(), expected_folder,
                    f"Extension '{ext}' should map to '{expected_folder}'")


# @unittest.skip("skip for now")
class TestMigrateDirectory(unittest.TestCase):
    """
    Test suite for the migrate_directory function in file_analyzer_utils.sh.
    Tests various directory structures and file organization scenarios.
    """

    def setUp(self):
        """
        Set up a temporary environment for each test.
        This runs before every single test method.
        """     
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_dir = os.path.join(script_dir, "test_dir")
        self.source_dir = os.path.join(self.test_dir, "source")
        self.destination_dir = os.path.join(self.test_dir, "destination")
        
        # Create directories
        os.makedirs(self.source_dir, exist_ok=True)
        os.makedirs(self.destination_dir, exist_ok=True)
        
        # Grant all permissions (read, write, execute) to all users
        # 0o777 = rwxrwxrwx (owner, group, others all have full permissions)
        os.chmod(self.test_dir, 0o777)
        os.chmod(self.source_dir, 0o777)
        os.chmod(self.destination_dir, 0o777)

    def tearDown(self):
        """
        Clean up the temporary environment after each test.
        This runs after every single test method.
        """
        shutil.rmtree(self.test_dir)

    def _run_shell_function(self, function_call: str):
        """
        Helper method to source file_analyzer_utils.sh and run a function call.
        Returns the completed subprocess result object.
        """
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'file_analyzer_utils.sh'))
        command = f"source {script_path}; {function_call}"
        
        # Enhanced subprocess execution with better error handling
        result = subprocess.run(
            ['bash', '-c', command],
            capture_output=True,
            text=True,
            cwd=self.test_dir
        )
        
        # Debug output
        if result.returncode != 0 or result.stderr:
            print(f"Command failed with return code {result.returncode}")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            print(f"Command: {command}")
            print(f"Working directory: {self.test_dir}")
            print(f"Script path: {script_path}")
            print(f"Script exists: {os.path.exists(script_path)}")
        
        # Check if file_utils.sh exists in the same directory as file_analyzer_utils.sh
        utils_path = os.path.join(os.path.dirname(script_path), 'file_utils.sh')
        print(f"file_utils.sh path: {utils_path}")
        print(f"file_utils.sh exists: {os.path.exists(utils_path)}")
    
        return result

    def _create_test_file(self, filepath, content="test content"):
        """Helper method to create a test file."""
        # Create parent directories if they don't exist
        parent_dir = os.path.dirname(filepath)
        os.makedirs(parent_dir, exist_ok=True)
        
        # Grant full permissions to the parent directory
        os.chmod(parent_dir, 0o777)
        
        # Create the file
        with open(filepath, 'w') as f:
            f.write(content)
        
        # Grant read/write permissions to the file
        os.chmod(filepath, 0o666)

    def _get_expected_folder_for_extension(self, extension):
        """Helper method to get expected destination folder for an extension."""
        mapping = {
            'txt': 'text_files',
            'jpg': 'images', 'jpeg': 'images', 'png': 'images', 'gif': 'images',
            'mp3': 'audio', 'wav': 'audio', 'ogg': 'audio',
            'mp4': 'videos', 'avi': 'videos', 'mkv': 'videos',
            'pdf': 'documents', 'doc': 'documents', 'docx': 'documents',
            'xls': 'documents', 'xlsx': 'documents', 'ppt': 'documents', 'pptx': 'documents',
            'zip': 'archives', 'rar': 'archives', '7z': 'archives',
            'exe': 'executables', 'dmg': 'executables', 'pkg': 'executables',
        }
        return mapping.get(extension, 'other')

    def _assert_file_migrated_correctly(self, 
                                        original_filename: str, 
                                        expected_parent_dir: str):
        """Helper method to assert a file was migrated to the correct folder with the correct name."""
        expected_path = os.path.join(expected_parent_dir, original_filename)
        self.assertTrue(os.path.exists(expected_path), 
                       f"File '{original_filename}' should exist in {expected_parent_dir}/{original_filename}")
        
        # Verify the content is preserved
        with open(expected_path, 'r') as f:
            content = f.read()
        self.assertIn("test content", content, 
                     f"File content should be preserved for '{original_filename}'")

    def _assert_directory_created(self, folder_name):
        """Helper method to assert a destination directory was created."""
        expected_dir = os.path.join(self.destination_dir, folder_name)
        self.assertTrue(os.path.isdir(expected_dir), 
                       f"Directory '{folder_name}' should be created")

    # --- Scenario 1: Only Files ---
    
    @unittest.skip("skip for now")
    def test_migrate_directory_only_files_single_category(self):
        """Test migrating a directory with only files of the same category."""
        # Create multiple text files
        test_files = ['document1.txt', 'notes.txt', 'readme.txt']
        for filename in test_files:
            self._create_test_file(os.path.join(self.source_dir, filename))

        # Run migration
        self._run_shell_function(f'migrate_directory "{self.source_dir}" "{self.destination_dir}"')
        
        # Assert the text_files directory was created
        self._assert_directory_created('text_files')
        
        # Assert all files were migrated correctly
        for filename in test_files:
            self._assert_file_migrated_correctly(filename, os.path.join(self.destination_dir, "text_files"))

    @unittest.skip("skip for now")
    def test_migrate_directory_only_files_multiple_categories(self):
        """Test migrating a directory with files from multiple categories."""
        test_files = [
            ('report.pdf', 'documents'),
            ('photo.jpg', 'images'), 
            ('music.mp3', 'audio'),
            ('video.mp4', 'videos'),
            ('data.txt', 'text_files'),
            ('backup.zip', 'archives'),
            ('installer.exe', 'executables'),
            ('unknown.xyz', 'other')
        ]
        
        # Create test files
        for filename, _ in test_files:
            self._create_test_file(os.path.join(self.source_dir, filename))

        # Run migration
        result = self._run_shell_function(f'migrate_directory "{self.source_dir}" "{self.destination_dir}"')
        
        # Assert all expected directories were created and files migrated
        for filename, expected_folder in test_files:
            self._assert_directory_created(expected_folder)
            expected_parent_dir= os.path.join(self.destination_dir, expected_folder)
            self._assert_file_migrated_correctly(filename, expected_parent_dir)

    @unittest.skip("skip for now")
    def test_migrate_directory_only_files_randomized(self):
        """Test migrating a directory with random files from various categories."""
        # Create 30 random files
        test_files = []
        extensions = ['txt', 'jpg', 'png', 'mp3', 'pdf', 'zip', 'mp4', 'doc', 'wav', 'gif']
        
        for i in range(30):
            ext = random.choice(extensions)
            filename = f"file{i}.{ext}"
            test_files.append((filename, self._get_expected_folder_for_extension(ext)))
            self._create_test_file(os.path.join(self.source_dir, filename))

        # Run migration
        result = self._run_shell_function(f'migrate_directory "{self.source_dir}" "{self.destination_dir}"')
        
        # Verify all files were migrated correctly
        for filename, expected_folder in test_files:
            expected_parent_dir = os.path.join(self.destination_dir, expected_folder)
            self._assert_file_migrated_correctly(filename, expected_parent_dir)

    # --- Scenario 2: One Level of Subdirectories ---
    
    @unittest.skip("skip for now")
    def test_migrate_directory_one_level_subdirectories(self):
        """Test migrating a directory with one level of subdirectories."""
        # Create subdirectories with files
        subdirs = ['subdir1', 'subdir2', 'subdir3']
        test_files = []
        
        for subdir in subdirs:
            subdir_path = os.path.join(self.source_dir, subdir)
            # Create files in each subdirectory
            files_in_subdir = [
                (f'{subdir}_document.pdf', 'documents'),
                (f'{subdir}_image.png', 'images'),
                (f'{subdir}_text.txt', 'text_files')
            ]
            for filename, expected_folder in files_in_subdir:
                self._create_test_file(os.path.join(subdir_path, filename))
                path = os.path.join(self.destination_dir, subdir, expected_folder)
                test_files.append((filename, path))

        # Also add some files in the root
        root_files = [
                    ('root_file.mp3', os.path.join(self.destination_dir, 'audio')), 
                    ('root_doc.docx', os.path.join(self.destination_dir, 'documents'))
                    ]
        for filename, p in root_files:
            self._create_test_file(os.path.join(self.source_dir, filename))
            test_files.append((filename, p))

        # Run migration
        result = self._run_shell_function(f'migrate_directory "{self.source_dir}" "{self.destination_dir}"')
        
        # Verify all files were migrated correctly
        for filename, expected_folder in test_files:
            self._assert_file_migrated_correctly(filename, expected_folder)

    @unittest.skip("skip for now")
    def test_migrate_directory_one_level_empty_subdirectories(self):
        """Test migrating a directory with empty subdirectories."""
        # Create empty subdirectories
        for i in range(3):
            os.makedirs(os.path.join(self.source_dir, f'empty_dir{i}'))
        
        # Add some files in the root
        test_files = [('file1.txt', 'text_files'), ('file2.jpg', 'images')]
        for filename, expected_folder in test_files:
            self._create_test_file(os.path.join(self.source_dir, filename))

        # Run migration
        result = self._run_shell_function(f'migrate_directory "{self.source_dir}" "{self.destination_dir}"')
        
        # Verify files were migrated correctly
        for filename, expected_folder in test_files:
            self._assert_file_migrated_correctly(filename, expected_folder)

    # --- Scenario 3: Multiple Levels of Subdirectories ---
    
    @unittest.skip("skip for now")
    def test_migrate_directory_two_levels_subdirectories(self):
        """Test migrating a directory with two levels of subdirectories."""
        test_files = []
        
        # Create nested structure: source/level1/level2/
        for i in range(2):
            for j in range(2):
                nested_path = os.path.join(self.source_dir, f'level1_{i}', f'level2_{j}')
                files_in_nested = [
                    (f'nested_{i}_{j}_doc.pdf', 'documents'),
                    (f'nested_{i}_{j}_image.gif', 'images'),
                ]
                for filename, expected_folder in files_in_nested:
                    self._create_test_file(os.path.join(nested_path, filename))
                    test_files.append((filename, expected_folder))

        # Run migration
        result = self._run_shell_function(f'migrate_directory "{self.source_dir}" "{self.destination_dir}"')
        
        # Verify all files were migrated correctly
        for filename, expected_folder in test_files:
            self._assert_file_migrated_correctly(filename, expected_folder)

    @unittest.skip("skip for now")
    def test_migrate_directory_three_levels_subdirectories(self):
        """Test migrating a directory with three levels of subdirectories."""
        test_files = []
        
        # Create deeply nested structure: source/l1/l2/l3/
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    deep_path = os.path.join(self.source_dir, f'l1_{i}', f'l2_{j}', f'l3_{k}')
                    files_in_deep = [
                        (f'deep_{i}_{j}_{k}.txt', 'text_files'),
                        (f'deep_{i}_{j}_{k}.zip', 'archives'),
                    ]
                    for filename, expected_folder in files_in_deep:
                        self._create_test_file(os.path.join(deep_path, filename))
                        test_files.append((filename, expected_folder))

        # Run migration
        result = self._run_shell_function(f'migrate_directory "{self.source_dir}" "{self.destination_dir}"')
        
        # Verify all files were migrated correctly
        for filename, expected_folder in test_files:
            self._assert_file_migrated_correctly(filename, expected_folder)

    @unittest.skip("skip for now")
    def test_migrate_directory_mixed_levels_comprehensive(self):
        """Test migrating a comprehensive directory structure with mixed levels and file types."""
        test_files = []
        
        # Root level files
        root_files = [('root.pdf', 'documents'), ('root.mp3', 'audio')]
        for filename, expected_folder in root_files:
            self._create_test_file(os.path.join(self.source_dir, filename))
            test_files.append((filename, expected_folder))
        
        # Level 1 files
        level1_path = os.path.join(self.source_dir, 'projects')
        level1_files = [('project.docx', 'documents'), ('screenshot.png', 'images')]
        for filename, expected_folder in level1_files:
            self._create_test_file(os.path.join(level1_path, filename))
            test_files.append((filename, expected_folder))
        
        # Level 2 files
        level2_path = os.path.join(level1_path, 'web_project')
        level2_files = [('index.txt', 'text_files'), ('demo.mp4', 'videos')]
        for filename, expected_folder in level2_files:
            self._create_test_file(os.path.join(level2_path, filename))
            test_files.append((filename, expected_folder))
        
        # Level 3 files
        level3_path = os.path.join(level2_path, 'assets')
        level3_files = [('logo.jpg', 'images'), ('app.exe', 'executables')]
        for filename, expected_folder in level3_files:
            self._create_test_file(os.path.join(level3_path, filename))
            test_files.append((filename, expected_folder))

        # Run migration
        result = self._run_shell_function(f'migrate_directory "{self.source_dir}" "{self.destination_dir}"')
        
        # Verify all files were migrated correctly regardless of their original nesting level
        for filename, expected_folder in test_files:
            self._assert_file_migrated_correctly(filename, expected_folder)



    @unittest.skip("skip for now")
    def test_migrate_directory_files_without_extensions(self):
        """Test that files without extensions are ignored (as per current implementation)."""
        # Create files without extensions
        files_without_ext = ['README', 'Makefile', 'LICENSE']
        for filename in files_without_ext:
            self._create_test_file(os.path.join(self.source_dir, filename))
        
        # Create some files with extensions
        files_with_ext = [('test.txt', 'text_files'), ('image.png', 'images')]
        for filename, expected_folder in files_with_ext:
            self._create_test_file(os.path.join(self.source_dir, filename))

        # Run migration
        result = self._run_shell_function(f'migrate_directory "{self.source_dir}" "{self.destination_dir}"')
        
        # Verify only files with extensions were migrated
        for filename, expected_folder in files_with_ext:
            self._assert_file_migrated_correctly(filename, expected_folder)
        
        # Verify files without extensions were not migrated
        for filename in files_without_ext:
            for category in ['text_files', 'images', 'documents', 'audio', 'videos', 'archives', 'executables', 'other']:
                potential_path = os.path.join(self.destination_dir, category, filename)
                self.assertFalse(os.path.exists(potential_path), 
                               f"File without extension '{filename}' should not be migrated")


if __name__ == '__main__':
    unittest.main()