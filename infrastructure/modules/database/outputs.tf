# This file defines the output values for the Azure Database for PostgreSQL module.
# It exposes necessary information for connecting to the created PostgreSQL database,
# addressing the requirement "Expose Database Connection Information" from section
# 2. SYSTEM ARCHITECTURE/2.2.2 Data Layer of the technical specification.

output "server_name" {
  description = "The name of the PostgreSQL server"
  value       = azurerm_postgresql_server.main.name
}

output "server_fqdn" {
  description = "The fully qualified domain name of the PostgreSQL server"
  value       = azurerm_postgresql_server.main.fqdn
}

output "database_name" {
  description = "The name of the PostgreSQL database"
  value       = azurerm_postgresql_database.main.name
}

output "server_id" {
  description = "The resource ID of the PostgreSQL server"
  value       = azurerm_postgresql_server.main.id
}

output "administrator_login" {
  description = "The administrator username for the PostgreSQL server"
  value       = azurerm_postgresql_server.main.administrator_login
  sensitive   = true
}

output "private_endpoint_ip" {
  description = "The private IP address of the PostgreSQL server's private endpoint"
  value       = azurerm_private_endpoint.main.private_service_connection[0].private_ip_address
}

output "server_version" {
  description = "The version of the PostgreSQL server"
  value       = azurerm_postgresql_server.main.version
}

output "ssl_enforcement_enabled" {
  description = "Whether SSL enforcement is enabled on the PostgreSQL server"
  value       = azurerm_postgresql_server.main.ssl_enforcement_enabled
}

output "ssl_minimal_tls_version_enforced" {
  description = "The minimum TLS version enforced on the PostgreSQL server"
  value       = azurerm_postgresql_server.main.ssl_minimal_tls_version_enforced
}

output "public_network_access_enabled" {
  description = "Whether public network access is enabled on the PostgreSQL server"
  value       = azurerm_postgresql_server.main.public_network_access_enabled
}

output "firewall_rules" {
  description = "The list of firewall rules applied to the PostgreSQL server"
  value = concat(
    [azurerm_postgresql_firewall_rule.azure_services],
    azurerm_postgresql_firewall_rule.allowed_ips[*]
  )
  sensitive = true
}

output "diagnostic_settings_name" {
  description = "The name of the diagnostic settings for the PostgreSQL server"
  value       = azurerm_monitor_diagnostic_setting.postgresql.name
}