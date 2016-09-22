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

access_token = mcmcazurerm.get_access_token(
    tenant_id,
    app_id,
    app_secret
)

# list subscriptions
subscriptions = mcmcazurerm.list_subscriptions(access_token)
for sub in subscriptions["value"]:
    print(sub["displayName"] + ': ' + sub["subscriptionId"])

# print(type(subscriptions))             # dict
# print(type(subscriptions["value"]))    # list
# print(type(subscriptions["value"][0])) # dict

# use the first subscription
subscription_id = subscriptions["value"][0]["subscriptionId"]

# create a resource group
print('Enter Resource group name to create.')
rgname = input()
location = 'southeastasia'
rgreturn = mcmcazurerm.create_resource_group(access_token, subscription_id, rgname, location)
print(rgreturn)

# list resource groups
# resource_groups = mcmcazurerm.list_resource_groups(access_token, subscription_id)
# for rg in resource_groups["value"]:
#    print(rg["name"] + ', ' + rg["location"] + ', ' + rg["properties"]["provisioningState"])

# delete a resource groups

# location = 'southeastasia'
# rgreturn = mcmcazurerm.delete_resource_group(access_token, subscription_id, rgname)
# print(rgreturn)

# list resource groups
resource_groups = mcmcazurerm.list_resource_groups(access_token, subscription_id)
for rg in resource_groups["value"]:
    print(rg["name"] + ', ' + rg["location"] + ', ' + rg["properties"]["provisioningState"])

# scale_sets = mcmcazurerm.list_vm_scale_sets(access_token, subscription_id, 'auto116')
# print(scale_sets)
