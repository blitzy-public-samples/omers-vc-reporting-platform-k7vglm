# This file defines the input variables for the Azure Key Vault module.
# It addresses the Security requirement specified in the System Architecture section 2.5.
# The variables defined here are used in the main.tf file to configure the Azure Key Vault resource.

variable "key_vault_name" {
  type        = string
  description = "The name of the Azure Key Vault"
  validation {
    condition     = can(regex("^[a-zA-Z0-9-]{3,24}$", var.key_vault_name))
    error_message = "The key_vault_name must be between 3 and 24 characters long and can only contain alphanumeric characters and hyphens."
  }
}

variable "location" {
  type        = string
  description = "The Azure region where the Key Vault should be created"
}

variable "resource_group_name" {
  type        = string
  description = "The name of the resource group in which to create the Key Vault"
}

variable "sku_name" {
  type        = string
  description = "The SKU name of the Key Vault (standard or premium)"
  default     = "standard"
  validation {
    condition     = contains(["standard", "premium"], var.sku_name)
    error_message = "The sku_name must be either 'standard' or 'premium'."
  }
}

variable "soft_delete_retention_days" {
  type        = number
  description = "The number of days that items should be retained for once soft-deleted"
  default     = 90
  validation {
    condition     = var.soft_delete_retention_days >= 7 && var.soft_delete_retention_days <= 90
    error_message = "The soft_delete_retention_days must be between 7 and 90 days."
  }
}

variable "purge_protection_enabled" {
  type        = bool
  description = "Enable purge protection for the Key Vault"
  default     = true
}

variable "enabled_for_disk_encryption" {
  type        = bool
  description = "Allow Azure Disk Encryption to retrieve secrets from the vault and unwrap keys"
  default     = false
}

variable "enabled_for_deployment" {
  type        = bool
  description = "Allow Azure Virtual Machines to retrieve certificates stored as secrets from the vault"
  default     = false
}

variable "enabled_for_template_deployment" {
  type        = bool
  description = "Allow Azure Resource Manager to retrieve secrets from the vault"
  default     = false
}

variable "access_policies" {
  type = list(object({
    tenant_id               = string
    object_id               = string
    key_permissions         = list(string)
    secret_permissions      = list(string)
    certificate_permissions = list(string)
    storage_permissions     = list(string)
  }))
  description = "List of access policies for the Key Vault"
  default     = []
  validation {
    condition = alltrue([
      for policy in var.access_policies : can(regex("^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$", policy.tenant_id)) &&
      can(regex("^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$", policy.object_id))
    ])
    error_message = "The tenant_id and object_id in access_policies must be valid UUIDs."
  }
}

variable "network_acls" {
  type = object({
    default_action             = string
    bypass                     = string
    ip_rules                   = list(string)
    virtual_network_subnet_ids = list(string)
  })
  description = "Network ACLs for the Key Vault"
  default = {
    default_action             = "Deny"
    bypass                     = "AzureServices"
    ip_rules                   = []
    virtual_network_subnet_ids = []
  }
  validation {
    condition     = contains(["Allow", "Deny"], var.network_acls.default_action)
    error_message = "The default_action in network_acls must be either 'Allow' or 'Deny'."
  }
  validation {
    condition     = contains(["AzureServices", "None"], var.network_acls.bypass)
    error_message = "The bypass in network_acls must be either 'AzureServices' or 'None'."
  }
}

variable "environment" {
  type        = string
  description = "The environment in which the Key Vault is being deployed (e.g., dev, staging, prod)"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "The environment must be one of: dev, staging, prod."
  }
}

variable "project_name" {
  type        = string
  description = "The name of the project associated with this Key Vault"
}

variable "tags" {
  type        = map(string)
  description = "A mapping of tags to assign to the Key Vault"
  default     = {}
}

variable "enable_rbac_authorization" {
  type        = bool
  description = "Specify whether Azure Key Vault uses Role Based Access Control (RBAC) for authorization of data actions"
  default     = false
}

variable "public_network_access_enabled" {
  type        = bool
  description = "Whether public network access is allowed for this Key Vault"
  default     = false
}