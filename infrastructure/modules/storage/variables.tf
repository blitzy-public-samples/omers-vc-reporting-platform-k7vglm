# This file defines the input variables for the Azure Blob Storage module used in the VC firm's financial reporting metrics backend platform.
# It addresses requirements for Data Archiving and Retention, Scalability and Performance, and Security.

# Resource Group Name
# Requirement addressed: Data Archiving and Retention
# Location: 2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.6 Storage
variable "resource_group_name" {
  type        = string
  description = "The name of the resource group in which to create the storage account."
}

# Azure Region
# Requirement addressed: Scalability and Performance
# Location: 2. SYSTEM ARCHITECTURE/2.4 Scalability and Performance Considerations
variable "location" {
  type        = string
  description = "The Azure region where the storage account should be created."
}

# Storage Account Name
# Requirement addressed: Data Archiving and Retention
# Location: 2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.6 Storage
variable "storage_account_name" {
  type        = string
  description = "The name of the storage account. Must be globally unique, between 3 and 24 characters in length and use numbers and lower-case letters only."
  validation {
    condition     = can(regex("^[a-z0-9]{3,24}$", var.storage_account_name))
    error_message = "The storage account name must be between 3 and 24 characters in length and use numbers and lower-case letters only."
  }
}

# Account Tier
# Requirement addressed: Scalability and Performance
# Location: 2. SYSTEM ARCHITECTURE/2.4 Scalability and Performance Considerations
variable "account_tier" {
  type        = string
  description = "The performance tier of the storage account (Standard or Premium)."
  default     = "Standard"
  validation {
    condition     = contains(["Standard", "Premium"], var.account_tier)
    error_message = "The account tier must be either 'Standard' or 'Premium'."
  }
}

# Account Replication Type
# Requirement addressed: Data Archiving and Retention, Scalability and Performance
# Location: 2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.6 Storage, 2.4 Scalability and Performance Considerations
variable "account_replication_type" {
  type        = string
  description = "The type of replication to use for the storage account (LRS, GRS, RAGRS, ZRS)."
  default     = "GRS"
  validation {
    condition     = contains(["LRS", "GRS", "RAGRS", "ZRS"], var.account_replication_type)
    error_message = "The account replication type must be one of 'LRS', 'GRS', 'RAGRS', or 'ZRS'."
  }
}

# Account Kind
# Requirement addressed: Scalability and Performance
# Location: 2. SYSTEM ARCHITECTURE/2.4 Scalability and Performance Considerations
variable "account_kind" {
  type        = string
  description = "The kind of storage account (StorageV2, FileStorage, or BlobStorage)."
  default     = "StorageV2"
  validation {
    condition     = contains(["StorageV2", "FileStorage", "BlobStorage"], var.account_kind)
    error_message = "The account kind must be one of 'StorageV2', 'FileStorage', or 'BlobStorage'."
  }
}

# HTTPS Traffic Only
# Requirement addressed: Security
# Location: 2. SYSTEM ARCHITECTURE/2.5 Security Architecture
variable "enable_https_traffic_only" {
  type        = bool
  description = "Boolean flag to allow https traffic only to storage service."
  default     = true
}

# Minimum TLS Version
# Requirement addressed: Security
# Location: 2. SYSTEM ARCHITECTURE/2.5 Security Architecture
variable "min_tls_version" {
  type        = string
  description = "The minimum supported TLS version for the storage account."
  default     = "TLS1_2"
  validation {
    condition     = contains(["TLS1_0", "TLS1_1", "TLS1_2"], var.min_tls_version)
    error_message = "The minimum TLS version must be one of 'TLS1_0', 'TLS1_1', or 'TLS1_2'."
  }
}

# Allow Blob Public Access
# Requirement addressed: Security
# Location: 2. SYSTEM ARCHITECTURE/2.5 Security Architecture
variable "allow_blob_public_access" {
  type        = bool
  description = "Allow or disallow public access to all blobs or containers in the storage account."
  default     = false
}

