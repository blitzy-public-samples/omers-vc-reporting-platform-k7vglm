"""
Database Backup and Cleanup Script

This script creates a backup of the database and uploads it to Azure Blob Storage.
It also cleans up old backups based on a retention period.

Requirements addressed:
- Data Backup and Recovery (6. SECURITY CONSIDERATIONS/6.2 DATA SECURITY/6.2.5 Data Backup and Recovery)
- Long-term Data Archiving (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.6 Storage)
"""

import os
import logging
import subprocess
from datetime import datetime, timedelta
from typing import Optional

from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import AzureError

from src.database.config import get_database_settings
from src.database.session import engine

# Azure Blob Storage Client (version ^12.8.1)
# Azure Identity (version ^1.6.0)

# Global variables
BACKUP_CONTAINER_NAME = "database-backups"
BACKUP_RETENTION_DAYS = 35

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_backup() -> bool:
    """
    Creates a backup of the database and uploads it to Azure Blob Storage.

    Returns:
        bool: True if backup was successful, False otherwise.
    """
    try:
        # Get database settings
        db_settings = get_database_settings()

        # Create a unique backup file name using the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file_name = f"backup_{timestamp}.sql"

        # Parse database connection details
        db_url_parts = db_settings.DATABASE_URL.split("://")[1].split("@")
        db_user = db_url_parts[0].split(":")[0]
        db_password = db_url_parts[0].split(":")[1]
        db_host = db_url_parts[1].split(":")[0]
        db_port = db_url_parts[1].split(":")[1].split("/")[0]
        db_name = db_url_parts[1].split("/")[1]

        # Use pg_dump to create a backup of the database
        pg_dump_command = [
            "pg_dump",
            "-h", db_host,
            "-p", db_port,
            "-U", db_user,
            "-d", db_name,
            "-f", backup_file_name,
            "-F", "c"  # Use custom format for compression
        ]

        # Set PGPASSWORD environment variable for authentication
        os.environ["PGPASSWORD"] = db_password

        # Execute pg_dump command
        subprocess.run(pg_dump_command, check=True, capture_output=True, text=True)

        # Upload the backup file to Azure Blob Storage
        upload_to_azure_blob(backup_file_name)

        # Remove the local backup file
        os.remove(backup_file_name)

        return True

    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing pg_dump: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Error creating database backup: {str(e)}")
        return False

def upload_to_azure_blob(file_name: str) -> None:
    """
    Uploads a file to Azure Blob Storage.

    Args:
        file_name (str): Name of the file to upload.

    Raises:
        AzureError: If there's an error during the upload process.
    """
    try:
        # Authenticate with Azure using DefaultAzureCredential
        credential = DefaultAzureCredential()

        # Create a BlobServiceClient using the storage account name from environment variables
        account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
        if not account_name:
            raise ValueError("AZURE_STORAGE_ACCOUNT_NAME environment variable is not set")

        blob_service_client = BlobServiceClient(
            account_url=f"https://{account_name}.blob.core.windows.net",
            credential=credential
        )

        # Get a reference to the container
        container_client = blob_service_client.get_container_client(BACKUP_CONTAINER_NAME)

        # Upload the backup file to Azure Blob Storage
        with open(file_name, "rb") as backup_file:
            container_client.upload_blob(name=file_name, data=backup_file)

        logger.info(f"Database backup uploaded: {file_name}")

    except AzureError as e:
        logger.error(f"Azure error during backup upload: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error uploading backup to Azure Blob Storage: {str(e)}")
        raise

def cleanup_old_backups() -> None:
    """
    Removes backups older than the specified retention period.
    """
    try:
        # Authenticate with Azure using DefaultAzureCredential
        credential = DefaultAzureCredential()

        # Create a BlobServiceClient using the storage account name from environment variables
        account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
        if not account_name:
            raise ValueError("AZURE_STORAGE_ACCOUNT_NAME environment variable is not set")

        blob_service_client = BlobServiceClient(
            account_url=f"https://{account_name}.blob.core.windows.net",
            credential=credential
        )

        # Get a reference to the container
        container_client = blob_service_client.get_container_client(BACKUP_CONTAINER_NAME)

        # Calculate the cutoff date based on BACKUP_RETENTION_DAYS
        cutoff_date = datetime.utcnow() - timedelta(days=BACKUP_RETENTION_DAYS)

        # List all blobs in the backup container
        blobs = container_client.list_blobs()

        # Delete blobs older than the cutoff date
        for blob in blobs:
            if blob.creation_time < cutoff_date:
                container_client.delete_blob(blob.name)
                logger.info(f"Deleted old backup: {blob.name}")

        logger.info("Cleanup of old backups completed")

    except AzureError as e:
        logger.error(f"Azure error during cleanup of old backups: {str(e)}")
    except Exception as e:
        logger.error(f"Error cleaning up old backups: {str(e)}")

def main() -> None:
    """
    Main function to run the backup process.
    """
    try:
        logger.info("Starting database backup process")

        # Create backup
        if create_backup():
            # If backup is successful, clean up old backups
            cleanup_old_backups()
        else:
            logger.error("Backup creation failed, skipping cleanup")

        logger.info("Database backup process completed")

    except Exception as e:
        logger.error(f"Error in backup process: {str(e)}")

if __name__ == "__main__":
    main()