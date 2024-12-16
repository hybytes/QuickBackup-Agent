import boto3
import os
import yaml
from datetime import datetime
import time

# Load configuration
CONFIG_PATH = "/tmp/quickbackup/config.yml"

def load_config():
    """
    Load configuration from the YAML file.
    """
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def validate_config(config):
    """
    Validate the configuration file.
    """
    if "backup_paths" not in config or not isinstance(config["backup_paths"], list):
        raise ValueError("Invalid configuration: 'backup_paths' must be a list.")
    if "s3_bucket" not in config:
        raise ValueError("Invalid configuration: 's3_bucket' is required.")

def backup_directory_to_s3(s3_client, directory, bucket):
    """
    Compress and upload a directory to S3.
    """
    if not os.path.isdir(directory):
        raise Exception(f"Invalid directory: {directory}")
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    zip_file = f"/tmp/backup_{timestamp}.zip"
    
    os.system(f"zip -r {zip_file} {directory}")
    s3_client.upload_file(zip_file, bucket, os.path.basename(zip_file))
    print(f"Backup uploaded: {os.path.basename(zip_file)}")
    os.remove(zip_file)

def backup_to_s3(config):
    """
    Perform backup for all configured directories.
    """
    try:
        s3 = boto3.client("s3")
        for path in config["backup_paths"]:
            backup_directory_to_s3(s3, path, config["s3_bucket"])
    except Exception as e:
        print(f"Error during backup: {e}")
        raise

def main():
    """
    Main execution function for the backup agent.
    """
    try:
        config = load_config()
        validate_config(config)
        
        while True:
            backup_to_s3(config)
            time.sleep(120)  # Wait 2 minutes before the next backup
    except Exception as e:
        print(f"Critical error: {e}")

if __name__ == "__main__":
    main()
