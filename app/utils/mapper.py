# MAPPER SCRIPT
# maps the routes to their respective functions and passes along the data

from app.route import ROUTES
from app.utils.log import Log

class Mapper():
	def __init__(self,name,version,api):
		self._api=api
		self._name=name
		self._version=version
		self.log=Log()

	def map(self,topic,payload):
		try:
			_a=self.topic_parser(topic)
			_f=self.route_parser(ROUTES[_a])
			return getattr(self._api,_f)(_a,payload)
		except Exception as e:
			self.log.print("Mapper:Unauthorised function call",format(e))
			return 0

	def topic_parser(self,topic):
		try:
			c=0
			top=topic.split('/')
			subtopic=''
			for t in top:
				if(t==self._version or t==self._name or t=='request'):
					c=c+1
				else:
					subtopic=subtopic+'/'+t
			if(c==3):
				return subtopic[1:]
			return None
		except Exception as e:
			self.log.print("Mapper.topic_parser() error occured: ",format(e))
			return None

	def route_parser(self,route):
		try:
			subroute=route.split('@')
			return subroute[0]
		except Exception as e:
			self.log.print("Mapper.route_parser() error occured: ",format(e))
			return None