=============
Brainstorming
=============


Client - Server - Link
======================

- The client is a JS based application
- It retrieves data via JSON from the server
- The server needs to provide a basic shell template
- The server needs to provide a set of JS files and templates for the client, packaged neatly together
- Make this a JSResource with a name, can be imported on the page which needs it.
- Ship some configuration, e.g. the URL prefix of the API to use.
- API is known between client and server



Example Login
-------------

- Server ships an empty template with JS injected
- It ships a "login" JS package with 
    - the JSON template for the login page
    - a JS to handle it
- Server API:
    - /login?username=<username>&password=<pw> returns either {'status': 'ok'} or a 403 Unauthorized if pw is wrong
        - should probably be POST
    - /authorize is the OAuth 2.0 endpoint
        - the user is redirected here with the following url parameters:
            - response_type = code
            - client_id
            - redirect_uri 
            - scope = "poco"
        - authorization is checked via a cookie
        - if no authorization is available the login form is shown: "/users/authorize#login"
            - "#login" denotes the client side template to be rendered
            - there might be some view on the JS side as well
        - the login is done via AJAX and a cookie is set for this domain 
            - if an error occurred the login screen is shown again
        - (the grant screen is shown)
            - theoretically the grant screen is not needed here if the client id is correct
        - after granting the access, the user is redirected back to the oauth client with an authorization code
            - if access is not granted an error is shown and no auth code is sent back


Example JS code
---------------

Here::

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

This probably should be scoped somehow.

    
    


On Access tokens and permissions
================================


The question is: How do we know what permissions are bound to an access token?

Facts:

- each server which provided an access token can only speak for itself
    - usermanager can check if poco access is allowed. 
    - permissions are authorized by the user. "is client X allowed to do Y?"
    - permissions are the actual scope in OAuth
    
- the problem arises with more than one authorization server
    - each server wants it's own permisson
    
    
Scenario
--------

The project management page is shown, it needs 

- from the usermanager for general information
- from some additional service, e.g. the annotation service

The annotation service also needs username etc. The service itself is included as JS in the project management page and it has it's own server.


PM registration
---------------

- The PM needs to know which user is logged in and it needs user details (poco).
- The PM has a client id and secret
- The user enters the PM
- the PM has a welcome screen which redirects to the UM (or it might be in an iframe)
- there the user logs in
- the UM redirects back with an authorization code
- the PM view exchanges the auth code with an access token 

This is normal OAuth without the grant screen.
    
For all components to the UM
-----------------------------

- redirect to UM
- get auth code
- retrieve access token for auth code
- retrieve poco

For all components to the PM
----------------------------

- do a server-server request with a userid and your client credentials
- retrieve information and give it to the JS part



URL naming
----------

- on /api/<version>/<component> we mount API calls which take access tokens. These are for AJAX etc.
- on /<component>/ we mount calls which take cookies. These are not API as they are called by a user in a browser


JavaScript template handling
============================

We have the following requirements:

* On page load a skeleton template should be rendered
* Optionally a full page should be rendered
* Each page has a set of JS views it wants to display, 
    * the list of activity items
    * input forms
    * new status messages
    * sidebar management
* a JS View is a template with some JS logic 
* JS views are registered in a namespace (var views={})
* how are pages configured?

Lets take the authorize screen as example. It can directly do a redirect but eventually has to show the login form. The login form js a JS view. It's main method is ``render()``.

The following components need to be retrieved:

* the main page
* some general CSS
* some general JS
* the initial JS views
* some configuration parameters

Idea:

* We load the URL ``/authorize/`` which redirects to ``/authorize/#!login_form`` if a login is necessary
* The view handler code detects the fragment identifier and loads the JS for ``login_form``. It might be relative to ``/authorize``, e.g. ``/authorize/js/login_form``
* The ``render()`` method of ``login_form`` is called.

How to serve that?
------------------

* We have a JS resource for the view mounted at ``/authorize/js/login_form``
* It has a JST and a JS component
* We need to change the JST importer for this


Problem with the existing dummy JS solution
===========================================

- We pass in the initial_view now but evenatually a lot of slots need to be filled
  when entering a screen. e.g. on the PM screen we need to fill the form, the list of
  statuses and the sidebar, probably more..
- How does the JS code know about the access token? Or wouldn't it need to? Maybe the API
  can also check for cookies and access tokens? That way the access token is hidden from
  the user. 
- We nevertheless need some way of passing in data from the server to the JS.

Ideas
-----

- Each page needs to have it's own JS attached. It can be loaded via a name
- Each page could initialize that itself by simply providing $(document).ready()
- Data might be passed in while rendering, e.g. it could render a JSON string into the 
  template which is evaluated then.
  

Attaching the JS for a page
---------------------------

We do this in setup::

    js_from_pkg_stream(__name__, 'static/js/pages/<pagename>.js', name="pagename", merge=True, prio=4,)
    
Maybe this can be simplified and included in the page code itself?

Passing variables
-----------------

The server side code adds a template var ``js_vars`` which is a JSON string. It will be inserted into the master template as ``js_vars`` and evaluated automatically by some generic view class we derive from.




    








