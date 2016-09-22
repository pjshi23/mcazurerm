"""
Copyright (c) 2016, Marcelo Leal
Description: Simple Azure Resource Manager Python library
License: MIT (see LICENSE.txt file for details)
"""
import json
import mcmcazurerm

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

access_token = mcmcazurerm.get_access_token(
	tenant_id,
	app_id,
	app_secret
)

# list subscriptions
subscriptions = mcmcazurerm.list_subscriptions(access_token)
for sub in subscriptions["value"]:
	print("SUBSCRIPTION: " + sub["displayName"] + ': ' + sub["subscriptionId"])

# use the first subscription
subscription_id = subscriptions["value"][0]["subscriptionId"]

# list media services
media_services = mcmcazurerm.list_media_services(access_token, subscription_id)
for ms in media_services["value"]:
	print("MEDIA SERVICES: " + ms["name"] + ', REGION: ' + ms["location"])

