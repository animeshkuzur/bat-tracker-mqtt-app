# LOG MODULE
# utility script containing all the log and debug related functions

from time import localtime, strftime
from config.config import APP_DEBUG, APP_NAME
from os.path import abspath, isfile
import sys

class Log():
	def __init__(self):
		self._log_file="./logs/"+APP_NAME+".log"

	def print(self,data,e):
		try:
			f=open(self._log_file,"a")
			f.write("["+strftime("%Y-%m-%d %H:%M:%S", localtime())+"] "+data+" - "+e+"\n")
			f.close()
			if(APP_DEBUG=='TRUE'):
				print(strftime("[%Y-%m-%d %H:%M:%S]", localtime()),data,e)
		except Exception as e:
			print("Unable to write file")
			print(format(e))
			sys.exit()

	def create_log(self):
		try:
			if(isfile(self._log_file)!=True):
				f=open(self._log_file,"w")
				f.close()
		except Exception as e:
			print("Unable to write file")
			print(format(e))
			sys.exit()