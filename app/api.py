# APIs SCRIPT
# this script acts as the controller

from app.utils.log import Log
from app.utils.publisher import Publisher
from database.database import Database
import json
from os.path import abspath, isfile
from time import gmtime, strftime

class Api():
	def __init__(self,name,version,host,port,username,password):
		self._name=name
		self._version=version
		self.publish=Publisher(name,version,host,port,username,password)
		self.log=Log()
		self.db=Database()

	def track(self,topic,payload):
		dat={}
		dat1={}
		topic1=''
		try:
			temp=json.loads(payload)
			if(temp['key']=="" or temp['data']['lat']=="" or temp['data']['lng']==""):
				self.log.print("Bad request...","OK")
				dat['status']='error'
				dat['status_code']=400
				dat['message']='Required Parameters empty'
				dat['data']={}
				dat['key']='NULL'
			else:
				result = self.db.get_user(temp['key'])
				if not result:
					self.log.print("Unauthorized request...","OK")
					dat['status']='error'
					dat['status_code']=401
					dat['message']='Unauthorized: invalid key given'
					dat['data']={}
					dat['key']='NULL'
				else:
					phone = result[1]
					self.db.post_track(result[0],temp['data']['lat'],temp['data']['lng'])
					dat1['data']={'lat':temp['data']['lat'],'lng':temp['data']['lng']}
					topic1 = phone
					dat['status']='success'
					dat['status_code']=200
					dat['message']='Co-ordinates successfully recorded'
					dat['data']={}
		except Exception as e:
			self.log.print("Error parsing request json",format(e))
			dat['status']='error'
			dat['status_code']=400
			dat['message']='Bad Request: error parsing json'
			dat['data']={}
			dat['key']='NULL'
		self.publish.publish(topic1,dat1,0,True,False)
		self.publish.publish(topic,dat,0,False,False)
		return 0

	def qos(self):
		return 1