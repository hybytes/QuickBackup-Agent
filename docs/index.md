# QuickBackup Agent - Amazon Linux Support

## Overview
QuickBackup Agent is a lightweight command-line tool for backing up specific directories to an Amazon S3 bucket. It is designed to work efficiently on **Amazon Linux 2** and **Amazon Linux 2023** versions, allowing users to automate and manage backups securely and effectively.

## Supported Platforms
QuickBackup Agent is fully supported on **Amazon Linux 2** and **Amazon Linux 2023**, ensuring compatibility with the latest Amazon Linux versions.

## Installation and Setup

### 1. Install Python 3 and Pip
QuickBackup Agent requires Python 3 to run. Ensure that Python 3 and Pip are installed:

```bash
sudo yum install -y python3 pip
pip3 install boto3 pyyaml
