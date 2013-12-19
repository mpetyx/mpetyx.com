
#import httplib
#import server
#import users, etc.??
import users, objects, collections
routes = {'users' : users.py,
		'objects' : objects.py,
		'collections' : collections.py
		} #add more here

class mapper:
	def  _init__(self):
		url = 404

	def get(self, url):
		com = url.find('.com')
		print 'url -' + url
		if com > 0:
			cookie = '' #fix this
			url = url[url.find('.com') + 5:].split("/")
			print url

			try:
				#if its just say /login with no follow up run something different?
				print routes[url[0]]
				print url[1]
				routes[url[0]].run(cookie, url[1])
					
			except IndexError:
				server.senderror(404)
			except KeyError:
				server.senderror(404)
		
		else:
			server.senderror(404)
class users: #temporary to test
	def run(self, cookie, obj) :
		server.send('whatever')
#	def seturl(self, url):
#		self.url = url

#	def geturl(self):
#		return self.url
#	def set/get cookies:??

#if __name__ == "__main__":
#	conn = httplib.HTTPConnection()
#	conn.connect('site')
#	conn.request("GET", "/url")
#	conn.close()

