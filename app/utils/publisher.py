import paho.mqtt.client as mqtt
from app.utils.log import Log
import json

class Publisher():

	def __init__(self,name,version,host,port,username,password):
		self._name=name
		self._version=version
		self._host=host
		self._port=port
		self._username=username
		self._password=password
		self.log=Log()
		self._CLEAN_SESSION=True

	def publish(self,topic,data,q,r,debug=True):
		try:
			client=mqtt.Client("global_publisher",clean_session=self._CLEAN_SESSION)
			client.on_connect=self.on_connect
			client.on_disconnect=self.on_disconnect
			client.on_publish=self.on_publish
			if(self._username!=None):
				client.username_pw_set(username=self._username,password=self._password)
			client.connect(self._host, port=self._port, keepalive=60, bind_address="")
			topic=self._version+"/"+self._name+"/"+topic+"/response"
			client.loop_start()
			rc=client.publish(topic,payload=json.dumps(data),qos=q,retain=r)
			client.loop_stop()
			client.disconnect()
			if(debug):
				if rc[0]==0:
					self.log.print("Global publisher on topic: "+topic+" QoS:"+str(q)+" Retain:"+str(r)+" RC:"+str(rc),"OK")
				else:
					self.log.print("Global publish unable to publish on topic: "+topic,str(r))
		except Exception as e:
			self.log.print("Global Publisher error: ",format(e))		

	def on_connect(self,client, userdata, flags, rc):
		self.log.print(client.name+":on_connect callback result, Flags: "+str(flags),str(rc))

	def on_disconnect(self):
		pass

	def on_publish(self,client,userdata,mid):
		self.log.print("publish response, MID: "+mid+"...","OK")
