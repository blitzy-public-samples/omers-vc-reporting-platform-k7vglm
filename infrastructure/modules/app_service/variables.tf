# This file defines the input variables for the Azure App Service module.
# It addresses the following requirements:
# - Application Hosting Configuration (2. SYSTEM ARCHITECTURE/2.1 High-Level System Architecture)
# - Scalability Configuration (2. SYSTEM ARCHITECTURE/2.4 Scalability and Performance Considerations)
# - Security Configuration (6. SECURITY CONSIDERATIONS/6.2 Data Security)

variable "resource_group_name" {
  type        = string
  description = "The name of the resource group in which to create the App Service."
}

variable "location" {
  type        = string
  description = "The Azure region in which to create the App Service."
}

variable "app_service_plan_name" {
  type        = string
  description = "The name of the App Service Plan."
}

variable "app_service_name" {
  type        = string
  description = "The name of the App Service."
}

variable "sku_tier" {
  type        = string
  description = "The SKU tier of the App Service Plan."
  default     = "PremiumV2"
}

variable "sku_size" {
  type        = string
  description = "The SKU size of the App Service Plan."
  default     = "P1v2"
}

variable "docker_image" {
  type        = string
  description = "The Docker image to use for the App Service."
  default     = "mcr.microsoft.com/appsvc/staticsite:latest"
}

variable "allowed_origins" {
  type        = list(string)
  description = "A list of origins that should be allowed to make cross-origin calls."
  default     = ["*"]
}

# Additional variables for enhanced security and scalability

variable "https_only" {
  type        = bool
  description = "Require HTTPS for the App Service."
  default     = true
}

variable "min_tls_version" {
  type        = string
  description = "The minimum supported TLS version for the App Service."
  default     = "1.2"
}

variable "ftps_state" {
  type        = string
  description = "The FTPS state for the App Service. Valid values are: AllAllowed, FtpsOnly, and Disabled."
  default     = "Disabled"
}

variable "health_check_path" {
  type        = string
  description = "The health check path for the App Service."
  default     = "/health"
}

variable "always_on" {
  type        = bool
  description = "Ensure the App Service is always on."
  default     = true
}

variable "use_32_bit_worker_process" {
  type        = bool
  description = "Use a 32-bit worker process. Set to false for 64-bit worker process."
  default     = false
}

variable "websockets_enabled" {
  type        = bool
  description = "Enable WebSockets for the App Service."
  default     = false
}

variable "app_settings" {
  type        = map(string)
  description = "A map of app settings to configure on the App Service."
  default     = {}
}

variable "connection_strings" {
  type = list(object({
    name  = string
    type  = string
    value = string
  }))
  description = "A list of connection strings to configure on the App Service."
  default     = []
}

variable "ip_restriction" {
  type = list(object({
    ip_address = string
    subnet_id  = string
  }))
  description = "A list of IP restrictions for the App Service."
  default     = []
}

variable "tags" {
  type        = map(string)
  description = "A mapping of tags to assign to the resources."
  default     = {}
}

variable "auto_scale_default_instances" {
  type        = number
  description = "The default number of instances for auto-scaling."
  default     = 1
}

variable "auto_scale_minimum_instances" {
  type        = number
  description = "The minimum number of instances for auto-scaling."
  default     = 1
}

variable "auto_scale_maximum_instances" {
  type        = number
  description = "The maximum number of instances for auto-scaling."
  default     = 10
}

variable "enable_backup" {
  type        = bool
  description = "Enable backup for the App Service."
  default     = true
}

variable "backup_frequency_interval" {
  type        = number
  description = "Frequency interval for backup (in hours)."
  default     = 24
}

variable "backup_retention_period_in_days" {
  type        = number
  description = "Retention period for backups (in days)."
  default     = 30
}