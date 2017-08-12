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

# loop through resource groups
resource_groups = mcazurerm.list_resource_groups(access_token, subscription_id)
for rg in resource_groups["value"]:
    rgname = rg["name"]
    vmsslist = mcazurerm.list_vm_scale_sets(access_token, subscription_id, rgname)
    for vmss in vmsslist['value']:
        name = vmss['name']
        location = vmss['location']
        capacity = vmss['sku']['capacity']
        offer = vmss['properties']['virtualMachineProfile']['storageProfile']['imageReference']['offer']
        sku = vmss['properties']['virtualMachineProfile']['storageProfile']['imageReference']['sku']
        print(''.join(['Name: ', name,
                       ', RG: ', rgname,
                       ', location: ', location,
                       ', Capacity: ', str(capacity),
                       ', OS: ', offer, ' ', sku]))
        print('VMSS NICs...')
        vmssNics = mcazurerm.get_vmss_nics(access_token, subscription_id, rgname, name)
        print(json.dumps(vmssNics, sort_keys=False, indent=2, separators=(',', ': ')))
        print('VMSS Virtual machines...')
        vms = mcazurerm.list_vmss_vms(access_token, subscription_id, rgname, name)
        # print(json.dumps(vms, sort_keys=False, indent=2, separators=(',', ': ')))
        for vm in vms['value']:
            vmId = vm['instanceId']
            print(vmId + ', ' + vm['name'] + '\n')
            print('VMSS VM NICs...')
            vmnics = mcazurerm.get_vmss_vm_nics(access_token, subscription_id, rgname, name, vmId)
            print(json.dumps(vmnics, sort_keys=False, indent=2, separators=(',', ': ')))
