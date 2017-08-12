import json

import mcazurerm

# Load Azure app defaults
try:
    with open('mcazurermconfig.json') as configFile:
        configData = json.load(configFile)
except FileNotFoundError:
    print("Error: Expecting vmssConfig.json in current folder")
    sys.exit()

tenant_id = configData['tenantId']
app_id = configData['appId']
app_secret = configData['appSecret']
subscription_id = configData['subscriptionId']
access_token = mcazurerm.get_access_token(
    tenant_id,
    app_id,
    app_secret
)

# create a resource group
print('Enter Resource group name to create.')
rgname = input()
location = 'eastus'
rgreturn = mcazurerm.create_resource_group(access_token, subscription_id, rgname, location)
print(rgreturn)
