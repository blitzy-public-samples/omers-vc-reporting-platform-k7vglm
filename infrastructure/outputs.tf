# infrastructure/outputs.tf

# This file defines the outputs for the VC firm's financial reporting metrics backend platform
# It exposes important information about the created Azure resources

# Resource Group Output
output "resource_group_name" {
  description = "The name of the main resource group"
  value       = azurerm_resource_group.main.name
}

# App Service Outputs
output "app_service_name" {
  description = "The name of the App Service hosting the FastAPI application"
  value       = module.app_service.app_service_name
}

output "app_service_default_hostname" {
  description = "The default hostname of the App Service"
  value       = module.app_service.app_service_default_hostname
}

# Database Outputs
output "database_server_name" {
  description = "The name of the Azure Database for PostgreSQL server"
  value       = module.database.server_name
}

output "database_name" {
  description = "The name of the PostgreSQL database"
  value       = module.database.database_name
}

# Function App Outputs
output "function_app_name" {
  description = "The name of the Azure Function App for data transformation"
  value       = module.function_app.function_app_name
}

output "function_app_default_hostname" {
  description = "The default hostname of the Function App"
  value       = module.function_app.function_app_default_hostname
}

# Key Vault Outputs
output "key_vault_name" {
  description = "The name of the Azure Key Vault"
  value       = module.key_vault.key_vault_name
}

output "key_vault_uri" {
  description = "The URI of the Azure Key Vault"
  value       = module.key_vault.key_vault_uri
}

# Storage Outputs
output "storage_account_name" {
  description = "The name of the storage account for data archiving and backups"
  value       = module.storage.storage_account_name
}

# Monitoring Outputs
output "log_analytics_workspace_id" {
  description = "The ID of the Log Analytics workspace"
  value       = module.monitoring.log_analytics_workspace_id
}

output "application_insights_instrumentation_key" {
  description = "The instrumentation key for Application Insights"
  value       = module.monitoring.application_insights_instrumentation_key
  sensitive   = true
}

# Additional Outputs for Enhanced Observability and Management

# App Service Plan Output
output "app_service_plan_id" {
  description = "The ID of the App Service Plan"
  value       = module.app_service.app_service_plan_id
}

# Database Connection String Output
output "database_connection_string" {
  description = "The connection string for the PostgreSQL database"
  value       = module.database.connection_string
  sensitive   = true
}

# Function App Storage Account Output
output "function_app_storage_account_name" {
  description = "The name of the storage account used by the Function App"
  value       = module.function_app.storage_account_name
}

# Key Vault Access Policy Output
output "key_vault_access_policy_object_ids" {
  description = "The Object IDs of the access policies applied to the Key Vault"
  value       = module.key_vault.access_policy_object_ids
}

# Storage Account Primary Access Key Output
output "storage_account_primary_access_key" {
  description = "The primary access key for the storage account"
  value       = module.storage.primary_access_key
  sensitive   = true
}

# Application Insights App ID Output
output "application_insights_app_id" {
  description = "The App ID of the Application Insights instance"
  value       = module.monitoring.application_insights_app_id
}

# Resource Group Location Output
output "resource_group_location" {
  description = "The location of the main resource group"
  value       = azurerm_resource_group.main.location
}

# Tags Output
output "resource_tags" {
  description = "The tags applied to the resources"
  value       = azurerm_resource_group.main.tags
}