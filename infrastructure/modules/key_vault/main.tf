# Azure Key Vault Module
# This module creates an Azure Key Vault for secure management of secrets and encryption keys
# Requirements addressed:
# - Security: Implement Azure Key Vault for secure management of secrets and encryption keys
#   Location: 2. SYSTEM ARCHITECTURE/2.5 Security Architecture

terraform {
  required_version = ">= 0.13.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 2.65.0"
    }
  }
}

# Data source to get the current Azure client configuration
data "azurerm_client_config" "current" {}

# Local variables for common tags and naming convention
locals {
  common_tags = merge(var.common_tags, {
    environment   = var.environment
    project       = var.project_name
    resource_type = "Key Vault"
  })
  key_vault_name = lower("kv-${var.project_name}-${var.environment}-${var.location_short}")
}

# Azure Key Vault resource
resource "azurerm_key_vault" "main" {
  name                = local.key_vault_name
  location            = var.location
  resource_group_name = var.resource_group_name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = var.sku_name

  soft_delete_retention_days  = var.soft_delete_retention_days
  purge_protection_enabled    = var.purge_protection_enabled
  enabled_for_disk_encryption = var.enabled_for_disk_encryption
  enabled_for_deployment      = var.enabled_for_deployment
  enabled_for_template_deployment = var.enabled_for_template_deployment

  network_acls {
    default_action             = var.network_acls_default_action
    bypass                     = var.network_acls_bypass
    ip_rules                   = var.network_acls_ip_rules
    virtual_network_subnet_ids = var.network_acls_subnet_ids
  }

  # Dynamic block for access policies
  dynamic "access_policy" {
    for_each = var.access_policies
    content {
      tenant_id               = access_policy.value.tenant_id
      object_id               = access_policy.value.object_id
      application_id          = lookup(access_policy.value, "application_id", null)
      key_permissions         = access_policy.value.key_permissions
      secret_permissions      = access_policy.value.secret_permissions
      certificate_permissions = access_policy.value.certificate_permissions
      storage_permissions     = lookup(access_policy.value, "storage_permissions", null)
    }
  }

  tags = local.common_tags

  lifecycle {
    prevent_destroy = true
  }
}

# Azure Monitor Diagnostic Setting for Key Vault
resource "azurerm_monitor_diagnostic_setting" "key_vault" {
  name                       = "key-vault-diagnostics"
  target_resource_id         = azurerm_key_vault.main.id
  log_analytics_workspace_id = var.log_analytics_workspace_id

  log {
    category = "AuditEvent"
    enabled  = true

    retention_policy {
      enabled = true
      days    = 30
    }
  }

  metric {
    category = "AllMetrics"
    enabled  = true

    retention_policy {
      enabled = true
      days    = 30
    }
  }
}