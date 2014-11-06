from wsgiref.simple_server import make_server

# The decorator add an attribute into the target method
def route(path):
	def decorator(func):
		def wrapper(*arg,**kw):
			print 'path '+path
			return func(*arg,**kw)
		wrapper.__web_path__ = path
		return wrapper
	return decorator

@route('response1')
def response1():
	return "This is response 1"

@route('response2')
def response2():
	return "This is response 2"


# Useful links: http://wsgi.readthedocs.org/en/latest/learn.html
def app(environ,start_response):
	start_response('200 OK',[('Content-Type','text/html')])
	import my_web
	# medlst is the list containing all the names in my_web module. All in strings.
	medlst = dir(my_web)
	for medname in medlst:
		# Here med is the really attribute, not just a name
		med = getattr(my_web,medname,None)
		# Get the __web_path attribute for med
		attr = getattr(med,'__web_path__',None)
		if attr:
			print 'attr ' + attr
			if attr == environ['PATH_INFO'][1:]:
				return med()
	return "Hello World "+environ['PATH_INFO'][1:]


# An example of the path /this%20is%20only%20a%20test
if __name__ == '__main__':
	http_server = make_server('',8000,app)
	print "start server"
	# dir() (without parameters) returns a list of methods in the current module
	# print dir()

	http_server.serve_forever()
