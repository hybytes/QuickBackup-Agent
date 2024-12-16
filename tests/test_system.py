import os
import time
import boto3
import pytest
from unittest.mock import patch

S3_BUCKET = "hybytes-rpm-repo"  # Your S3 bucket name
TEST_BACKUP_DIR = "/home/ec2-user/testdir"

# Helper function to check S3 bucket
def list_s3_files(bucket_name):
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=bucket_name)
    return [item['Key'] for item in response.get('Contents', [])]

@pytest.fixture
def setup_test_environment():
    # Ensure test directory exists
    os.makedirs(TEST_BACKUP_DIR, exist_ok=True)
    with open(f"{TEST_BACKUP_DIR}/testfile.txt", "w") as f:
        f.write("This is a test file.")
    yield
    # Cleanup after test
    os.remove(f"{TEST_BACKUP_DIR}/testfile.txt")
    os.rmdir(TEST_BACKUP_DIR)

def test_service_running():
    # Check if the service is running
    status = os.system("sudo systemctl is-active --quiet quickbackup")
    assert status == 0, "QuickBackup service is not running"

def test_backup_uploaded(setup_test_environment):
    # Wait for the service to back up files
    time.sleep(130)  # Wait for at least one backup interval
    uploaded_files = list_s3_files(S3_BUCKET)
    assert any("backup_" in file for file in uploaded_files), "No backup file uploaded to S3"

def test_restart_service():
    # Restart the service and ensure it restarts successfully
    os.system("sudo systemctl restart quickbackup")
    status = os.system("sudo systemctl is-active --quiet quickbackup")
    assert status == 0, "QuickBackup service failed to restart"

def test_handle_invalid_config():
    # Test with an invalid configuration file
    invalid_config_path = "/etc/quickbackup/config_invalid.yml"
    original_config_path = "/etc/quickbackup/config.yml"
    backup_config_path = "/etc/quickbackup/config_backup.yml"

    # Use sudo to move the original configuration and create the invalid one
    os.system(f"sudo mv {original_config_path} {backup_config_path}")
    os.system(f"echo 'invalid_yaml_syntax' | sudo tee {invalid_config_path} > /dev/null")

    try:
        # Wait to see if service errors out
        time.sleep(10)
        status = os.system("sudo systemctl is-active --quiet quickbackup")
        assert status != 0, "Service should fail with invalid config"
    finally:
        # Restore original configuration
        os.system(f"sudo mv {backup_config_path} {original_config_path}")
        os.system(f"sudo rm {invalid_config_path}")
