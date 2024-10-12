# Azure Function App Terraform Module
# This module creates an Azure Function App with associated resources

# Requirement addressed: Data Transformation Process
# Location: 2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.5 Data Processing
# Description: Implement Azure Functions for background processing tasks, such as data transformation and currency conversion

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 2.0"
    }
  }
}

resource "azurerm_storage_account" "function_storage" {
  name                     = var.storage_account_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = var.environment
    purpose     = "function_app_storage"
  }
}

resource "azurerm_app_service_plan" "function_app_service_plan" {
  name                = "${var.function_app_name}-plan"
  resource_group_name = var.resource_group_name
  location            = var.location
  kind                = "FunctionApp"

  sku {
    tier = "Dynamic"
    size = "Y1"
  }

  tags = {
    environment = var.environment
    purpose     = "function_app_service_plan"
  }
}

resource "azurerm_function_app" "function_app" {
  name                       = var.function_app_name
  resource_group_name        = var.resource_group_name
  location                   = var.location
  app_service_plan_id        = azurerm_app_service_plan.function_app_service_plan.id
  storage_account_name       = azurerm_storage_account.function_storage.name
  storage_account_access_key = azurerm_storage_account.function_storage.primary_access_key
  version                    = "~4"  # Updated to latest major version

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME       = "python"
    APPINSIGHTS_INSTRUMENTATIONKEY = var.application_insights_instrumentation_key
    WEBSITE_RUN_FROM_PACKAGE       = "1"  # Enable run from package
  }

  site_config {
    python_version = "3.9"
    ftps_state     = "Disabled"  # Disable FTPS for security
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    environment = var.environment
    purpose     = "data_transformation"
  }
}

resource "azurerm_key_vault" "function_key_vault" {
  name                       = "${var.function_app_name}-kv"
  resource_group_name        = var.resource_group_name
  location                   = var.location
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  soft_delete_retention_days = 7
  purge_protection_enabled   = false

  tags = {
    environment = var.environment
    purpose     = "function_app_secrets"
  }
}

resource "azurerm_key_vault_access_policy" "function_app_key_vault_access" {
  key_vault_id = azurerm_key_vault.function_key_vault.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = azurerm_function_app.function_app.identity[0].principal_id

  secret_permissions = [
    "Get",
    "List"
  ]
}

data "azurerm_client_config" "current" {}

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