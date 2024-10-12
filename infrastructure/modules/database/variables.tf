# Variables definition file for Azure Database for PostgreSQL module
# Addresses requirements:
# - Data Storage Configuration (2. SYSTEM ARCHITECTURE/2.2.2 Data Layer)
# - Database Security (6. SECURITY CONSIDERATIONS/6.2 DATA SECURITY)

variable "resource_group_name" {
  type        = string
  description = "The name of the resource group where the PostgreSQL server will be created"
}

variable "location" {
  type        = string
  description = "The Azure region where the PostgreSQL server will be created"
}

variable "server_name" {
  type        = string
  description = "The name of the Azure Database for PostgreSQL server"
}

variable "database_name" {
  type        = string
  description = "The name of the PostgreSQL database to be created"
}

variable "administrator_login" {
  type        = string
  description = "The administrator username for the PostgreSQL server"
}

variable "administrator_login_password" {
  type        = string
  description = "The administrator password for the PostgreSQL server"
  sensitive   = true
}

variable "subnet_id" {
  type        = string
  description = "The ID of the subnet where the private endpoint will be created"
}

variable "sku_name" {
  type        = string
  description = "The SKU name for the PostgreSQL server (e.g., GP_Gen5_4, MO_Gen5_16, B_Gen5_1)"
  default     = "GP_Gen5_4"
}

variable "storage_mb" {
  type        = number
  description = "The max storage allowed for the PostgreSQL server in megabytes (min 5120 MB, max 1048576 MB)"
  default     = 102400 # 100 GB
}

variable "backup_retention_days" {
  type        = number
  description = "The number of days to retain backups for the PostgreSQL server (between 7 and 35 days)"
  default     = 7
  validation {
    condition     = var.backup_retention_days >= 7 && var.backup_retention_days <= 35
    error_message = "Backup retention days must be between 7 and 35 days."
  }
}

variable "geo_redundant_backup_enabled" {
  type        = bool
  description = "Enable geo-redundant backups for the PostgreSQL server"
  default     = true
}

variable "auto_grow_enabled" {
  type        = bool
  description = "Enable auto-growing of storage for the PostgreSQL server"
  default     = true
}

variable "ssl_enforcement_enabled" {
  type        = bool
  description = "Enforce SSL connection on the PostgreSQL server"
  default     = true
}

variable "public_network_access_enabled" {
  type        = bool
  description = "Enable public network access for the PostgreSQL server (not recommended for production)"
  default     = false
}

variable "postgresql_version" {
  type        = string
  description = "The version of PostgreSQL to use (e.g., '11', '12', '13')"
  default     = "13"
}

variable "tags" {
  type        = map(string)
  description = "A mapping of tags to assign to the resource"
  default     = {}
}

variable "firewall_rules" {
  type = list(object({
    name             = string
    start_ip_address = string
    end_ip_address   = string
  }))
  description = "List of firewall rules to add to the PostgreSQL server"
  default     = []
}

variable "allowed_cidrs" {
  type        = list(string)
  description = "List of CIDR blocks that are allowed to access the PostgreSQL server"
  default     = []
}

variable "enable_threat_detection_policy" {
  type        = bool
  description = "Enable threat detection policy for the PostgreSQL server"
  default     = true
}

variable "log_retention_days" {
  type        = number
  description = "The number of days to retain logs for the PostgreSQL server"
  default     = 7
  validation {
    condition     = var.log_retention_days >= 7 && var.log_retention_days <= 2147483647
    error_message = "Log retention days must be between 7 and 2147483647 days."
  }
}