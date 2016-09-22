# MCAzureRM is modified and based on https://github.com/gbowerman/azurerm #

i created this repro to leverage AzureRM on Mooncake.

all endpoint of AzureRM repro has been fixed with Mooncake endpoint.

China Developer can leverage this to create/update/delete resource simply.

I'm considering make it available on PIP so that you can pip install mcazurerm later.

feel free to let me know if you have any question -> raise issues 



# azurerm
Easy to use Python library for Azure Resource Manager.

The azurerm philosophy is ease of use over completeness of API. Rather than support every possible attribute the goal is to provide a set of simple functions for the most common tasks that anyone can extend. 

Note: This is not an official Microsoft library, just some REST wrappers to make it easier to call the Azure REST API. For the official Microsoft Azure library for Python please go here: <a href="https://github.com/Azure/azure-sdk-for-python">https://github.com/Azure/azure-sdk-for-python</a>.


#### Example to list Azure subscriptions, create a Resource Group, list Resource Groups
```
import azurerm

tenant_id = 'your-tenant-id'
application_id = 'your-application-id'
application_secret = 'your-application-secret'

# create an authentication token
access_token = azurerm.get_access_token(
    tenant_id,
    application_id,
    application_secret
)

# list subscriptions
subscriptions = azurerm.list_subscriptions(access_token)
for sub in subscriptions["value"]:
    print(sub["displayName"] + ': ' + sub["subscriptionId"])

# select the first subscription
subscription_id = subscriptions["value"][0]["subscriptionId"]

# create a resource group
print('Enter Resource group name to create.')
rgname = input()
location = 'southeastasia'
rgreturn = azurerm.create_resource_group(access_token, subscription_id, rgname, location)
print(rgreturn)
print(json.dumps(rgreturn.json(), sort_keys=False, indent=2, separators=(',', ': ')))

# list resource groups
resource_groups = azurerm.list_resource_groups(access_token, subscription_id)
for rg in resource_groups["value"]:
    print(rg["name"] + ', ' + rg["location"] + ', ' + rg["properties"]["provisioningState"])
``` 

#### Example to create a virtual machine
```
import azurerm
impor json

tenant_id = 'your-tenant-id'
application_id = 'your-application-id'
application_secret = 'your-application-secret'

# authenticate
access_token = azurerm.get_access_token(tenant_id, app_id, app_secret)

# create resource group
print('Creating resource group: ' + name)
rmreturn = azurerm.create_resource_group(access_token, subscription_id, name, location)
print(rmreturn)

# create NSG
nsg_name = name + 'nsg'
print('Creating NSG: ' + nsg_name)
rmreturn = azurerm.create_nsg(access_token, subscription_id, name, nsg_name, location)
nsg_id = rmreturn.json()['id']
print('nsg_id = ' + nsg_id)

# create NSG rule
nsg_rule = 'ssh'
print('Creating NSG rule: ' + nsg_rule)
rmreturn = azurerm.create_nsg_rule(access_token, subscription_id, name, nsg_name, nsg_rule, description='ssh rule',
                                  destination_range='22')
print(rmreturn)
print(json.dumps(rmreturn.json(), sort_keys=False, indent=2, separators=(',', ': ')))

# create storage account
print('Creating storage account: ' + name)
rmreturn = azurerm.create_storage_account(access_token, subscription_id, name, name, location, storage_type='Premium_LRS')
print(rmreturn)

# create VNET
vnetname = name + 'vnet'
print('Creating VNet: ' + vnetname)
rmreturn = azurerm.create_vnet(access_token, subscription_id, name, vnetname, location, nsg_id=nsg_id)
print(rmreturn)
# print(json.dumps(rmreturn.json(), sort_keys=False, indent=2, separators=(',', ': ')))
subnet_id = rmreturn.json()['properties']['subnets'][0]['id']
print('subnet_id = ' + subnet_id)

# create public IP address
public_ip_name = name + 'ip'
dns_label = name + 'ip'
print('Creating public IP address: ' + public_ip_name)
rmreturn = azurerm.create_public_ip(access_token, subscription_id, name, public_ip_name, dns_label, location)
print(rmreturn)
ip_id = rmreturn.json()['id']
print('ip_id = ' + ip_id)

# create NIC
nic_name = name + 'nic'
print('Creating NIC: ' + nic_name)
rmreturn = azurerm.create_nic(access_token, subscription_id, name, nic_name, ip_id, subnet_id, location)
print(rmreturn)
nic_id = rmreturn.json()['id']

# create VM
vm_name = name
vm_size = 'Standard_DS1'
publisher = 'Canonical'
offer = 'UbuntuServer'
sku = '16.04.0-LTS'
version = 'latest'
os_uri = 'http://' + name + '.blob.core.chinacloudapi.cn/vhds/osdisk.vhd'
username = 'rootuser'
password = 'myPassw0rd'

print('Creating VM: ' + vm_name)
rmreturn = azurerm.create_vm(access_token, subscription_id, name, vm_name, vm_size, publisher, offer, sku,
                             version, name, os_uri, username, password, nic_id, location)
print(rmreturn)
print(json.dumps(rmreturn.json(), sort_keys=False, indent=2, separators=(',', ': ')))
```   

