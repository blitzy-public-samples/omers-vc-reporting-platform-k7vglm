# This file contains staging-specific values for the VC firm's backend platform
# Sensitive values are referenced from Azure Key Vault secrets for enhanced security
# Resource naming follows a consistent pattern: <resource-type>-vcfirm-backend-staging
# Storage account names use 'sa' prefix due to naming restrictions (no hyphens allowed)

# Backend configuration
backend_resource_group_name     = "rg-vcfirm-tfstate-staging"
backend_storage_account_name    = "savcfirmtfstatestaging"
backend_container_name          = "tfstate"
backend_key                     = "staging.terraform.tfstate"

# Resource group
resource_group_name             = "rg-vcfirm-backend-staging"
location                        = "eastus"

# Tags
common_tags = {
  Environment = "Staging"
  Project     = "VC Firm Backend"
  ManagedBy   = "Terraform"
}

# App Service
app_service_plan_name           = "asp-vcfirm-backend-staging"
app_service_name                = "app-vcfirm-backend-staging"
app_service_sku                 = "P1v2"
app_service_always_on           = true

# Database
db_server_name                  = "psql-vcfirm-backend-staging"
db_name                         = "vcfirmdbstaging"
db_admin_username               = "vcfirmadmin"
db_admin_password               = "@Microsoft.KeyVault(SecretUri=https://kv-vcfirm-backend-staging.vault.azure.net/secrets/db-admin-password/)"
db_sku_name                     = "GP_Gen5_2"
db_storage_mb                   = 5120
db_backup_retention_days        = 7
db_geo_redundant_backup_enabled = false
db_auto_grow_enabled            = true
db_public_network_access_enabled = false
db_ssl_enforcement_enabled      = true
db_ssl_minimal_tls_version_enforced = "TLS1_2"

# Function App
function_storage_account_name   = "savcfirmfuncstaging"
function_app_name               = "func-vcfirm-backend-staging"
function_app_sku                = "EP1"
function_app_os_type            = "linux"
function_app_runtime_stack      = "python"
function_app_python_version     = "3.9"

# Key Vault
key_vault_name                  = "kv-vcfirm-backend-staging"
key_vault_sku                   = "standard"
key_vault_enabled_for_disk_encryption = true
key_vault_soft_delete_retention_days  = 90

# Storage Account
storage_account_name            = "savcfirmbackendstaging"
storage_account_tier            = "Standard"
storage_account_replication_type = "GRS"
storage_account_min_tls_version = "TLS1_2"
storage_account_allow_blob_public_access = false

# Monitoring
log_analytics_workspace_name    = "log-vcfirm-backend-staging"
log_analytics_sku               = "PerGB2018"
log_retention_in_days           = 30
application_insights_name       = "appi-vcfirm-backend-staging"
application_insights_type       = "web"

# Network
vnet_name                       = "vnet-vcfirm-backend-staging"
vnet_address_space              = ["10.0.0.0/16"]
subnet_app_service_name         = "snet-app-service"
subnet_app_service_prefix       = ["10.0.1.0/24"]
subnet_function_app_name        = "snet-function-app"
subnet_function_app_prefix      = ["10.0.2.0/24"]
subnet_database_name            = "snet-database"
subnet_database_prefix          = ["10.0.3.0/24"]

# Security
ip_restriction_allow_list       = ["203.0.113.0/24", "198.51.100.0/24"]  # Example IP ranges, replace with actual allowed IPs