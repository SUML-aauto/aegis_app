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
        application_stack {
          docker_registry_url = "https://ghcr.io"
          docker_registry_username = var.ghcr_username
          docker_registry_password = var.ghcr_access_token
          docker_image_name = "suml-aauto/aegis_app:master"
        }
    }
    app_settings = {
        WEBSITES_PORT = "8080"
        WEBSITES_ENABLE_APP_SERVICE_STORAGE = "false"
    }
}

/*
resource "azurerm_storage_account" "aegisauto_storage" {
    name                     = "aegisautostorage"
    resource_group_name      = azurerm_resource_group.main_resource_group.name
    location                 = azurerm_resource_group.main_resource_group.location
    account_tier             = "Standard"
    account_replication_type = "LRS"
}

resource "azurerm_storage_container" "aegisauto_mlflow_storage" {
    name                  = "aegisautomlflowstorage"
    storage_account_name  = azurerm_storage_account.aegisauto_storage.name
    container_access_type = "private"
}
*/
