# This file defines input variables for the Azure Function App Terraform module
# It addresses the requirement: "Data Transformation Process"
# Location: 2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.5 Data Processing
# Description: Implement Azure Functions for background processing tasks, such as data transformation and currency conversion

variable "resource_group_name" {
  type        = string
  description = "The name of the resource group in which to create the Function App"
  validation {
    condition     = can(regex("^[a-zA-Z0-9-_]{1,90}$", var.resource_group_name))
    error_message = "The resource group name must be between 1 and 90 characters, and can only contain alphanumeric characters, hyphens, and underscores."
  }
}

variable "location" {
  type        = string
  description = "The Azure region where the Function App should be created"
  validation {
    condition     = can(regex("^[a-zA-Z0-9-]+$", var.location))
    error_message = "The location must be a valid Azure region name."
  }
}

variable "function_app_name" {
  type        = string
  description = "The name of the Function App"
  validation {
    condition     = can(regex("^[a-zA-Z0-9-]{1,60}$", var.function_app_name))
    error_message = "The Function App name must be between 1 and 60 characters, and can only contain alphanumeric characters and hyphens."
  }
}

variable "storage_account_name" {
  type        = string
  description = "The name of the storage account for the Function App"
  validation {
    condition     = can(regex("^[a-z0-9]{3,24}$", var.storage_account_name))
    error_message = "The storage account name must be between 3 and 24 characters, and can only contain lowercase letters and numbers."
  }
}

variable "application_insights_instrumentation_key" {
  type        = string
  description = "The instrumentation key for Application Insights integration"
  sensitive   = true
  validation {
    condition     = can(regex("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", var.application_insights_instrumentation_key))
    error_message = "The Application Insights instrumentation key must be a valid GUID."
  }
}

variable "app_service_plan_id" {
  type        = string
  description = "The ID of the App Service Plan for the Function App"
}

variable "runtime_stack" {
  type        = string
  description = "The runtime stack for the Function App (e.g., 'python', 'node', 'dotnet')"
  default     = "python"
  validation {
    condition     = contains(["python", "node", "dotnet", "java"], var.runtime_stack)
    error_message = "The runtime stack must be one of: python, node, dotnet, or java."
  }
}

variable "runtime_version" {
  type        = string
  description = "The version of the runtime stack"
  default     = "3.9"
}

variable "environment_variables" {
  type        = map(string)
  description = "A map of environment variables to set in the Function App"
  default     = {}
}

variable "tags" {
  type        = map(string)
  description = "A mapping of tags to assign to the Function App"
  default     = {}
}