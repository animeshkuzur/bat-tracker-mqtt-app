# THREADS SCRIPT
# script to manage threads

from app.utils.log import Log
import threading

class Threads(threading.Thread):
	def __init__(self,tid,name,lock,obj):
		threading.Thread.__init__(self)
		self._id=str(tid)
		self._name=name
		self._lock=lock
		self._obj=obj
		self.log=Log()
		self.log.print("Creating Thread Named: "+self._name+"; ID: "+self._id,"OK")

	def run(self):
		self._obj.start()