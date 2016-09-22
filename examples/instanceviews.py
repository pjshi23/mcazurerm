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
rg = configData['resourceGroup']
vmss = configData['vmssName']

access_token = mcmcazurerm.get_access_token(tenant_id, app_id, app_secret)

# loop through resource groups
instances = mcmcazurerm.list_vmss_vm_instance_view(access_token, subscription_id, rg, vmss)

print(json.dumps(instances, sort_keys=False, indent=2, separators=(',', ': ')))
