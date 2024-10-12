# Terraform output definitions for the Azure Blob Storage module used in the VC firm's financial reporting metrics backend platform

output "storage_account_id" {
  description = "The ID of the Azure Storage Account"
  value       = azurerm_storage_account.main.id
}

output "storage_account_name" {
  description = "The name of the Azure Storage Account"
  value       = azurerm_storage_account.main.name
}

output "primary_access_key" {
  description = "The primary access key for the Azure Storage Account"
  value       = azurerm_storage_account.main.primary_access_key
  sensitive   = true
}

output "primary_connection_string" {
  description = "The primary connection string for the Azure Storage Account"
  value       = azurerm_storage_account.main.primary_connection_string
  sensitive   = true
}

output "archive_container_name" {
  description = "The name of the container for archived data"
  value       = azurerm_storage_container.archive.name
}

output "backups_container_name" {
  description = "The name of the container for database backups"
  value       = azurerm_storage_container.backups.name
}

output "primary_blob_endpoint" {
  description = "The primary blob endpoint URL"
  value       = azurerm_storage_account.main.primary_blob_endpoint
}

output "secondary_access_key" {
  description = "The secondary access key for the Azure Storage Account"
  value       = azurerm_storage_account.main.secondary_access_key
  sensitive   = true
}

output "secondary_connection_string" {
  description = "The secondary connection string for the Azure Storage Account"
  value       = azurerm_storage_account.main.secondary_connection_string
  sensitive   = true
}

output "primary_file_endpoint" {
  description = "The primary file endpoint URL"
  value       = azurerm_storage_account.main.primary_file_endpoint
}

output "primary_queue_endpoint" {
  description = "The primary queue endpoint URL"
  value       = azurerm_storage_account.main.primary_queue_endpoint
}

output "primary_table_endpoint" {
  description = "The primary table endpoint URL"
  value       = azurerm_storage_account.main.primary_table_endpoint
}

output "storage_account_tier" {
  description = "The tier of the Azure Storage Account"
  value       = azurerm_storage_account.main.account_tier
}

output "storage_account_replication_type" {
  description = "The replication type of the Azure Storage Account"
  value       = azurerm_storage_account.main.account_replication_type
}

output "storage_account_kind" {
  description = "The kind of the Azure Storage Account"
  value       = azurerm_storage_account.main.account_kind
}

output "storage_account_access_tier" {
  description = "The access tier of the Azure Storage Account"
  value       = azurerm_storage_account.main.access_tier
}

output "storage_account_https_only" {
  description = "Whether the Azure Storage Account only allows HTTPS traffic"
  value       = azurerm_storage_account.main.enable_https_traffic_only
}

output "storage_account_min_tls_version" {
  description = "The minimum TLS version for the Azure Storage Account"
  value       = azurerm_storage_account.main.min_tls_version
}

# Note: The following outputs assume that these containers are defined in the main.tf file.
# If they are not, these should be removed or added to the main.tf file.

output "raw_data_container_name" {
  description = "The name of the container for raw data"
  value       = azurerm_storage_container.raw_data.name
}

output "processed_data_container_name" {
  description = "The name of the container for processed data"
  value       = azurerm_storage_container.processed_data.name
}

output "logs_container_name" {
  description = "The name of the container for logs"
  value       = azurerm_storage_container.logs.name
}