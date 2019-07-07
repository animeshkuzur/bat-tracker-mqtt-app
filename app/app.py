# APP SCRIPT
# all core logic goes here. Starts after configuration is complete or to re-configure the app

from app.utils.log import Log
from config.config import CONFIG
from database.database import Database
from app.api import Api
from app.utils.subscriber import Subscriber
from app.utils.threads import Threads
import threading

class App():
	def __init__(self):
		self.database = Database()
		self._name=CONFIG['app_name']
		self._version=CONFIG['app_version']
		self._broker_host=CONFIG['broker_host']
		self._broker_port=CONFIG['broker_port']
		self._broker_username=CONFIG['broker_username']
		self._broker_password=CONFIG['broker_password']
		self._lock=threading.Lock()
		self.log=Log()

	def start(self):
		try:
			api=Api(self._name,self._version,self._broker_host,self._broker_port,self._broker_username,self._broker_password)
			self.log.print("Listening to all APIs","OK")
			sub=Subscriber(api,self._name,self._version,self._broker_host,self._broker_port,self._broker_username,self._broker_password,self._lock)
			sub_thread = Threads(1, "Subscriber Thread",self._lock,sub)
			sub_thread.start()
			sub_thread.join()
		except Exception as e:
			self.log.print("Exception in the main thread: ",format(e))
		# self.database.get_user('71f7bb0c6db392201e3c')