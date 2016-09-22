import json

import mcmcazurerm

# Load Azure app defaults
try:
    with open('mcmcazurermconfig.json') as configFile:
        configData = json.load(configFile)
except FileNotFoundError:
    print("Error: Expecting vmssConfig.json in current folder")
    sys.exit()

tenant_id = configData['tenantId']
app_id = configData['appId']
app_secret = configData['appSecret']
subscription_id = configData['subscriptionId']

access_token = mcmcazurerm.get_access_token(tenant_id, app_id, app_secret)

# list locations
locations = mcmcazurerm.list_locations(access_token, subscription_id)

for location in locations['value']:
    print(location['name']
          + ', Display Name: ' + location['displayName']
          + ', Coords: ' + location['latitude']
          + ', ' + location['longitude'])
