# SUBSCRIBE MODULE
# subscribes to a particular topic and fetches data

import paho.mqtt.client as mqtt
from app.utils.mapper import Mapper
from app.utils.log import Log
import time

class Subscriber():

	def __init__(self,api,name,version,host,port,username,password,lock):
		self._api=api
		self._name=name
		self._version=version
		self._host=host
		self._port=port
		self._username=username
		self._password=password
		self._CLEAN_SESSION=True
		self._loop_flag=0
		self._lock=lock
		self.log=Log()
		self.mapper=Mapper(name,version,api)

	def start(self):
		client=mqtt.Client("global_subscriber",clean_session=self._CLEAN_SESSION)
		client.on_connect=self.on_connect
		client.on_disconnect=self.on_disconnect
		client.on_subscribe=self.on_subscribe
		client.on_unsubscribe=self.on_unsubscribe
		client.on_message=self.on_message
		if(self._username!=None):
			client.username_pw_set(username=self._username,password=self._password)
		client.connect(self._host, port=self._port, keepalive=60, bind_address="")
		client.loop_start()
		topic=self._version+"/"+self._name+"/#"
		r=client.subscribe(topic,self._api.qos())
		if r[0]==0:
			self.log.print("Global Listener on topic: "+topic,"OK")
		else:
			self.log.print("Global Listener unable to subscribe to topic: "+topic,str(r))
		while(self._loop_flag==0):
			time.sleep(0.01)
		client.loop_stop()
		client.disconnect()
		self.log.print("Destroying Subscriber Thread","OK")

	def on_connect(self,client, userdata, flags, rc):
		self.log.print(client.name+":on_connect callback result, Flags: "+str(flags),str(rc))

	def on_disconnect(self):
		pass

	def on_subscribe(self,client, userdata, mid, granted_qos):
		self.log.print(client.name+":on_subscribe callback result, MID: "+str(mid),str(rc))

	def on_unsubscribe(self,client, userdata, mid):
		pass

	def on_message(self,client, userdata, message):
		if('response' in str(message.topic)):
			return 0
		self.log.print("on_message callback, acquiring lock","OK")
		self._lock.acquire()
		try:
			self.log.print("incoming request on topic:"+str(message.topic)+" QoS:"+str(message.qos)+" Retain Flag:"+str(message.retain),"OK")
			self._loop_flag=self.mapper.map(str(message.topic),message.payload.decode())
		except Exception as e:
			self.log.print("on_message callback error",format(e))
			self._loop_flag=0
		self.log.print("exiting on_message callback, releasing lock","OK")
		self._lock.release()
