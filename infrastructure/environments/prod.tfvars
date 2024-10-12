# Production Environment Configuration
# Addresses requirement: Production Environment Configuration
# Location: 2. SYSTEM ARCHITECTURE/2.1 High-Level System Architecture

# Backend Configuration
backend_resource_group_name  = "rg-vcfirm-tfstate-prod"
backend_storage_account_name = "savcfirmtfstateprod"
backend_container_name       = "tfstate"

# Resource Group
resource_group_name = "rg-vcfirm-backend-prod"
location            = "eastus2"

# App Service
app_service_plan_name = "asp-vcfirm-backend-prod"
app_service_name      = "app-vcfirm-backend-prod"

# Database
# Addresses requirement: Scalability and Performance for Production
# Location: 2. SYSTEM ARCHITECTURE/2.4 Scalability and Performance Considerations
db_server_name    = "psql-vcfirm-backend-prod"
db_name           = "vcfirm_metrics_prod"
db_admin_username = "vcfirm_admin"
db_admin_password = "${azurerm_key_vault_secret.db_admin_password.value}"

# Function App
function_storage_account_name = "savcfirmfuncprod"
function_app_name             = "func-vcfirm-backend-prod"

# Key Vault
# Addresses requirement: Security Configuration for Production
# Location: 2. SYSTEM ARCHITECTURE/2.5 Security Architecture
key_vault_name = "kv-vcfirm-backend-prod"

# Storage Account
storage_account_name = "savcfirmbackupprod"

# Monitoring
log_analytics_workspace_name = "log-vcfirm-backend-prod"
application_insights_name    = "appi-vcfirm-backend-prod"

# Additional Production-specific configurations
# Addresses requirement: High Availability and Disaster Recovery
# Location: 2. SYSTEM ARCHITECTURE/2.6 High Availability and Disaster Recovery

# App Service Plan configuration
app_service_plan_tier = "PremiumV2"
app_service_plan_size = "P2v2"

# Database configuration
db_sku_name     = "GP_Gen5_4"
db_storage_mb   = 102400
db_backup_retention_days = 35
db_geo_redundant_backup  = "Enabled"

# Function App configuration
function_app_always_on = true

# Storage Account configuration
storage_account_replication_type = "GRS"
storage_account_tier             = "Standard"

# Monitoring configuration
log_retention_in_days = 90

# Network Security
# Addresses requirement: Network Security for Production
# Location: 2. SYSTEM ARCHITECTURE/2.5 Security Architecture
vnet_name                = "vnet-vcfirm-prod"
vnet_address_space       = ["10.0.0.0/16"]
subnet_app_service_name  = "snet-app-service"
subnet_app_service_prefix = ["10.0.1.0/24"]
subnet_database_name     = "snet-database"
subnet_database_prefix   = ["10.0.2.0/24"]

# Note: Sensitive values like database passwords are now referenced from Azure Key Vault secrets.
# The 'location' is set to 'eastus2' as an example, but should be adjusted based on the specific requirements and preferences of the VC firm.
# Resource naming follows a consistent pattern to easily identify production resources.
# These values should be reviewed and approved by the operations team before deployment to ensure they meet all production requirements and best practices.

# TODO: Implement the following in the main Terraform configuration:
# 1. Set up Azure Front Door for global load balancing and WAF protection
# 2. Configure Azure Backup for the database and critical storage accounts
# 3. Implement Azure Security Center for advanced threat protection
# 4. Set up Azure Monitor alerts for critical metrics and logs
# 5. Configure VNet peering if multiple VNets are used in the architecture
# 6. Implement Azure Private Link for secure access to PaaS services
# 7. Set up Azure DDoS Protection Standard for the VNet