# Network Rules
# Requirement addressed: Security
# Location: 2. SYSTEM ARCHITECTURE/2.5 Security Architecture
variable "network_rules" {
  type = object({
    default_action             = string
    ip_rules                   = list(string)
    virtual_network_subnet_ids = list(string)
  })
  description = "Network rules restricting access to the storage account."
  default = {
    default_action             = "Deny"
    ip_rules                   = []
    virtual_network_subnet_ids = []
  }
  validation {
    condition     = contains(["Allow", "Deny"], var.network_rules.default_action)
    error_message = "The default action must be either 'Allow' or 'Deny'."
  }
}

# Archive Container Name
# Requirement addressed: Data Archiving and Retention
# Location: 2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.6 Storage
variable "archive_container_name" {
  type        = string
  description = "Name of the container for archived data."
  default     = "archive"
  validation {
    condition     = can(regex("^[a-z0-9](?!.*--)[a-z0-9-]{1,61}[a-z0-9]$", var.archive_container_name))
    error_message = "The archive container name must be between 3 and 63 characters, start with a letter or number, and can contain only lowercase letters, numbers, and hyphens (-)."
  }
}

# Backups Container Name
# Requirement addressed: Data Archiving and Retention
# Location: 2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.6 Storage
variable "backups_container_name" {
  type        = string
  description = "Name of the container for database backups."
  default     = "backups"
  validation {
    condition     = can(regex("^[a-z0-9](?!.*--)[a-z0-9-]{1,61}[a-z0-9]$", var.backups_container_name))
    error_message = "The backups container name must be between 3 and 63 characters, start with a letter or number, and can contain only lowercase letters, numbers, and hyphens (-)."
  }
}

# Lifecycle Rules
# Requirement addressed: Data Archiving and Retention, Scalability and Performance
# Location: 2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.6 Storage, 2.4 Scalability and Performance Considerations
variable "lifecycle_rules" {
  type = list(object({
    name    = string
    enabled = bool
    filters = object({
      prefix_match = list(string)
      blob_types   = list(string)
    })
    actions = object({
      base_blob = object({
        tier_to_cool_after_days    = number
        tier_to_archive_after_days = number
        delete_after_days          = number
      })
    })
  }))
  description = "Lifecycle management policy rules for blob storage."
  default = [
    {
      name    = "archive_old_data"
      enabled = true
      filters = {
        prefix_match = ["archive/"]
        blob_types   = ["blockBlob"]
      }
      actions = {
        base_blob = {
          tier_to_cool_after_days    = 30
          tier_to_archive_after_days = 90
          delete_after_days          = 2555
        }
      }
    }
  ]
  validation {
    condition = alltrue([
      for rule in var.lifecycle_rules :
      rule.name != null &&
      rule.enabled != null &&
      rule.filters != null &&
      rule.actions != null &&
      rule.actions.base_blob != null &&
      rule.actions.base_blob.tier_to_cool_after_days >= 0 &&
      rule.actions.base_blob.tier_to_archive_after_days >= 0 &&
      rule.actions.base_blob.delete_after_days >= 0
    ])
    error_message = "Each lifecycle rule must have a name, enabled flag, filters, and valid actions with non-negative day values."
  }
}

# Encryption Settings
# Requirement addressed: Security
# Location: 2. SYSTEM ARCHITECTURE/2.5 Security Architecture
variable "encryption_settings" {
  type = object({
    key_source = string
    key_vault_key_id = string
  })
  description = "Encryption settings for the storage account."
  default = {
    key_source = "Microsoft.Storage"
    key_vault_key_id = null
  }
  validation {
    condition     = contains(["Microsoft.Storage", "Microsoft.Keyvault"], var.encryption_settings.key_source)
    error_message = "The encryption key source must be either 'Microsoft.Storage' or 'Microsoft.Keyvault'."
  }
}

# Tags
# Requirement addressed: Operational Efficiency
# Location: 2. SYSTEM ARCHITECTURE/2.6 Operational Considerations
variable "tags" {
  type        = map(string)
  description = "A mapping of tags to assign to the resource."
  default     = {}
}