import os
import boto3
import pytest
from unittest.mock import patch
from backup import load_config, backup_to_s3

# Integration Test Case 1: Backup a valid directory and upload to S3
def test_integration_valid_backup():
    # Setup: Create a test directory and file
    test_dir = "/tmp/testdir"
    test_file = os.path.join(test_dir, "test.txt")
    os.makedirs(test_dir, exist_ok=True)
    with open(test_file, "w") as f:
        f.write("This is a test file.")

    # Configure the backup
    config = {
        "backup_paths": [test_dir],
        "s3_bucket": "hybytes-rpm-repo",  # Replace with your actual S3 bucket
    }

    # Perform the backup
    try:
        backup_to_s3(config)

        # Check if the file is uploaded to S3
        s3 = boto3.client("s3")
        bucket_objects = s3.list_objects_v2(Bucket=config["s3_bucket"])
        uploaded_files = [obj["Key"] for obj in bucket_objects.get("Contents", [])]
        assert any("backup_" in file for file in uploaded_files), "Backup file not found in S3."
    finally:
        # Cleanup: Remove the test directory and file
        for file in os.listdir(test_dir):
            os.remove(os.path.join(test_dir, file))
        os.rmdir(test_dir)

# Integration Test Case 2: Invalid directory handling
def test_integration_invalid_directory():
    config = {
        "backup_paths": ["/invalid/path"],
        "s3_bucket": "hybytes-rpm-repo",
    }
    with pytest.raises(Exception):
        backup_to_s3(config)

# Integration Test Case 3: Missing S3 bucket
def test_integration_missing_s3_bucket():
    config = {
        "backup_paths": ["/home/ec2-user/testdir"],
        # Missing S3 bucket key
    }
    with pytest.raises(KeyError):
        backup_to_s3(config)
