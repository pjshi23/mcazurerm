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
resource_group = configData['resourceGroup']
vmssname = configData['vmssName']

access_token = mcazurerm.get_access_token(tenant_id, app_id, app_secret)

# delete vmss vm id #1
# vm_ids = '["1"]'
# result = mcazurerm.delete_vmss_vms(access_token, subscription_id, resource_group, vmssname, vm_ids)
# print(result)

# restart vmss vm id's #2, #3
# vm_ids = '["2", "3"]'
# result = mcazurerm.restart_vmss_vms(access_token, subscription_id, resource_group, vmssname, vm_ids)
# print(result)

# poweroff some vmss vm's
vm_ids = '["7", "9"]'
result = mcazurerm.poweroff_vmss_vms(access_token, subscription_id, resource_group, vmssname, vm_ids)
print(result)

# start vmss vm id's #2, #3
# vm_ids = '["2", "3"]'
# result = mcazurerm.start_vmss_vms(access_token, subscription_id, resource_group, vmssname, vm_ids)
# print(result)
