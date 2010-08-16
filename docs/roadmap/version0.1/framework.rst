=========
Framework
=========

Implement a RESTful handler
===========================

Each handler is a class with methods according to HTTP methods, e.g.::

    class MainHandler(Handler):
        
        def get(self):
            ...

        def post(self):
            ...
            
Each handler instance has the following attributes available:

- ``request`` contains a ``Werkzeug.Request`` instance
- ``settings`` contains the ``AttributeMapper`` instance of the global settings
- ``app`` contains the application object which is calling the handler

If the route in the application contained some further attributes like in ``/users/{userid}`` then those will be passed to the handler method, e.g.::

    def get(self, userid=None): 
        ...
        
Each method is supposed to return a ``werkzeug.Response`` instance (but not call it), e.g.::


    def get(self):
        return werkzeug.Response("hey!")


These handlers can easily be unit tested. 


Implement a nestable Application
================================

The handlers need to be attachable to routes it should be able to modularize those handlers. E.g. a ``/users`` url namespace should be handled by one application and
a ``/projects`` namespace by another. These application should not need to know about
their prefix, only the containing application should know.

The application object holds a list of routes with handlers attached and is initialized with a ``settings`` dictionary which holds global configuration for this application.

It should look like this::

    from app import Application
    
    class UserManager(Application):
        ...

    class Website(Application):
        """a website"""
        
        sub_apps = {'users' , UserManager}

        handlers = [
            ('/static/{filename:.*?}', StaticHandler),
            ('/js/{filename:.*?}', ResourceHandler),
            ('/css/{filename:.*?}', ResourceHandler),
            ('/', IndexHandler),
        ]

    app = Website(settings)

``app`` in the end is a WSGI server. 



Implement some helper decorators 
================================

The following decorators might be helpful to decorate the HTTP method implementations with:

- ``@json`` will convert the output of the handler into JSON and wrap it into a werkzeug Response. Usually it means to return a dictionary.
- ``@response`` will wrap the output of the handler into a werkzeug Response. In the above example you'd only need to return ``"hey!"``.






