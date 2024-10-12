# Development environment-specific values for the VC firm's financial reporting metrics backend platform
# This file contains values for variables defined in ../variables.tf

# Requirement addressed: Environment-specific Configuration
# Location: 2. SYSTEM ARCHITECTURE/2.1 High-Level System Architecture

# Backend configuration
backend_resource_group_name     = "rg-vcfirm-tfstate-dev"
backend_storage_account_name    = "stvcfirmtfstatedev"
backend_container_name          = "tfstate"
backend_key                     = "dev.terraform.tfstate"

# Main resource group
resource_group_name = "rg-vcfirm-backend-dev"
location            = "eastus"

# App Service
app_service_plan_name = "asp-vcfirm-backend-dev"
app_service_name      = "app-vcfirm-backend-dev"
app_service_sku       = {
  tier = "Standard"
  size = "S1"
}

# Database
db_server_name    = "psql-vcfirm-backend-dev"
db_name           = "vcfirm_metrics_dev"
db_admin_username = "vcfirm_admin"
db_admin_password = "PLACEHOLDER_PASSWORD" # Note: Replace with actual secure password before deployment or use Azure Key Vault reference
db_sku_name       = "GP_Gen5_2"
db_storage_mb     = 5120

# Requirement addressed: Scalability and Performance for Development
# Location: 2. SYSTEM ARCHITECTURE/2.4 Scalability and Performance Considerations

# Function App
function_storage_account_name = "stvcfirmfuncdev"
function_app_name             = "func-vcfirm-backend-dev"
function_app_sku              = "Y1"
function_app_worker_count     = 1

# Requirement addressed: Security Configuration for Development
# Location: 2. SYSTEM ARCHITECTURE/2.5 Security Architecture

# Key Vault
key_vault_name = "kv-vcfirm-backend-dev"
key_vault_sku  = "standard"

# Storage Account for data archiving and backups
storage_account_name = "stvcfirmbackenddev"
storage_account_tier = "Standard"
storage_account_replication_type = "LRS"

# Monitoring
log_analytics_workspace_name = "log-vcfirm-backend-dev"
application_insights_name    = "appi-vcfirm-backend-dev"

# Network configuration
vnet_name          = "vnet-vcfirm-backend-dev"
vnet_address_space = ["10.0.0.0/16"]
subnet_names       = ["subnet-app", "subnet-db", "subnet-func"]
subnet_prefixes    = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]

# Tags
default_tags = {
  Environment = "Development"
  Project     = "VC Firm Financial Reporting"
  ManagedBy   = "Terraform"
}

# Note: This file contains development environment-specific values for the variables defined in variables.tf
# Sensitive values like db_admin_password should be replaced with actual values securely, possibly using Azure Key Vault or other secure methods
# Resource naming follows a consistent pattern: [resource-type]-vcfirm-backend-dev
# The 'dev' suffix in resource names indicates that these are for the development environment