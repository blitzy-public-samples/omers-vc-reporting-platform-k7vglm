# Azure Monitor and Application Insights configuration for the VC firm's financial reporting metrics backend platform
# This module sets up Log Analytics workspace, Application Insights, and metric alerts

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"  # Updated to the latest major version
    }
  }
}

# Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "main" {
  name                = var.log_analytics_workspace_name
  location            = var.location
  resource_group_name = var.resource_group_name
  sku                 = "PerGB2018"
  retention_in_days   = var.retention_in_days

  tags = merge(var.common_tags, {
    component = "monitoring"
  })
}

# Application Insights
resource "azurerm_application_insights" "main" {
  name                = var.application_insights_name
  location            = var.location
  resource_group_name = var.resource_group_name
  application_type    = "web"
  workspace_id        = azurerm_log_analytics_workspace.main.id

  tags = merge(var.common_tags, {
    component = "monitoring"
  })
}

# Action Group for critical alerts
resource "azurerm_monitor_action_group" "critical" {
  name                = "${var.project_name}-critical-alerts"
  resource_group_name = var.resource_group_name
  short_name          = "critical"

  email_receiver {
    name                    = "admin"
    email_address           = var.admin_email
    use_common_alert_schema = true
  }

  sms_receiver {
    name         = "oncall"
    country_code = var.oncall_sms_country_code
    phone_number = var.oncall_sms_number
  }
}

# Metric Alert for high CPU usage
resource "azurerm_monitor_metric_alert" "high_cpu" {
  name                = "${var.project_name}-high-cpu-usage"
  resource_group_name = var.resource_group_name
  scopes              = var.app_service_ids

  criteria {
    metric_namespace = "Microsoft.Web/sites"
    metric_name      = "CpuPercentage"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = var.cpu_threshold
    time_grain       = "PT1M"
    time_window      = "PT5M"
    frequency        = "PT1M"
    time_aggregation = "Average"
  }

  action {
    action_group_id = azurerm_monitor_action_group.critical.id
  }

  tags = merge(var.common_tags, {
    alert_type = "high_cpu"
  })
}

# Metric Alert for high memory usage
resource "azurerm_monitor_metric_alert" "high_memory" {
  name                = "${var.project_name}-high-memory-usage"
  resource_group_name = var.resource_group_name
  scopes              = var.app_service_ids

  criteria {
    metric_namespace = "Microsoft.Web/sites"
    metric_name      = "MemoryPercentage"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = var.memory_threshold
    time_grain       = "PT1M"
    time_window      = "PT5M"
    frequency        = "PT1M"
    time_aggregation = "Average"
  }

  action {
    action_group_id = azurerm_monitor_action_group.critical.id
  }

  tags = merge(var.common_tags, {
    alert_type = "high_memory"
  })
}

# HTTP 5xx Error Rate Alert
resource "azurerm_monitor_metric_alert" "http_5xx_errors" {
  name                = "${var.project_name}-http-5xx-errors"
  resource_group_name = var.resource_group_name
  scopes              = var.app_service_ids

  criteria {
    metric_namespace = "Microsoft.Web/sites"
    metric_name      = "Http5xx"
    aggregation      = "Total"
    operator         = "GreaterThan"
    threshold        = var.http_5xx_threshold
    time_grain       = "PT1M"
    time_window      = "PT5M"
    frequency        = "PT1M"
    time_aggregation = "Total"
  }

  action {
    action_group_id = azurerm_monitor_action_group.critical.id
  }

  tags = merge(var.common_tags, {
    alert_type = "http_5xx_errors"
  })
}

# Application Insights Availability Test
resource "azurerm_application_insights_web_test" "availability" {
  name                    = "${var.project_name}-availability-test"
  location                = var.location
  resource_group_name     = var.resource_group_name
  application_insights_id = azurerm_application_insights.main.id
  kind                    = "ping"
  frequency               = 300
  timeout                 = 60
  enabled                 = true
  geo_locations           = var.availability_test_locations

  configuration = <<XML
<WebTest Name="AvailabilityTest" Enabled="True" CssProjectStructure="" CssIteration="" Timeout="120" WorkItemIds="" xmlns="http://microsoft.com/schemas/VisualStudio/TeamTest/2010" Description="" CredentialUserName="" CredentialPassword="" PreAuthenticate="True" Proxy="default" StopOnError="False" RecordedResultFile="" ResultsLocale="">
  <Items>
    <Request Method="GET" Version="1.1" Url="${var.app_service_url}" ThinkTime="0" Timeout="300" ParseDependentRequests="True" FollowRedirects="True" RecordResult="True" Cache="False" ResponseTimeGoal="0" Encoding="utf-8" ExpectedHttpStatusCode="200" ExpectedResponseUrl="" ReportingName="" IgnoreHttpStatusCode="False" />
  </Items>
</WebTest>
XML

  tags = merge(var.common_tags, {
    component = "availability_test"
  })
}

# Availability Alert
resource "azurerm_monitor_metric_alert" "availability" {
  name                = "${var.project_name}-availability-alert"
  resource_group_name = var.resource_group_name
  scopes              = [azurerm_application_insights.main.id]

  criteria {
    metric_namespace = "microsoft.insights/components"
    metric_name      = "availabilityResults/availabilityPercentage"
    aggregation      = "Average"
    operator         = "LessThan"
    threshold        = var.availability_threshold
    time_grain       = "PT1M"
    time_window      = "PT5M"
    frequency        = "PT1M"
    time_aggregation = "Average"
  }

  action {
    action_group_id = azurerm_monitor_action_group.critical.id
  }

  tags = merge(var.common_tags, {
    alert_type = "availability"
  })
}