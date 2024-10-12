# Main Terraform configuration file for the VC firm's financial reporting metrics backend platform
# This file defines the core infrastructure components and modules for the Azure-based backend system.

terraform {
  required_version = ">= 1.0.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 2.0"
    }
  }
  backend "azurerm" {
    resource_group_name  = var.backend_resource_group_name
    storage_account_name = var.backend_storage_account_name
    container_name       = var.backend_container_name
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = true
    }
  }
}

provider "azuread" {}

data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location

  tags = merge(var.tags, {
    Environment = var.environment
    Project     = "VC Financial Reporting Backend"
  })
}

resource "azurerm_virtual_network" "main" {
  name                = "${var.resource_group_name}-vnet"
  address_space       = var.vnet_address_space
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  tags = var.tags
}

resource "azurerm_subnet" "app_service" {
  name                 = "app-service-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = [var.subnet_prefixes.app_service]

  delegation {
    name = "app-service-delegation"
    service_delegation {
      name    = "Microsoft.Web/serverFarms"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

resource "azurerm_subnet" "database" {
  name                 = "database-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = [var.subnet_prefixes.database]
  service_endpoints    = ["Microsoft.Sql"]
}

resource "azurerm_subnet" "function" {
  name                 = "function-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = [var.subnet_prefixes.function]

  delegation {
    name = "function-app-delegation"
    service_delegation {
      name    = "Microsoft.Web/serverFarms"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

module "app_service" {
  source              = "./modules/app_service"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  app_service_plan_name = var.app_service_plan_name
  app_service_name    = var.app_service_name
  subnet_id           = azurerm_subnet.app_service.id
  sku                 = var.sku.app_service_plan
  tags                = var.tags
}

module "database" {
  source              = "./modules/database"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  server_name         = var.db_server_name
  db_name             = var.db_name
  admin_username      = var.db_admin_username
  admin_password      = var.db_admin_password
  subnet_id           = azurerm_subnet.database.id
  sku                 = var.sku.database
  tags                = var.tags
}

module "function_app" {
  source                  = "./modules/function_app"
  resource_group_name     = azurerm_resource_group.main.name
  location                = var.location
  storage_account_name    = var.function_storage_account_name
  function_app_name       = var.function_app_name
  subnet_id               = azurerm_subnet.function.id
  tags                    = var.tags
}

module "key_vault" {
  source              = "./modules/key_vault"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  key_vault_name      = var.key_vault_name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  object_id           = data.azurerm_client_config.current.object_id
  tags                = var.tags
}

module "storage" {
  source                = "./modules/storage"
  resource_group_name   = azurerm_resource_group.main.name
  location              = var.location
  storage_account_name  = var.storage_account_name
  sku                   = var.sku.storage_account
  tags                  = var.tags
}

module "monitoring" {
  source                        = "./modules/monitoring"
  resource_group_name           = azurerm_resource_group.main.name
  location                      = var.location
  log_analytics_workspace_name  = var.log_analytics_workspace_name
  application_insights_name     = var.application_insights_name
  tags                          = var.tags
}

resource "azurerm_network_security_group" "main" {
  name                = "${var.resource_group_name}-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name                       = "AllowHTTPS"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "DenyAllInbound"
    priority                   = 4096
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = var.tags
}

resource "azurerm_subnet_network_security_group_association" "app_service" {
  subnet_id                 = azurerm_subnet.app_service.id
  network_security_group_id = azurerm_network_security_group.main.id
}

resource "azurerm_subnet_network_security_group_association" "database" {
  subnet_id                 = azurerm_subnet.database.id
  network_security_group_id = azurerm_network_security_group.main.id
}

resource "azurerm_subnet_network_security_group_association" "function" {
  subnet_id                 = azurerm_subnet.function.id
  network_security_group_id = azurerm_network_security_group.main.id
}

# Add diagnostic settings for all resources
module "diagnostics" {
  source                     = "./modules/diagnostics"
  resource_group_name        = azurerm_resource_group.main.name
  log_analytics_workspace_id = module.monitoring.log_analytics_workspace_id

  resources = {
    app_service    = module.app_service.app_service_id
    database       = module.database.server_id
    function_app   = module.function_app.function_app_id
    key_vault      = module.key_vault.key_vault_id
    storage        = module.storage.storage_account_id
    vnet           = azurerm_virtual_network.main.id
    nsg            = azurerm_network_security_group.main.id
  }
}

# Azure AD Application for the backend API
resource "azuread_application" "backend_api" {
  display_name = "VC Financial Reporting Backend API"
  owners       = [data.azurerm_client_config.current.object_id]

  api {
    oauth2_permission_scope {
      admin_consent_description  = "Allow the application to access the VC Financial Reporting Backend API on behalf of the signed-in user."
      admin_consent_display_name = "Access VC Financial Reporting Backend API"
      enabled                    = true
      id                         = "00000000-0000-0000-0000-000000000000"
      type                       = "User"
      user_consent_description   = "Allow the application to access the VC Financial Reporting Backend API on your behalf."
      user_consent_display_name  = "Access VC Financial Reporting Backend API"
      value                      = "user_impersonation"
    }
  }

  web {
    homepage_url  = "https://${module.app_service.default_site_hostname}"
    redirect_uris = ["https://${module.app_service.default_site_hostname}/api/docs/oauth2-redirect"]

    implicit_grant {
      access_token_issuance_enabled = true
    }
  }

  required_resource_access {
    resource_app_id = "00000003-0000-0000-c000-000000000000" # Microsoft Graph

    resource_access {
      id   = "e1fe6dd8-ba31-4d61-89e7-88639da4683d" # User.Read
      type = "Scope"
    }
  }
}

resource "azuread_service_principal" "backend_api" {
  application_id = azuread_application.backend_api.application_id
  owners         = [data.azurerm_client_config.current.object_id]
}

# Store sensitive information in Key Vault
resource "azurerm_key_vault_secret" "db_connection_string" {
  name         = "db-connection-string"
  value        = module.database.connection_string
  key_vault_id = module.key_vault.key_vault_id
}

resource "azurerm_key_vault_secret" "function_app_key" {
  name         = "function-app-key"
  value        = module.function_app.function_app_key
  key_vault_id = module.key_vault.key_vault_id
}

# Add role assignments
resource "azurerm_role_assignment" "app_service_kv_access" {
  scope                = module.key_vault.key_vault_id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = module.app_service.app_service_identity_principal_id
}

resource "azurerm_role_assignment" "function_app_kv_access" {
  scope                = module.key_vault.key_vault_id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = module.function_app.function_app_identity_principal_id
}

# Output important information
output "app_service_url" {
  value = "https://${module.app_service.default_site_hostname}"
}

output "function_app_url" {
  value = "https://${module.function_app.default_hostname}"
}

output "application_insights_instrumentation_key" {
  value     = module.monitoring.application_insights_instrumentation_key
  sensitive = true
}