import pymysql
from app.utils.log import Log
from config.config import CONFIG
from time import localtime, strftime

class Database():
	def __init__(self):
		self.log=Log()

	def test(self):
		db = pymysql.connect(CONFIG['mysql_host'],CONFIG['mysql_username'],CONFIG['mysql_password'],CONFIG['mysql_db'])
		cursor = db.cursor()
		cursor.execute("SELECT VERSION()")
		# Fetch a single row using fetchone() method.
		data = cursor.fetchone()
		print ("Database version : %s " % data)
		# disconnect from server
		db.close()

	def get_user(self,token):
		db = pymysql.connect(CONFIG['mysql_host'],CONFIG['mysql_username'],CONFIG['mysql_password'],CONFIG['mysql_db'])
		cursor = db.cursor()
		cursor.execute("SELECT users.id,users.phone FROM users LEFT JOIN tracker_tokens on tracker_tokens.user_id = users.id where tracker_tokens.token = '%s'" % token)
		data = cursor.fetchone()
		db.close()
		return data

	def post_track(self,id,lat,lng):
		try:
			db = pymysql.connect(CONFIG['mysql_host'],CONFIG['mysql_username'],CONFIG['mysql_password'],CONFIG['mysql_db'])
			cursor = db.cursor()
			datetime = strftime("%Y-%m-%d %H:%M:%S", localtime())
			cursor.execute("INSERT INTO `location_histories` (`id`,`user_id`,`lat`,`lng`,`timestamp`,`created_at`, `updated_at`) VALUES (NULL, %s, %s, %s, current_timestamp(),NULL,NULL);",(str(id),lat,lng))
			db.commit()
		except Exception as e:
			self.log.print("Error occured in insert: ",format(e))
		return 0