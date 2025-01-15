resource "azurerm_resource_group" "main_resource_group" {
    name = "aegisauto-main"
    location = "polandcentral"
}

resource "azurerm_service_plan" "main_webapp_service_plan" {
    name                = "main_webapp_service_plan"
    resource_group_name = azurerm_resource_group.main_resource_group.name
    location            = "polandcentral"
    os_type             = "Linux"
    sku_name            = "F1"
}

resource "azurerm_linux_web_app" "main_webapp" {
    name                = "aegisauto"
    resource_group_name = azurerm_resource_group.main_resource_group.name
    location            = azurerm_service_plan.main_webapp_service_plan.location
    service_plan_id     = azurerm_service_plan.main_webapp_service_plan.id

    site_config {
        always_on = false
        app_command_line = ""
    }
    app_settings = {
        WEBSITES_PORT = "8080"
        WEBSITES_ENABLE_APP_SERVICE_STORAGE = "false"
    }
}
