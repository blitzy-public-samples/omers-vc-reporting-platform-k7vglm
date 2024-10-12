# Azure Database for PostgreSQL Terraform Configuration
# This file defines the resources for creating and managing an Azure Database for PostgreSQL instance
# Requirements addressed:
# - Data Storage Implementation (2. SYSTEM ARCHITECTURE/2.2.2 Data Layer)
# - Database Security (6. SECURITY CONSIDERATIONS/6.2 DATA SECURITY)

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"  # Updated to the latest major version
    }
  }
}

resource "azurerm_postgresql_server" "main" {
  name                = var.server_name
  location            = var.location
  resource_group_name = var.resource_group_name

  administrator_login          = var.administrator_login
  administrator_login_password = var.administrator_login_password

  sku_name   = var.sku_name
  version    = "14"  # Updated to the latest stable PostgreSQL version
  storage_mb = var.storage_mb

  backup_retention_days        = var.backup_retention_days
  geo_redundant_backup_enabled = var.geo_redundant_backup_enabled
  auto_grow_enabled            = var.auto_grow_enabled

  public_network_access_enabled    = var.public_network_access_enabled
  ssl_enforcement_enabled          = true  # Always enforce SSL
  ssl_minimal_tls_version_enforced = "TLS1_2"

  threat_detection_policy {
    enabled              = true
    disabled_alerts      = []
    email_account_admins = true
    email_addresses      = var.alert_email_addresses
    retention_days       = 30
  }

  tags = merge(var.default_tags, {
    environment = var.environment
    project     = "vc-metrics-platform"
  })
}

resource "azurerm_postgresql_database" "main" {
  name                = var.database_name
  resource_group_name = var.resource_group_name
  server_name         = azurerm_postgresql_server.main.name
  charset             = "UTF8"
  collation           = "English_United States.1252"
}

resource "azurerm_private_endpoint" "main" {
  name                = "${var.server_name}-endpoint"
  location            = var.location
  resource_group_name = var.resource_group_name
  subnet_id           = var.subnet_id

  private_service_connection {
    name                           = "${var.server_name}-privateserviceconnection"
    private_connection_resource_id = azurerm_postgresql_server.main.id
    subresource_names              = ["postgresqlServer"]
    is_manual_connection           = false
  }

  private_dns_zone_group {
    name                 = "default"
    private_dns_zone_ids = [var.private_dns_zone_id]
  }
}

resource "azurerm_postgresql_firewall_rule" "azure_services" {
  name                = "allow_azure_services"
  resource_group_name = var.resource_group_name
  server_name         = azurerm_postgresql_server.main.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "0.0.0.0"
}

resource "azurerm_postgresql_firewall_rule" "allowed_ips" {
  count               = length(var.allowed_ip_ranges)
  name                = "allowed_ip_${count.index}"
  resource_group_name = var.resource_group_name
  server_name         = azurerm_postgresql_server.main.name
  start_ip_address    = var.allowed_ip_ranges[count.index].start_ip
  end_ip_address      = var.allowed_ip_ranges[count.index].end_ip
}

resource "azurerm_monitor_diagnostic_setting" "postgresql" {
  name                       = "${var.server_name}-diagnostics"
  target_resource_id         = azurerm_postgresql_server.main.id
  log_analytics_workspace_id = var.log_analytics_workspace_id

  log {
    category = "PostgreSQLLogs"
    enabled  = true

    retention_policy {
      enabled = true
      days    = 30
    }
  }

  metric {
    category = "AllMetrics"
    enabled  = true

    retention_policy {
      enabled = true
      days    = 30
    }
  }
}