import pytest
import os
import time
from backup import backup_to_s3

# Performance Test 1: Backup Speed for Large Directory
def test_large_directory_backup():
    large_dir = "/tmp/large_test_dir"
    os.makedirs(large_dir, exist_ok=True)
    # Create 1000 dummy files
    for i in range(1000):
        with open(f"{large_dir}/file_{i}.txt", "w") as f:
            f.write("This is a test file.\n")

    config = {
        "backup_paths": [large_dir],
        "s3_bucket": "hybytes-rpm-repo",
    }

    start_time = time.time()
    backup_to_s3(config)
    end_time = time.time()

    # Ensure backup completes within a reasonable time (e.g., 30 seconds)
    assert end_time - start_time < 30, "Backup took too long"

    # Clean up
    os.system(f"rm -r {large_dir}")

# Performance Test 2: Backup with Multiple Directories
def test_multiple_directories_backup():
    dir1 = "/tmp/testdir1"
    dir2 = "/tmp/testdir2"
    os.makedirs(dir1, exist_ok=True)
    os.makedirs(dir2, exist_ok=True)

    # Create dummy files in both directories
    for i in range(100):
        with open(f"{dir1}/file_{i}.txt", "w") as f:
            f.write("This is a test file.\n")
        with open(f"{dir2}/file_{i}.txt", "w") as f:
            f.write("This is a test file.\n")

    config = {
        "backup_paths": [dir1, dir2],
        "s3_bucket": "hybytes-rpm-repo",
    }

    start_time = time.time()
    backup_to_s3(config)
    end_time = time.time()

    # Ensure backup completes within a reasonable time (e.g., 60 seconds)
    assert end_time - start_time < 60, "Backup of multiple directories took too long"

    # Clean up
    os.system(f"rm -r {dir1}")
    os.system(f"rm -r {dir2}")

# Performance Test 3: Stress Test for Frequent Backups
def test_frequent_backups():
    test_dir = "/tmp/frequent_test_dir"
    os.makedirs(test_dir, exist_ok=True)
    with open(f"{test_dir}/file.txt", "w") as f:
        f.write("This is a test file.\n")

    config = {
        "backup_paths": [test_dir],
        "s3_bucket": "hybytes-rpm-repo",
    }

    for _ in range(5):  # Run backup 5 times
        start_time = time.time()
        backup_to_s3(config)
        end_time = time.time()
        assert end_time - start_time < 15, "Frequent backup took too long"

    # Clean up
    os.system(f"rm -r {test_dir}")

# Performance Test 4: Large File Upload
def test_large_file_upload():
    large_dir = "/tmp/large_file_test"
    os.makedirs(large_dir, exist_ok=True)
    large_file = f"{large_dir}/large_file.txt"
    with open(large_file, "w") as f:
        f.write("A" * 1024 * 1024 * 50)  # 50 MB file

    config = {
        "backup_paths": [large_dir],
        "s3_bucket": "hybytes-rpm-repo",
    }

    start_time = time.time()
    backup_to_s3(config)
    end_time = time.time()

    # Ensure upload completes within a reasonable time (e.g., 60 seconds)
    assert end_time - start_time < 60, "Large file upload took too long"

    # Clean up
    os.system(f"rm -r {large_dir}")