#### Example to create a Media Services Account
```
import json
import azurerm

# Load Azure app defaults
try:
        with open('config.json') as configFile:
                configData = json.load(configFile)
except FileNotFoundError:
        print("ERROR: Expecting config.json in current folder")
        sys.exit()

tenant_id = configData['tenantId']
app_id = configData['appId']
app_secret = configData['appSecret']
subscription_id = configData['subscriptionId']
resourceGroup = configData['resourceGroup']
stoaccountName = configData['stoaccountName']
region = configData['region']

access_token = azurerm.get_access_token(
        tenant_id,
        app_id,
        app_secret
)

# list subscriptions
subscriptions = azurerm.list_subscriptions(access_token)
for sub in subscriptions["value"]:
        print("SUBSCRIPTION: " + sub["displayName"] + ': ' + sub["subscriptionId"])

# use the first subscription
subscription_id = subscriptions["value"][0]["subscriptionId"]

# create a media service account in a resource group
name = "itisjustasimpletest"
response = azurerm.create_media_service_rg(access_token, subscription_id, resourceGroup, region, stoaccountName, name)
if (response.status_code == 201):
        print("MEDIA SERVICE ACCOUNT: '" + name.upper() + "' CREATED OK.")
else:
        print("ERROR: Creating New MEDIA SERVICE ACCOUNT: " + name.upper())
```   

