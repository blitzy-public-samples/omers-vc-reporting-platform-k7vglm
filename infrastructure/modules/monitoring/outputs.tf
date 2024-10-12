# This file defines the outputs for the monitoring module, exposing important resource
# identifiers and properties for use in other modules or the root configuration.
# It addresses the "Monitoring and Logging" requirement located in 
# "2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.4 Monitoring & Logging"

output "log_analytics_workspace_id" {
  description = "The ID of the Log Analytics Workspace"
  value       = azurerm_log_analytics_workspace.main.id
}

output "log_analytics_workspace_name" {
  description = "The name of the Log Analytics Workspace"
  value       = azurerm_log_analytics_workspace.main.name
}

output "application_insights_id" {
  description = "The ID of the Application Insights resource"
  value       = azurerm_application_insights.main.id
}

output "application_insights_name" {
  description = "The name of the Application Insights resource"
  value       = azurerm_application_insights.main.name
}

output "application_insights_app_id" {
  description = "The App ID of the Application Insights resource"
  value       = azurerm_application_insights.main.app_id
}

output "application_insights_instrumentation_key" {
  description = "The instrumentation key of the Application Insights resource"
  value       = azurerm_application_insights.main.instrumentation_key
  sensitive   = true
}

output "application_insights_connection_string" {
  description = "The connection string of the Application Insights resource"
  value       = azurerm_application_insights.main.connection_string
  sensitive   = true
}

output "monitor_action_group_id" {
  description = "The ID of the Monitor Action Group for critical alerts"
  value       = azurerm_monitor_action_group.critical.id
}

output "monitor_action_group_name" {
  description = "The name of the Monitor Action Group for critical alerts"
  value       = azurerm_monitor_action_group.critical.name
}

output "monitor_diagnostic_setting_id" {
  description = "The ID of the Monitor Diagnostic Setting"
  value       = azurerm_monitor_diagnostic_setting.main.id
}