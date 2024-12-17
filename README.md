# QuickBackup Agent Documentation

## Overview

QuickBackup Agent is a lightweight tool for backing up specified directories and uploading them to an Amazon S3 bucket. The agent allows for configurable backup paths via a YAML file and supports scheduling backups at regular intervals.

### Supported Platforms

QuickBackup Agent supports the following Amazon Linux versions:
- Amazon Linux 2
- Amazon Linux 2023

### Prerequisites

- Amazon Linux 2 or Amazon Linux 2023.
- Python 3.9+.
- AWS CLI installed and configured.
- S3 Bucket for backups.

### Dependencies

QuickBackup Agent requires the following dependencies:
- **boto3**: For interacting with AWS services.
- **pyyaml**: For reading and writing YAML configuration files.
- **python3**: The version of Python required to run the application.

## Installation Guide
QuickBackup Agent can be easily installed and configured on Amazon Linux platforms by following these steps:
### Step 1: Install the QuickBackup Agent



```bash
sudo yum install https://hybytes-rpm-repo.s3.eu-west-2.amazonaws.com/quickbackup-1.0.0-1.amzn2023.x86_64.rpm

```

### Explanation:
- **boto3**, **python3** and **pyyaml** are required to interact with AWS services and read/write configuration files. When you install QuickBackup Agent using the RPM package, these dependencies will be installed automatically, so you don’t need to manually install them via `pip`.
- This approach streamlines the installation process for users, ensuring they don't need to worry about additional setup steps.

### Step 2: Verify Installation
Confirm that the files are correctly installed:


```bash
ls /usr/local/bin/backup.py
ls /etc/quickbackup/config.yml
ls /etc/systemd/system/quickbackup.service

```

### Step 3: Configure AWS Credentials
Confirm that the files are correctly installed:


```bash
aws configure

```
When prompted, provide the following information:  
* **Access Key ID:** Your AWS Access Key ID   
* **Secret Access Key:** Your AWS Secret Access Key   
* **Default region name:** The AWS region where your S3 bucket is located (e.g., us-west-2).  
* **Default output format:** Leave this blank or set to json.


### Step 4: Enable and Start the Service


```bash
sudo systemctl enable quickbackup
sudo systemctl start quickbackup

```


### Step 5: Verify the Service



```bash
sudo systemctl status quickbackup

```


### Step 6: Configure the Backup Agent

Configure a configuration file at `/etc/quickbackup/config.yml`:

```bash
backup_paths:
  - /path/to/your/directory
s3_bucket: your-s3-bucket-name

```
Ensure that the paths you want to back up are correctly specified in the backup_paths section.

## Backup Scheduling
QuickBackup Agent can be configured to run backups on a scheduled basis using systemd timers. You can configure the agent to perform backups at your desired intervals, such as every hour, day, or week.

## Example Configuration
Here is an example configuration for QuickBackup Agent to back up a directory to an S3 bucket:

```bash
backup_paths:
  - /var/log/myapp
  - /home/ubuntu/data
s3_bucket: my-backup-bucket


```
This configuration will back up both /var/log/myapp and /home/ubuntu/data directories to the my-backup-bucket S3 bucket.

## Troubleshooting

Here is an example configuration for QuickBackup Agent to back up a directory to an S3 bucket:

### Issue 1: "Config file not found"

If you encounter an error stating that the configuration file is not found, ensure that you have created the file at the correct location (`/etc/quickbackup/config.yml)` and that the paths are valid.

### Issue 2: "Permission Denied" when running backup

Ensure that the user running the QuickBackup Agent has appropriate permissions to access the directories you are backing up and write to the specified S3 bucket.

## Contributing

We welcome contributions to QuickBackup Agent! If you'd like to contribute, please fork the repository and submit a pull request with your proposed changes.

## Support

For any issues or inquiries, please reach out to us via GitHub issues or email at support@hybytes.com.