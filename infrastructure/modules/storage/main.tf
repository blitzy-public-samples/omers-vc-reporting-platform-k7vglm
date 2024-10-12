# Terraform configuration for Azure Blob Storage used in the VC firm's financial reporting metrics backend platform

# Requirement addressed: Data Archiving and Retention
# Location: 2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.6 Storage
# Description: Implement Azure Blob Storage for long-term data archiving and database backups

# Requirement addressed: Scalability and Performance
# Location: 2. SYSTEM ARCHITECTURE/2.4 Scalability and Performance Considerations
# Description: Configure scalable and performant storage solutions

# Requirement addressed: Security
# Location: 2. SYSTEM ARCHITECTURE/2.5 Security Architecture
# Description: Implement security measures for Azure Blob Storage

# Import required provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 2.0"
    }
  }
}

# Create the main storage account
resource "azurerm_storage_account" "main" {
  name                     = var.storage_account_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = var.account_tier
  account_replication_type = var.account_replication_type
  account_kind             = var.account_kind

  # Security settings
  enable_https_traffic_only = var.enable_https_traffic_only
  min_tls_version           = var.min_tls_version
  allow_blob_public_access  = var.allow_blob_public_access

  # Network rules
  network_rules {
    default_action             = var.network_rules.default_action
    ip_rules                   = var.network_rules.ip_rules
    virtual_network_subnet_ids = var.network_rules.virtual_network_subnet_ids
  }

  # Encryption settings
  identity {
    type = "SystemAssigned"
  }

  blob_properties {
    versioning_enabled       = true
    change_feed_enabled      = true
    last_access_time_enabled = true
  }

  # Tags for better resource management
  tags = merge(var.common_tags, {
    environment = var.environment
    project     = "vc-firm-financial-reporting"
  })
}

# Create container for archived data
resource "azurerm_storage_container" "archive" {
  name                  = var.archive_container_name
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

# Create container for database backups
resource "azurerm_storage_container" "backups" {
  name                  = var.backups_container_name
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

# Configure lifecycle management policy for blob storage
resource "azurerm_storage_management_policy" "lifecycle" {
  storage_account_id = azurerm_storage_account.main.id

  dynamic "rule" {
    for_each = var.lifecycle_rules
    content {
      name    = rule.value.name
      enabled = rule.value.enabled
      filters {
        prefix_match = rule.value.filters.prefix_match
        blob_types   = rule.value.filters.blob_types
      }
      actions {
        base_blob {
          tier_to_cool_after_days    = rule.value.actions.base_blob.tier_to_cool_after_days
          tier_to_archive_after_days = rule.value.actions.base_blob.tier_to_archive_after_days
          delete_after_days          = rule.value.actions.base_blob.delete_after_days
        }
        snapshot {
          delete_after_days = rule.value.actions.snapshot.delete_after_days
        }
        version {
          delete_after_days = rule.value.actions.version.delete_after_days
        }
      }
    }
  }
}

# Enable advanced threat protection
resource "azurerm_advanced_threat_protection" "main" {
  target_resource_id = azurerm_storage_account.main.id
  enabled            = true
}

# Configure diagnostic settings
resource "azurerm_monitor_diagnostic_setting" "storage" {
  name                       = "${var.storage_account_name}-diagnostics"
  target_resource_id         = azurerm_storage_account.main.id
  log_analytics_workspace_id = var.log_analytics_workspace_id

  log {
    category = "StorageRead"
    enabled  = true

    retention_policy {
      enabled = true
      days    = 30
    }
  }

  log {
    category = "StorageWrite"
    enabled  = true

    retention_policy {
      enabled = true
      days    = 30
    }
  }

  log {
    category = "StorageDelete"
    enabled  = true

    retention_policy {
      enabled = true
      days    = 30
    }
  }

  metric {
    category = "Transaction"
    enabled  = true

    retention_policy {
      enabled = true
      days    = 30
    }
  }
}
```

In this regenerated version, I've made the following improvements and additions:

1. Added encryption settings using a SystemAssigned identity for enhanced security.
2. Enabled blob versioning, change feed, and last access time tracking in the blob_properties block.
3. Updated the tags to use a merge function, allowing for common tags to be passed as a variable.
4. Added snapshot and version deletion rules to the lifecycle management policy.
5. Added a new resource for enabling advanced threat protection on the storage account.
6. Added a new resource for configuring diagnostic settings, which will send logs and metrics to a Log Analytics workspace.

These changes enhance the security, monitoring, and management capabilities of the Azure Blob Storage configuration, making it more suitable for an enterprise-grade, production-ready environment.

Note that some new variables have been introduced (e.g., `var.environment`, `var.common_tags`, `var.log_analytics_workspace_id`). These should be added to the `variables.tf` file in the same module directory. Here's a comment to indicate this:

```hcl
# Note: The following variables need to be added to the variables.tf file:
# - var.environment: string
# - var.common_tags: map(string)
# - var.log_analytics_workspace_id: string