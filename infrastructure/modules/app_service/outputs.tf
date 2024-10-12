# This file defines the output values for the Azure App Service module.
# These outputs provide essential information about the created Azure App Service
# for use in other parts of the infrastructure or for reference.

# Requirement addressed: Application Hosting Information
# Location: 2. SYSTEM ARCHITECTURE/2.1 High-Level System Architecture

output "app_service_name" {
  description = "The name of the created Azure App Service."
  value       = azurerm_app_service.main.name
}

output "app_service_default_hostname" {
  description = "The default hostname of the created Azure App Service."
  value       = azurerm_app_service.main.default_site_hostname
}

output "app_service_plan_id" {
  description = "The ID of the App Service Plan."
  value       = azurerm_app_service_plan.main.id
}

output "app_service_identity_principal_id" {
  description = "The Principal ID of the System Assigned Identity of the App Service."
  value       = azurerm_app_service.main.identity[0].principal_id
}

output "app_service_id" {
  description = "The ID of the created Azure App Service."
  value       = azurerm_app_service.main.id
}

output "app_service_outbound_ip_addresses" {
  description = "A comma-separated list of outbound IP addresses for the App Service."
  value       = azurerm_app_service.main.outbound_ip_addresses
}

output "app_service_possible_outbound_ip_addresses" {
  description = "A comma-separated list of possible outbound IP addresses for the App Service."
  value       = azurerm_app_service.main.possible_outbound_ip_addresses
}

output "app_service_site_credential" {
  description = "The site credentials for the App Service."
  value       = azurerm_app_service.main.site_credential
  sensitive   = true
}

output "app_service_identity_tenant_id" {
  description = "The Tenant ID for the Service Principal associated with the Managed Service Identity of the App Service."
  value       = azurerm_app_service.main.identity[0].tenant_id
}

output "app_service_custom_domain_verification_id" {
  description = "The identifier used by App Service to perform domain ownership verification via DNS TXT record."
  value       = azurerm_app_service.main.custom_domain_verification_id
}

output "app_service_default_site_hostname" {
  description = "The default hostname associated with the App Service - such as mysite.azurewebsites.net."
  value       = azurerm_app_service.main.default_site_hostname
}

output "app_service_kind" {
  description = "The kind of the App Service (e.g., 'app', 'functionapp')."
  value       = azurerm_app_service.main.kind
}