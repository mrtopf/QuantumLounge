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
    
        handlers = [
            ("/", MainHandler),
        ]
        
    app = Application()

That's it and it means to use the ``MainHandler`` we defined above to serve
something on path ``/``. 

The paths are handled using 
`Routes <http://routes.groovie.org/>`_ and thus the same syntax applies here. Parameters
in the path like ``/users/{userid}`` will be passed as keyword arguments to the methods
of the chosen handler.

Application instantiation
=========================

An ``Application`` can be instantiated with the following parameters:

- ``settings`` is a global settings dictionary 
- ``prefix`` is being used to inform the application of the prefix it's running under. This is used for sub applications

An example::

    app = Application({'db': SomeDB()}, '/users')

Running application
===================

You can e.g. use ``wsgiref`` to run this application::

    if __name__=="__main__":
        app = Application()
        wsgiref.simple_server.make_server('', 8080, app).serve_forever()


Sub Applications
================

Sometimes it's useful to not have all functionality in one application. E.g. you
might have different components which work together but can potentially also run
standalone. In this framework this can be done with sub applications.

Imagine a user manager you want to add to your main application which should
run under ``/users``. To do this we first create a new application for it just like
we would do for a primary application::

    class UserManager(Application):
    
        handlers = [
            ('/' : UserListing),
            ('/{id}', UserDetails)
        ]
        
Then we define the main application which "mounts" this application on ``/users``::

    class MainApp(Application):
        
        sub_apps={'users' : UserManager}
        
        handler = [
            ('/' : Index),
        ]
        

That way all requests to ``/users/*`` are directed to the sub application and the sub application itself only defines the relative paths.