## Functions currently supported
A basic set of infrastructure create, list, query functions are implemented. If you want to add something please send me a PR (don't forget to update this readme too).

### Deployments
```
show_deployment(access_token, subscription_id, resource_group, deployment_name) # show deployment status/details
list_deployment_operations(access_token, subscription_id, resource_group, deployment_name) # list operations involved in a given deployment
```

### Image/Publisher catalog
```
list_offers(access_token, subscription_id, location, publisher) # list available VM image offers from a publisher
list_publishers(access_token, subscription_id, location) # list available image publishers for a location
list_sku_versions(access_token, subscription_id, location, publisher, offer, sku) # list available versions for a given publisher's sku
list_skus(access_token, subscription_id, location, publisher, offer) # list available VM image skus for a publisher offer
```

### Network
```
create_nsg(access_token, subscription_id, resource_group, nsg_name, location) # create network security group (use create_nsg_rule() to add rules to it)
create_nsg_rule(access_token, subscription_id, resource_group, nsg_name, nsg_rule_name, description, protocol='Tcp', source_range='*', destination_range='*', source_prefix='Internet', destination_prefix='*', access = 'Allow', priority=100, direction='Inbound') # create network security group rule to apply to a named NSG
create_public_ip(access_token, subscription_id, resource_group) # list the public ip addresses in a resource group
create_vnet(access_token, subscription_id, resource_group, name, location, address_prefix='10.0.0.0/16', nsg_id=None)) # create a VNet with specified name and location, optional address prefix and NSG id
delete_nic(access_token, subscription_id, resource_group, nic_name) # delete a network interface
delete_nsg(access_token, subscription_id, resource_group, nsg_name) # delete network security group
delete_nsg_rule(access_token, subscription_id, resource_group, nsg_name, nsg_rule_name) # delete network security group rule
delete_public_ip(access_token, subscription_id, resource_group, public_ip_name) # delete a public ip addresses associated with a resource group
get_lb_nat_rule(access_token, subscription_id, resource_group, lb_name, rule_name) # get details about a load balancer inbound NAT rule
get_load_balancer(access_token, subscription_id, resource_group, lb_name) # get details about a load balancer
get_network_usage(access_token, subscription_id, location) # list network usage and limits for a location
get_public_ip(access_token, subscription_id, resource_group) # get details about the named public ip address
get_vnet(access_token, subscription_id, resource_group, vnet_name) # get details about the named virtual network
list_lb_nat_rules(access_token, subscription_id, resource_group, lb_name) # list the inbound NAT rules for a load balancer
list_load_balancers(access_token, subscription_id) # list the load balancers in a subscription
list_load_balancers_rg(access_token, subscription_id, resource_group) # list the load balancers in a resource group
create_nic(access_token, subscription_id, resource_group, nic_name, public_ip_id, subnet_id, location) # create a network interface
list_nics(access_token, subscription_id) # list the network interfaces in a subscription
list_nics_rg(access_token, subscription_id, resource_group) # list the network interfaces in a resource group
list_public_ips(access_token, subscription_id, resource_group) # list the public ip addresses in a resource group
list_vnets(access_token, subscription_id) # list the VNETs in a subscription
```

### Insights
```
list_autoscale_settings(access_token, subscription_id) # list the autoscale settings in a subscription_id
list_insights_components(access_token, subscription_id, resource_group) # list the Microsoft Insights components in a resource group
list_metric_definitions_for_resource(access_token, subscription_id, resource_group, resource_provider, resource_type, resource_name) # list the monitoring metric definitions for a resource
get_metrics_for_resource(access_token, subscription_id, resource_group, resource_provider, resource_type, resource_name) # get the monitoring metrics for a resource
```

#### Media Services (Media Resource provider)
```
create_media_service_rg(access_token, subscription_id, rgname) # create a media services account in a resource group
check_name_availability(access_token, subscription_id, rgname) # verify the availability of an media services account name
delete_media_service_rg(access_token, subscription_id, rgname) # delete a media services account in a resource group
list_media_endpoint_keys(access_token, subscription_id, rgname, msname) # list media services endpoint keys in a resource group and specifig media services account
list_media_services(access_token, subscription_id) # list media services in a subscription
list_media_services_rg(access_token, subscription_id, rgname) # list media services in a specific resource group
```

#### Resource groups
```
create_resource_group(access_token, subscription_id, rgname, location) # create a resource group in the specified location  
delete_resource_group(access_token, subscription_id, rgname) # delete the named resource group
get_resource_group(access_token, subscription_id, rgname) # get details about the named resource group
list_resource_groups(access_token, subscription_id) # list the resource groups in your subscription  
```

#### Storage
```
create_storage_account(access_token, subscription_id, rgname, location, storage_type='Standard_LRS') # create a new storage account
delete_storage_account(access_token, subscription_id, rgname) # delete a storage account in the specified resource group
get_storage_account(access_token, subscription_id, rgname) # get details for the specified storage account
get_storage_account_keys(access_token, subscription_id, rgname, account_name) # get the access keys for the specified storage account
get_storage_usage(access_token, subscription_id) # returns storage usage and quota information for the specified subscription
list_storage_accounts_rg(access_token, subscription_id, rgname) # list the storage accounts in the specified resource group
list_storage_accounts_sub(access_token, subscription_id) # list the storage accounts in the specified subscription
```

#### Subscription, location, and access token
```
get_access_token(tenant_id, application_id, application_secret) # get an Azure access token for your application
    # Note get_access_token has optional endpoint parameters which allow you to join national clouds
    # - authentication_endpoint='https://login.microsoftonline.com/', resource='https://management.core.windows.net/
list_locations(access_token, subscription_id) # list available locations for a subscription
list_subscriptions(access_token) # list the available Azure subscriptions for this application  
```

### Template functions
```
deploy_template(access_token, subscription_id, resource_group, deployment_name, template, parameters) # deploy a template referenced by a JSON string, with parameters as a JSON string
deploy_template_uri(access_token, subscription_id, resource_group, deployment_name, template_uri, parameters) # deploy a template referenced by a URI, with parameters as a JSON string
deploy_template_uri_param_uri(access_token, subscription_id, resource_group, deployment_name, template_uri, parameters_uri) # deploy a template with both template and parameters referenced by URIs
```

#### Virtual machines and VM Scale Sets (Compute Resource provider)
```
create_vm(access_token, subscription_id, resource_group, vm_name, vm_size, publisher, offer, sku, version,
              storage_account, os_uri, username, password, nic_id, location) # simple vm create function
deallocate_vm(access_token, subscription_id, resource_group, vm_name) # stop#deallocate a virtual machine
delete_vm(access_token, subscription_id, resource_group, vm_name) # delete a virtual machine
delete_vmss(access_token, subscription_id, resource_group, vmss_name) # delete a virtual machine scale set
delete_vmss_vms(access_token, subscription_id, resource_group, vm_ids) # delete a VM in a VM Scale Set
get_compute_usage(access_token, subscription_id, location) # list compute usage and limits for a location
get_vm(access_token, subscription_id, resource_group, vm_name) # get virtual machine details
get_vm_extension(access_token, subscription_id, resource_group, vm_name, extension_name) # get details about a VM extension
get_vmss(access_token, subscription_id, resource_group, vmss_name) # get virtual machine scale set details
get_vmss_instance_view(access_token, subscription_id, resource_group, vmss_name) # get virtual machine scale set instance view
get_vmss_nics(access_token, subscription_id, resource_group, vmss_name) # get NIC details for a VM Scale Set
get_vmss_vm(access_token, subscription_id, resource_group, vmss_name, instance_id) # get individual VMSS VM details
get_vmss_vm_instance_view(access_token, subscription_id, resource_group, vmss_name, instance_id) # get individual VMSS VM instance view
get_vmss_vm_nics(access_token, subscription_id, resource_group, vmss_name, instance_id) # get NIC details for a VMSS VM
list_as(access_token, subscription_id, resource_group) # list availability sets in a resource_group
list_as_sub(access_token, subscription_id) # list availability sets in a subscription
list_vm_images_sub(access_token, subscription_id) # list VM images in a subscription
list_vms(access_token, subscription_id, resource_group) # list VMs in a resource group
list_vms_sub(access_token, subscription_id) # list the VMs in a subscription
list_vmss(access_token, subscription_id, resource_group) # list the VM Scale Sets in a resource group
list_vmss_sub(access_token, subscription_id) # list the VM Scale Sets in a subscription
list_vmss_vm_instance_view(access_token, subscription_id, resource_group, vmss_name) # list the VMSS VM instance views in a scale set
list_vmss_vms(access_token, subscription_id, resource_group, vmss_name) # list the VMs in a VM Scale Set
restart_vm(access_token, subscription_id, resource_group, vm_name) # restart a virtual machine
restart_vmss(access_token, subscription_id, resource_group, vmss_name) # restart all the VMs in a virtual machine scale set
restart_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_id) # restart VMs in a virtual machine scale set
scale_vmss(access_token, subscription_id, resource_group, vmss_name, size, tier, capacity) # change the instance count of an existing VM Scale Set
start_vm(access_token, subscription_id, resource_group, vm_name) # start a virtual machine
start_vmss(access_token, subscription_id, resource_group, vmss_name) # start all the VMs in a virtual machine scale set
start_vmss_vms(access_token, subscription_id, resource_group, vmss_name, vm_ids) # start VMs in a virtual machine scale set
stop_vm(access_token, subscription_id, resource_group, vm_name) # stop a VM, don't deallocate resources
stopdealloc_vmss(access_token, subscription_id, resource_group, vmss_name) # stop all the VMs in a virtual machine scale set
stopdealloc_vmss_vms(access_token, subscription_id, resource_group, vm_ids) # stop VMs in a virtual machine scale set
poweroff_vmss(access_token, subscription_id, resource_group, vmss_name) # poweroff all the VMs in a virtual machine scale set
poweroff_vmss_vms(access_token, subscription_id, resource_group, vmss_name, vm_ids) # poweroff VMs in a virtual machine scale set
update_vm(access_token, subscription_id, resource_group, vm_name, body) # updates a VM model, that is put an updated virtual machine scale set body
update_vmss(access_token, subscription_id, resource_group, vmss_name, body) # updates a VMSS model, that is put an updated virtual machine scale set body
upgrade_vmss_vms(access_token, subscription_id, resource_group, vmss_name, instance_ids) # upgrade a specific VMs a virtual machine scale set
```
