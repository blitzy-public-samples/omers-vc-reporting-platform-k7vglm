# infrastructure/modules/key_vault/outputs.tf

# This file defines the outputs for the Azure Key Vault module.
# These outputs can be used by other modules or the root module to reference
# the created Key Vault resource.

# Requirement addressed:
# Security (2. SYSTEM ARCHITECTURE/2.5 Security Architecture)
# Provide necessary outputs for the created Azure Key Vault to be used by other modules or the root module

output "key_vault_id" {
  description = "The ID of the created Azure Key Vault"
  value       = azurerm_key_vault.main.id
  sensitive   = false
}

output "key_vault_name" {
  description = "The name of the created Azure Key Vault"
  value       = azurerm_key_vault.main.name
  sensitive   = false
}

output "key_vault_uri" {
  description = "The URI of the created Azure Key Vault"
  value       = azurerm_key_vault.main.vault_uri
  sensitive   = false
}

output "key_vault_tenant_id" {
  description = "The Azure Active Directory tenant ID that should be used for authenticating requests to the Key Vault"
  value       = azurerm_key_vault.main.tenant_id
  sensitive   = false
}

output "key_vault_sku_name" {
  description = "The Name of the SKU used for this Key Vault"
  value       = azurerm_key_vault.main.sku_name
  sensitive   = false
}

output "key_vault_enabled_for_deployment" {
  description = "Boolean flag to specify whether Azure Virtual Machines are permitted to retrieve certificates stored as secrets from the Key Vault"
  value       = azurerm_key_vault.main.enabled_for_deployment
  sensitive   = false
}

output "key_vault_enabled_for_disk_encryption" {
  description = "Boolean flag to specify whether Azure Disk Encryption is permitted to retrieve secrets from the vault and unwrap keys"
  value       = azurerm_key_vault.main.enabled_for_disk_encryption
  sensitive   = false
}

output "key_vault_enabled_for_template_deployment" {
  description = "Boolean flag to specify whether Azure Resource Manager is permitted to retrieve secrets from the Key Vault"
  value       = azurerm_key_vault.main.enabled_for_template_deployment
  sensitive   = false
}

output "key_vault_purge_protection_enabled" {
  description = "Boolean flag to specify whether protection against purge is enabled for this Key Vault"
  value       = azurerm_key_vault.main.purge_protection_enabled
  sensitive   = false
}

output "key_vault_soft_delete_retention_days" {
  description = "The number of days that items should be retained for once soft-deleted"
  value       = azurerm_key_vault.main.soft_delete_retention_days
  sensitive   = false
}

output "key_vault_access_policy" {
  description = "A list of all access policies for the Key Vault"
  value       = azurerm_key_vault.main.access_policy
  sensitive   = true
}

output "key_vault_network_acls" {
  description = "A list of network ACLs for the Key Vault"
  value       = azurerm_key_vault.main.network_acls
  sensitive   = false
}