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

# list autoscale settings
auto_settings = mcazurerm.list_autoscale_settings(access_token, subscription_id)
# print(auto_settings)
for auto_setting in auto_settings['value']:
    print(auto_setting['name'] + ', ' + auto_setting['location'])
    print(auto_setting['properties']['profiles'])

# loop through resource groups
resource_groups = mcazurerm.list_resource_groups(access_token, subscription_id)
for rg in resource_groups["value"]:
    rgname = rg["name"]
    insights_comp = mcazurerm.list_insights_components(access_token, subscription_id, rgname)
    if len(insights_comp) > 0:
        print(insights_comp)
