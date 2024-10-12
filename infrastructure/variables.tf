# infrastructure/variables.tf

# This file defines the variables used in the Terraform configuration for the
# VC firm's financial reporting metrics backend platform.

# Backend Configuration Variables
variable "backend_resource_group_name" {
  type        = string
  description = "The name of the resource group for the Terraform backend storage"
}

variable "backend_storage_account_name" {
  type        = string
  description = "The name of the storage account for the Terraform backend"
}

variable "backend_container_name" {
  type        = string
  description = "The name of the container in the storage account for the Terraform backend"
}

# Main Resource Group
variable "resource_group_name" {
  type        = string
  description = "The name of the main resource group for the project"
}

variable "location" {
  type        = string
  description = "The Azure region where resources will be created"
}

# App Service Plan and App Service
variable "app_service_plan_name" {
  type        = string
  description = "The name of the App Service Plan for hosting the FastAPI application"
}

variable "app_service_name" {
  type        = string
  description = "The name of the App Service for the FastAPI application"
}

# Database
variable "db_server_name" {
  type        = string
  description = "The name of the Azure Database for PostgreSQL server"
}

variable "db_name" {
  type        = string
  description = "The name of the PostgreSQL database"
}

variable "db_admin_username" {
  type        = string
  description = "The admin username for the PostgreSQL database"
}

variable "db_admin_password" {
  type        = string
  description = "The admin password for the PostgreSQL database"
  sensitive   = true
}

# Function App
variable "function_storage_account_name" {
  type        = string
  description = "The name of the storage account for Azure Functions"
}

variable "function_app_name" {
  type        = string
  description = "The name of the Azure Function App for data transformation processes"
}

# Key Vault
variable "key_vault_name" {
  type        = string
  description = "The name of the Azure Key Vault for secrets management"
}

# Storage Account
variable "storage_account_name" {
  type        = string
  description = "The name of the storage account for data archiving and backups"
}

# Monitoring
variable "log_analytics_workspace_name" {
  type        = string
  description = "The name of the Log Analytics workspace for monitoring"
}

variable "application_insights_name" {
  type        = string
  description = "The name of the Application Insights resource for application monitoring"
}

# Environment
variable "environment" {
  type        = string
  description = "The environment name (e.g., dev, staging, prod)"
  default     = "dev"
}

# Tags
variable "tags" {
  type        = map(string)
  description = "A map of tags to apply to all resources"
  default     = {}
}

# SKUs
variable "sku" {
  type = object({
    app_service_plan = string
    database         = string
    storage_account  = string
  })
  description = "The SKUs for various Azure resources"
  default = {
    app_service_plan = "P1v2"
    database         = "GP_Gen5_2"
    storage_account  = "Standard_LRS"
  }
}

# Virtual Network
variable "vnet_address_space" {
  type        = list(string)
  description = "The address space for the Virtual Network"
  default     = ["10.0.0.0/16"]
}

# Subnets
variable "subnet_prefixes" {
  type = object({
    app_service = string
    database    = string
    function    = string
  })
  description = "The address prefixes for the subnets"
  default = {
    app_service = "10.0.1.0/24"
    database    = "10.0.2.0/24"
    function    = "10.0.3.0/24"
  }
}

# CORS Configuration
variable "allowed_origins" {
  type        = list(string)
  description = "List of allowed origins for CORS configuration"
  default     = ["*"]
}

# SSL Configuration
variable "ssl_state" {
  type        = string
  description = "The SSL state for the App Service"
  default     = "SniEnabled"
}

variable "min_tls_version" {
  type        = string
  description = "The minimum supported TLS version for the App Service"
  default     = "1.2"
}

# Scaling Configuration
variable "app_service_plan_tier" {
  type        = string
  description = "The tier of the App Service Plan"
  default     = "PremiumV2"
}

variable "app_service_plan_size" {
  type        = string
  description = "The size of the App Service Plan"
  default     = "P1v2"
}

# Database Configuration
variable "db_version" {
  type        = string
  description = "The version of PostgreSQL to use"
  default     = "11"
}

variable "db_sku_name" {
  type        = string
  description = "The SKU name for the PostgreSQL server"
  default     = "GP_Gen5_2"
}

variable "db_storage_mb" {
  type        = number
  description = "The max storage allowed for the PostgreSQL server in megabytes"
  default     = 5120
}

# Function App Configuration
variable "function_app_version" {
  type        = string
  description = "The runtime version of the Function App"
  default     = "~3"
}

# Key Vault Access Policies
variable "key_vault_access_policies" {
  type = list(object({
    object_id               = string
    certificate_permissions = list(string)
    key_permissions         = list(string)
    secret_permissions      = list(string)
    storage_permissions     = list(string)
  }))
  description = "List of access policies for the Key Vault"
  default     = []
}

# Monitoring Configuration
variable "retention_in_days" {
  type        = number
  description = "The number of days to retain logs in the Log Analytics workspace"
  default     = 30
}

# Backup Configuration
variable "backup_enabled" {
  type        = bool
  description = "Whether to enable automated backups for the database"
  default     = true
}

variable "backup_retention_days" {
  type        = number
  description = "The number of days to retain backups"
  default     = 7
}

# Rate Limiting
variable "rate_limit_requests" {
  type        = number
  description = "The number of requests allowed per time window for rate limiting"
  default     = 100
}

variable "rate_limit_window" {
  type        = string
  description = "The time window for rate limiting (e.g., '1m', '1h')"
  default     = "1m"
}