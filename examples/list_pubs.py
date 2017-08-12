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

access_token = mcazurerm.get_access_token(tenant_id, app_id, app_secret)

pubs = mcazurerm.list_publishers(access_token, subscription_id, 'southeastasia')

# skus = mcazurerm.list_skus(access_token, subscription_id, 'southeastasia', 'MicrosoftWindowsServer', 'WindowsServer')
skus = mcazurerm.list_skus(access_token, subscription_id, 'southeastasia', 'Canonical', 'UbuntuServer')
for sku in skus:
    print(sku['name'])

print('Versions for sku 14.04.2-LTS:')
versions = mcazurerm.list_sku_versions(access_token, subscription_id, 'southeastasia', 'Canonical', 'UbuntuServer',
                                     '14.04.2-LTS')
for version in versions:
    print(version['name'])
