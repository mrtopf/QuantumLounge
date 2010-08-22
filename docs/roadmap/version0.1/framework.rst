=========
Framework
=========

Implement a RESTful handler (DONE)
==================================

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


Implement a nestable Application (DONE)
=======================================

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
        
        sub_apps = {'users' : UserManager}

        handlers = [
            ('/static/{filename:.*?}', StaticHandler),
            ('/js/{filename:.*?}', ResourceHandler),
            ('/css/{filename:.*?}', ResourceHandler),
            ('/', IndexHandler),
        ]

    app = Website(settings)

``app`` in the end is a WSGI server. 



Implement some helper decorators (DONE)
=======================================

The following decorators might be helpful to decorate the HTTP method implementations with:

- ``@json()`` will convert the output of the handler into JSON and wrap it into a werkzeug Response and set the content type to ``application/jsol``. Usually it means to return a dictionary.
- ``@html`` will wrap the output of the handler into a werkzeug Response and set the content type to HTML. In the above example you'd only need to return ``"hey!"``.


Remove the nestable application and use Routes directly
=======================================================

The purpose of the nested application was to be able to modularize e.g. the usermanager
to let it be mounted on any URL prefix. In practice this nesting leads to problem though
if you look at URLs like

/api/1/users

where 1 is actually not a real URL. Here multiple applications are needed for each
level and this is more like traversing.

As we are doing a monolithic application for now we can also use a common list of routes.
They still can be changed later and the usermanager is still independant enough to be
moved out anyday. It can even today already run standalone on it's own port.

Thus the goals are:

- keep the handlers with http methods and decorators
- keep the request creation on ``__call__`` in an application
- let one global application object find the right route match
- maybe let the sub components have their own routes which are simply included
- the sub packages will simply contain the handlers which are all connected together in a more central manner. They also always include the prefix directly


create a basic framework for displaying templates via JavaScript
=============================================================================

What we need to do:

- create a way to package all relevant JS code (template and JS) for a page.
- create a base class for the JS handling.





Some ideas for the JS side in implementing the oauth authorization endpoint::

    var session = {}; // some local store

    function init_page() {
        // get the URL with parameters in params
        session.redirect_uri = params.redirect_uri;
    }

    # show the login screen
    function login() {
        $("content").html(template.login.expand({}));
        $("#loginform").submit(login_sendform);
    }

    function login_sendform() {
        var data = $("#loginform").serialize(); // or however this looks
        function login_error() {
            $("content").html(template.login.expand({'username': data.username, 'error': 'Your login credentials have been wrong!'}));
        }
        $.ajax({
            url: api_prefix+"auth",
            data: data,
            type: "POST",
            dataType: "form",
            success: login_success,
            error: login_error
        });
    }

    function login_success(data, textStatus) {
        if (data.status && data.status==="ok") {
            // now we actually have everything already as granting is automated for now
            // next up we need to redirect the user with an auth code to the redirect uri
            var userid=data.userid;
            $.ajax({
                url: prefix+"/"+userid+"/"+"authcode", // url for retrieving an auth code for the logged in user, only works with that user
                method: "GET",
                success: function(data) {
                    var auth_code = data.auth_code;
                    // craft some URI
                    window.location.href = url;
                }
            });
        }
    }







