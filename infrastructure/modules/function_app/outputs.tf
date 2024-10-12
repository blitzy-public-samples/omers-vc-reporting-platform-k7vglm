# This file defines output values for the Azure Function App Terraform module.
# It addresses the requirement for implementing Azure Functions for background processing tasks,
# such as data transformation and currency conversion, as specified in:
# 2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.5 Data Processing

output "function_app_name" {
  value       = azurerm_function_app.function_app.name
  description = "The name of the created Azure Function App"
}

output "function_app_default_hostname" {
  value       = azurerm_function_app.function_app.default_hostname
  description = "The default hostname of the created Azure Function App"
}

output "function_app_id" {
  value       = azurerm_function_app.function_app.id
  description = "The ID of the created Azure Function App"
}

output "storage_account_name" {
  value       = azurerm_storage_account.function_storage.name
  description = "The name of the storage account created for the Function App"
}

output "storage_account_primary_access_key" {
  value       = azurerm_storage_account.function_storage.primary_access_key
  description = "The primary access key of the storage account created for the Function App"
  sensitive   = true
}

output "function_app_principal_id" {
  value       = azurerm_function_app.function_app.identity[0].principal_id
  description = "The Principal ID of the Function App's managed identity"
}

output "key_vault_id" {
  value       = azurerm_key_vault.function_key_vault.id
  description = "The ID of the Key Vault associated with the Function App"
}

output "key_vault_uri" {
  value       = azurerm_key_vault.function_key_vault.vault_uri
  description = "The URI of the Key Vault associated with the Function App"
}