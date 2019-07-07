# CONFIGURATION MODULE
# reads the config.json file and initializes the global variables

import json
from os.path import abspath, isfile
import sys

json_path = abspath("./config.json")

try:
	if(isfile(json_path)!=True):
		print('File not found: config.json')
		sys.exit()
	with open(json_path) as json_data:
		data = json.load(json_data)
except Exception as e:
	print('Failed to read file: config.json')
	print('Invalid json')
	print(e)
	sys.exit()

try:
	APP_NAME = data['app']['name']
	APP_DEBUG = data['app']['debug'].upper()
	APP_VERSION = data['app']['version']

	MYSQL_HOST = data['mysql']['host']
	MYSQL_PORT = data['mysql']['port']
	MYSQL_DB = data['mysql']['database']
	MYSQL_USERNAME = data['mysql']['username']
	MYSQL_PASSWORD = data['mysql']['password']

	REDIS_HOST = data['redis']['host']
	REDIS_PORT = data['redis']['port']

	BROKER_HOST = data['mqtt_broker']['host']
	BROKER_PORT = int(data['mqtt_broker']['port'])
	BROKER_KEY_MGMT = data['mqtt_broker']['key_mgmt'].upper()
	BROKER_USERNAME = None
	BROKER_PASSWORD = None
	if(BROKER_KEY_MGMT=='TRUE'):
		BROKER_USERNAME = data['mqtt_broker']['username']
		BROKER_PASSWORD = data['mqtt_broker']['password']

	CONFIG={
		'app_name':APP_NAME,
		'app_debug':APP_DEBUG,
		'app_version':APP_VERSION,

		'mysql_host':MYSQL_HOST,
		'mysql_port':MYSQL_PORT,
		'mysql_db':MYSQL_DB,
		'mysql_username':MYSQL_USERNAME,
		'mysql_password':MYSQL_PASSWORD,

		'broker_host':BROKER_HOST,
		'broker_port':BROKER_PORT,
		'broker_key_mgmt':BROKER_KEY_MGMT,
		'broker_username':BROKER_USERNAME,
		'broker_password':BROKER_PASSWORD
	}
except Exception as e:
	print('Failed to read file: config.json')
	print('Invalid config')
	print(format(e))
	sys.exit()