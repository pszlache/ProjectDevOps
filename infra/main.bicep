@description('Location for all resuorces')
param location string = resourceGroup().location

@description('Azure Container Registry name')
param arcName string

@description('ACR SKU')
param acrSku string = 'Basic'

resource acr 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' = {
  name: arcName
  location: location
  sku: {
    name: acrSku
  }
  properties: {
    adminUserEnabled: true
  }
}

output arcLoginServer string = acr.properties.loginServer
