import json
import sys

import mcmcazurerm


def usage():
    sys.exit('Usage: python ' + sys.argv[0] + ' rg_name')


# check for single command argument
if len(sys.argv) != 2:
    usage()

rgname = sys.argv[1]

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

access_token = mcmcazurerm.get_access_token(
    tenant_id,
    app_id,
    app_secret
)

# delete a resource groups
rgreturn = mcmcazurerm.delete_resource_group(access_token, subscription_id, rgname)
print(rgreturn)
