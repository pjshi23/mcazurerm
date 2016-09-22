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

# list the VMs 
vmsslist = mcmcazurerm.list_vmss_sub(access_token, subscription_id)
for vm in vmsslist['value']:
    # print(json.dumps(vm, sort_keys=False, indent=2, separators=(',', ': ')))
    print(vm['name'])
'''
# loop through resource groups
resource_groups = mcmcazurerm.list_resource_groups(access_token, subscription_id)
for rg in resource_groups["value"]:
    rgname = rg["name"] 
    vmsslist = mcmcazurerm.list_vmss(access_token, subscription_id, rgname)
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
        print('Virtual machines...')
        vms = mcmcazurerm.list_vmss_vms(access_token, subscription_id, rgname, name)
        #print(json.dumps(vms, sort_keys=False, indent=2, separators=(',', ': ')))
        for vm in vms['value']:
            vmid = vm['instanceId']
            vmnic = mcmcazurerm.get_vmss_vm_nics(access_token, subscription_id, rgname, name, vmid)
            privateIP = vmnic['value'][0]['properties']['ipConfigurations'][0]['properties']['privateIPAddress']
            #print(json.dumps(vmnic, sort_keys=False, indent=2, separators=(',', ': ')))
            print(vmid + ', ' + vm['name'] + ', private IP:' + privateIP)


#startoutput = mcmcazurerm.start_vmss(access_token, subscription_id, 'guydock3', 'guydock3')
# print(startoutput)

# scaleoutput = mcmcazurerm.scale_vmss(access_token, subscription_id, 'guydock3', 'guydock3', 'Standard_A1', 'Standard', 5)
# print(scaleoutput)
'''
