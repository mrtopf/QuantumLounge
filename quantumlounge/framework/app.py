import werkzeug
import routes

import handler

class Application(object):
    """a base class for dispatching WSGI requests"""
    
    handlers = []
    sub_apps = {} # mapping prefix => application
    
    def __init__(self, settings={}, prefix=""):
        """initialize the Application with a settings dictionary and an optional
        ``prefix`` if this is a sub application"""
        print "***",self,"***", prefix
        self.settings = settings
        self.prefix = prefix
        self.setup_subapps()
        self.setup_mapper()
    
    def setup_subapps(self):
        """set up the sub applications by instantiating them"""
        prefix = self.prefix
        self.sub_mapper = routes.Mapper() # for sub apps
        self.sub_prefixes = {}
        
        for path,app in self.sub_apps.items():
            # instantiate if not instantiated already
            if path[0]!="/": path = "/"+path
            if not isinstance(app, Application):
                app = self.sub_apps[path] = app(self.settings, path)
            # now add to sub mappers
            path = prefix+path
            if path[-1]=='/' and path!="/":
                path = path[:-1]
            print path
            self.sub_mapper.connect(path, app=app)
            self.sub_prefixes[path] = app
        
    def setup_mapper(self):
        """setup the Routes mapper"""
        prefix = self.prefix
        self.mapper = routes.Mapper()
        for path, handler in self.handlers:
        
            path = prefix+path
            if path[-1]=='/' and path!="/":
                path = path[:-1]
            self.mapper.connect(path, handler=handler)
        
    def __call__(self, environ, start_response):
        request = werkzeug.Request(environ)
        path = environ['PATH_INFO']
        
        if len(path)>0 and path[-1]=="/" and path!='/':
            path = path[:-1]

        print "called with %s" %path
        # first check sub apps
        m = self.sub_mapper.match(path)
        if m is not None:
            app = m['app']
            return app(environ, start_response)
        
        for a,v in self.sub_prefixes.items():
            print path, a,v
            if path.startswith(a):
                print "yes"
                return v(environ, start_response)

        m = self.mapper.match(path)
        if m is not None:
            handler = m['handler'](self, request)
            method = request.method.lower()
            if hasattr(handler, method):
                del m['handler']
                response = getattr(handler, method)(**m)
            else:
                return werkzeug.exceptions.MethodNotAllowed()(environ, start_response)
            # call the response
            return response(environ, start_response)        
        # no view found => 404
        return self.process(environ, start_response)
    
    def process(self, environ, start_response):
        """override this for custom request processing in case no route matches"""
        return werkzeug.exceptions.NotFound()(environ, start_response)
