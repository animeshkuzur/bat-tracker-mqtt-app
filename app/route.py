# ROUTES SCRIPT
# consists of all mqtt topics
# ROUTES variable is a global dictionary with topics as key and function names as values eg. <topic>:<function@filename>
# prefix '<version_number>/<app_name>/'
# postfix '/request'

ROUTES = {
	'track':'track@api'
}