"""
Test cases for QuickBackup Agent.

Environment: Production (Amazon Linux)
Purpose: Validate backup functionality, error handling, and configuration.
"""


import pytest
import os
from unittest.mock import patch, MagicMock
from backup import load_config, backup_to_s3

# Test Case 1: Valid Directory Backup
def test_valid_directory():
    config = {
        "backup_paths": ["/home/ec2-user/testdir"],
        "s3_bucket": "hybytes-rpm-repo",  
    }
    with patch("boto3.client") as mock_s3:
        backup_to_s3(config)
        mock_s3().upload_file.assert_called_once()

# Test Case 2: Invalid Directory
def test_invalid_directory():
    config = {
        "backup_paths": ["/invalid/path"],
        "s3_bucket": "hybytes-rpm-repo",
    }
    with pytest.raises(Exception):
        backup_to_s3(config)


# Test Case 3: Missing S3 Bucket
def test_missing_s3_bucket():
    config = {
        "backup_paths": ["/home/ec2-user/testdir"],
        # Missing "s3_bucket" key
    }
    with pytest.raises(KeyError):
        backup_to_s3(config)

# Test Case 4: Simulated S3 Upload Failure
def test_s3_upload_failure():
    config = {
        "backup_paths": ["/home/ec2-user/testdir"],
        "s3_bucket": "hybytes-rpm-repo",
    }
    with patch("boto3.client") as mock_s3:
        mock_s3().upload_file.side_effect = Exception("Simulated S3 error")
        with pytest.raises(Exception):
            backup_to_s3(config)

# Test Case 5: Valid Configuration Load
def test_load_valid_config():
    with patch("builtins.open", new_callable=MagicMock):
        with patch("yaml.safe_load", return_value={"backup_paths": ["/home/ec2-user/testdir"], "s3_bucket": "hybytes-rpm-repo"}):
            config = load_config()
            assert "backup_paths" in config
            assert "s3_bucket" in config

# Test Case 6: Missing Configuration File
def test_missing_config_file():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            load_config()

