# This file defines input variables for the monitoring module, which configures
# Azure Monitor and Application Insights resources.
# Requirement: Monitoring and Logging
# Location: 2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.4 Monitoring & Logging

variable "resource_group_name" {
  type        = string
  description = "The name of the resource group where monitoring resources will be created."
  validation {
    condition     = can(regex("^[a-zA-Z0-9-_]{1,90}$", var.resource_group_name))
    error_message = "Resource group name must be 1-90 characters long and can only contain alphanumeric characters, hyphens, and underscores."
  }
}

variable "location" {
  type        = string
  description = "The Azure region where monitoring resources will be created."
  validation {
    condition     = can(regex("^[a-zA-Z0-9-]+$", var.location))
    error_message = "Location must contain only alphanumeric characters and hyphens."
  }
}

variable "log_analytics_workspace_name" {
  type        = string
  description = "The name of the Log Analytics workspace."
  validation {
    condition     = can(regex("^[a-zA-Z0-9-]{4,63}$", var.log_analytics_workspace_name))
    error_message = "Log Analytics workspace name must be 4-63 characters long and can only contain alphanumeric characters and hyphens."
  }
}

variable "application_insights_name" {
  type        = string
  description = "The name of the Application Insights resource."
  validation {
    condition     = can(regex("^[a-zA-Z0-9-]{1,260}$", var.application_insights_name))
    error_message = "Application Insights name must be 1-260 characters long and can only contain alphanumeric characters and hyphens."
  }
}

variable "admin_email" {
  type        = string
  description = "The email address for receiving critical alerts."
  validation {
    condition     = can(regex("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$", var.admin_email))
    error_message = "Please provide a valid email address."
  }
}

variable "app_service_id" {
  type        = string
  description = "The ID of the App Service to be monitored."
  validation {
    condition     = can(regex("^/subscriptions/[a-zA-Z0-9-]+/resourceGroups/[a-zA-Z0-9-_]+/providers/Microsoft.Web/sites/[a-zA-Z0-9-]+$", var.app_service_id))
    error_message = "Please provide a valid App Service ID."
  }
}

variable "retention_in_days" {
  type        = number
  description = "The number of days to retain logs in the Log Analytics workspace."
  default     = 30
  validation {
    condition     = var.retention_in_days >= 30 && var.retention_in_days <= 730
    error_message = "Retention period must be between 30 and 730 days."
  }
}

variable "cpu_threshold" {
  type        = number
  description = "The CPU usage threshold (percentage) for triggering an alert."
  default     = 80
  validation {
    condition     = var.cpu_threshold > 0 && var.cpu_threshold <= 100
    error_message = "CPU threshold must be between 1 and 100 percent."
  }
}

variable "memory_threshold" {
  type        = number
  description = "The memory usage threshold (percentage) for triggering an alert."
  default     = 80
  validation {
    condition     = var.memory_threshold > 0 && var.memory_threshold <= 100
    error_message = "Memory threshold must be between 1 and 100 percent."
  }
}

variable "tags" {
  type        = map(string)
  description = "A mapping of tags to assign to the monitoring resources."
  default     = {}
}

variable "alert_severity" {
  type        = string
  description = "The severity level for alerts (0-4, with 0 being the most severe)."
  default     = "1"
  validation {
    condition     = can(regex("^[0-4]$", var.alert_severity))
    error_message = "Alert severity must be a number between 0 and 4."
  }
}

variable "enable_diagnostic_settings" {
  type        = bool
  description = "Enable diagnostic settings for the monitoring resources."
  default     = true
}

variable "log_categories" {
  type        = list(string)
  description = "List of log categories to enable for diagnostic settings."
  default     = ["Audit", "AllMetrics"]
}

variable "metric_categories" {
  type        = list(string)
  description = "List of metric categories to enable for diagnostic settings."
  default     = ["AllMetrics"]
}