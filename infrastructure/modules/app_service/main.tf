# Azure App Service Module for VC Financial Reporting Metrics Backend Platform
# This module creates and manages an Azure App Service for hosting the FastAPI application

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 2.0"
    }
  }
}

locals {
  common_tags = {
    Project     = "VC Financial Reporting"
    Environment = terraform.workspace
    ManagedBy   = "Terraform"
  }
}

resource "azurerm_app_service_plan" "main" {
  name                = var.app_service_plan_name
  location            = var.location
  resource_group_name = var.resource_group_name
  kind                = "Linux"
  reserved            = true

  sku {
    tier = var.sku_tier
    size = var.sku_size
  }

  tags = merge(local.common_tags, var.additional_tags)

  lifecycle {
    create_before_destroy = true
  }
}

resource "azurerm_app_service" "main" {
  name                = var.app_service_name
  location            = var.location
  resource_group_name = var.resource_group_name
  app_service_plan_id = azurerm_app_service_plan.main.id

  https_only = true

  site_config {
    linux_fx_version          = "DOCKER|${var.docker_image}"
    always_on                 = true
    http2_enabled             = true
    min_tls_version           = "1.2"
    ftps_state                = "Disabled"
    use_32_bit_worker_process = false

    cors {
      allowed_origins     = var.allowed_origins
      support_credentials = false
    }

    health_check_path = var.health_check_path
  }

  identity {
    type = "SystemAssigned"
  }

  app_settings = merge({
    WEBSITES_ENABLE_APP_SERVICE_STORAGE = "false"
    DOCKER_REGISTRY_SERVER_URL          = "https://mcr.microsoft.com"
    DOCKER_ENABLE_CI                    = "true"
    WEBSITES_PORT                       = var.app_port
    WEBSITE_RUN_FROM_PACKAGE            = "1"
    APPINSIGHTS_INSTRUMENTATIONKEY      = var.app_insights_instrumentation_key
  }, var.additional_app_settings)

  logs {
    http_logs {
      file_system {
        retention_in_days = 7
        retention_in_mb   = 35
      }
    }
  }

  tags = merge(local.common_tags, var.additional_tags)

  lifecycle {
    ignore_changes = [
      site_config[0].linux_fx_version, # Ignore changes to the Docker image tag
    ]
  }
}

resource "azurerm_app_service_custom_hostname_binding" "main" {
  count               = var.custom_domain != "" ? 1 : 0
  hostname            = var.custom_domain
  app_service_name    = azurerm_app_service.main.name
  resource_group_name = var.resource_group_name
}

resource "azurerm_app_service_managed_certificate" "main" {
  count                      = var.custom_domain != "" ? 1 : 0
  custom_hostname_binding_id = azurerm_app_service_custom_hostname_binding.main[0].id
}

resource "azurerm_app_service_certificate_binding" "main" {
  count               = var.custom_domain != "" ? 1 : 0
  hostname_binding_id = azurerm_app_service_custom_hostname_binding.main[0].id
  certificate_id      = azurerm_app_service_managed_certificate.main[0].id
  ssl_state           = "SniEnabled"
}

resource "azurerm_monitor_diagnostic_setting" "app_service" {
  name                       = "${var.app_service_name}-diagnostics"
  target_resource_id         = azurerm_app_service.main.id
  log_analytics_workspace_id = var.log_analytics_workspace_id

  log {
    category = "AppServiceHTTPLogs"
    enabled  = true

    retention_policy {
      enabled = true
      days    = 30
    }
  }

  log {
    category = "AppServiceConsoleLogs"
    enabled  = true

    retention_policy {
      enabled = true
      days    = 30
    }
  }

  log {
    category = "AppServiceAppLogs"
    enabled  = true

    retention_policy {
      enabled = true
      days    = 30
    }
  }

  log {
    category = "AppServiceAuditLogs"
    enabled  = true

    retention_policy {
      enabled = true
      days    = 30
    }
  }

  log {
    category = "AppServiceIPSecAuditLogs"
    enabled  = true

    retention_policy {
      enabled = true
      days    = 30
    }
  }

  log {
    category = "AppServicePlatformLogs"
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

resource "azurerm_monitor_autoscale_setting" "app_service" {
  name                = "${var.app_service_name}-autoscale"
  resource_group_name = var.resource_group_name
  location            = var.location
  target_resource_id  = azurerm_app_service_plan.main.id

  profile {
    name = "Default"

    capacity {
      default = var.default_instance_count
      minimum = var.min_instance_count
      maximum = var.max_instance_count
    }

    rule {
      metric_trigger {
        metric_name        = "CpuPercentage"
        metric_resource_id = azurerm_app_service_plan.main.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        time_aggregation   = "Average"
        operator           = "GreaterThan"
        threshold          = 75
      }

      scale_action {
        direction = "Increase"
        type      = "ChangeCount"
        value     = "1"
        cooldown  = "PT5M"
      }
    }

    rule {
      metric_trigger {
        metric_name        = "CpuPercentage"
        metric_resource_id = azurerm_app_service_plan.main.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        time_aggregation   = "Average"
        operator           = "LessThan"
        threshold          = 25
      }

      scale_action {
        direction = "Decrease"
        type      = "ChangeCount"
        value     = "1"
        cooldown  = "PT5M"
      }
    }
  }

  tags = merge(local.common_tags, var.additional_tags)
}