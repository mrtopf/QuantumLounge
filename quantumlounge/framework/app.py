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
        self.settings = settings
        self.prefix = prefix
        self.setup_mapper()
        self.setup_subapps()
    
    def setup_subapps(self):
        """set up the sub applications by instantiating them"""
        for prefix,app in self.sub_apps.items():
            # instantiate if not instantiated already
            if not isinstance(app, Application):
                self.sub_apps[prefix] = app(self.settings, '/'+prefix)
        
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
        # first check sub apps
        p = environ['PATH_INFO'].split("/")
        if len(p)>1:
            if self.sub_apps.has_key(p[1]):
                return self.sub_apps[p[1]](environ, start_response)

        path = environ['PATH_INFO']
        # TODO: Fix this. We need to decide what a path is supposed to end with
        if len(path)>0 and path[-1]=="/" and path!='/':
            path = path[:-1]
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
