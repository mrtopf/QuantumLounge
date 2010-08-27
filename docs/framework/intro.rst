=========
Framework
=========

This section describes the web framework which is used for some parts of QuantumLounge.

Handlers
========

For every URL you want to handle you have to implement a handler which is a simple
class which needs to implement methods like ``get()``, ``post()`` etc. to correspond
to the HTTP method in use.

A handler can look like this::

    from quantumlounge.framework import Handler
    import werkzeug
    
    class MainHandler(Handler):
        """handle some resource"""
        
        def get(self):
            """handle a GET request"""
            data = self.request.values['data'] # some query param called data
            
            # return a werkzeug Response object
            return werkzeug.Response("my response")
            
Accordingly you can implement ``post()``, ``delete()`` etc.

The handler has the following instance variables:

- ``request`` is the werkzeug request which is holding all request data
- ``app`` is the ``Application`` instance this handler is being called from
- ``settings`` is the global settings dictionary

Should the route which is bound to that handler in the ``Application`` contain
further paramaters like ``/users/{userid}`` then those will be passed as keyword
arguments to the handler methods, e.g.::

    def get(self, userid = None):
        ...
        
        

Application
===========

The application is a WSGI application which uses handlers to do it's work. It is also
possible to use sub application to modularize certain components. 

Lets look at a simple application first::

    from quantumlounge.framework import Application
    
    class MyApp(Application):
    
        def setup_handlers(self, map):
            """setup the mapper"""
            map.connect(None, "/", handler=MainHandler)
        
    app = Application()

You only need to define a ``setup_handlers`` method which gets a map (which is a Routes Mapper) and has to add routes to it. See the 
`Routes documentation <http://routes.groovie.org/>`_ for syntax and other details. Parameters in the path like ``/users/{userid}`` will be passed as keyword arguments to the methods of the chosen handler.

Using sub applications
----------------------

Sometimes it makes sense to not include every URL for every component of the application in this one ``setup_handler()`` method but there is an easy pattern on how to extend it.

Simply import those sub components and call a method of that component to add their own mappings::

    import api
    
        ...
        
        def setup_handlers(self, map):
            
            map.connect(None, "/", handler=MainHandler)
            api.setup_handlers(map)
            
In ``api/__init__.py`` you can define ``setup_handlers()`` as follows::

    import usermanager

    def setup_handlers(map):
        """setup the handlers"""
        with map.submapper(path_prefix="/api/1/users") as m:
            m.connect(None, '/login', handler=usermanager.Login)
            m.connect(None, '/token', handler=usermanager.Token)
            m.connect(None, '/u/{username}/profile', handler=usermanager.PoCo)

Note the ``path_prefix`` which can even be passed in to this local function so that the main application has full control over it's paths. 
            

Application instantiation
=========================

An ``Application`` can be instantiated with the following parameters:

- ``settings`` is a global settings dictionary 
- ``prefix`` is being used to inform the application of the prefix it's running under. This is used for sub applications

An example::

    app = Application({'db': SomeDB()}, '/users')
    
Usually we use a module called ``setup.py`` which holds code to create such a dictionary. Checkout how it's done in the 
`main http application <http://github.com/mrtopf/QuantumLounge/blob/master/quantumlounge/http/setup.py>`_.


Running application
===================

You can e.g. use ``wsgiref`` to run this application::

    if __name__=="__main__":
        app = Application()
        wsgiref.simple_server.make_server('', 8080, app).serve_forever()




