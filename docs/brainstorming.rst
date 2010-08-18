=========
Framework
=========


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



- poco endpoint might check either cookie or access_token
- generalize this!
- can user manager class be directly mapped to API?
    - usermanager.get() can be mapped to GET
    - but needs filtering, e.g. password should be omitted or poco formatting should be applied
    - then again we need to check for a lot of special conditions and the mapping is one line so no automation is probably needed.
    
    


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

Traditional OAuth flow would be as follows:

- annotation notices that it has no information and no access token from the UM
- annotation service redirects user to um
- user logs in and gets redirected back with an access token

This needs to be done for every service.

Requirements for annotation:

- it needs to identify the user via a poco endpoint. 
    - how does it know the username endpoint? 
    - would be easier to just call /poco
- it needs to be able to call the permission API from the PM so it knows if it's allowed
  to return the annotations for this user.
  - how would this API work? What is given to it?

Taking ideas from UMA:

- There is one central authorization manager (AM) which knows all other services
- in this case it would probably be the UM as you are authenticated against it already
- the AM in this case knows about the UM and the PM 
- the AM knows which user is logged in
- the PM knows which user is logged in (has it's user data)
- the annotation service could be bound by 2-legged oauth to the PM as they should trust
  each other and the user needs to trust both.
- if so then the Annotation service only needs a userid and can ask the PM for more 
  information on (userid,url) pairs.
- the userid could be transferred via the embedded JS as a parameter
- the client credentials are on the server side of the annotation service so the JS needs 
  to relay everything through this server.
- can this be gamed?
- user X can also send a forged request to the annotation service to retrieve comments for a page he has no access to. He can claim to be user Y.
- Thus the server side needs to have some cookie. 
- It might get one from the UM through a silent redirect (e.g. in an iframe).
    - It needs to be registered with the UM and have client credentials
    - It redirects to the UM. It needs to be sure that it's the right user manager
      calling, thus it probably needs to be a request signed with the client credentials.
    - The UM can check it's own cookie and returns the username and maybe poco endpoint

PM registration
---------------

- The PM needs to know which user is logged in and it needs user details (poco).
- The PM has a client id and secret
- The user enters the PM
- the PM has a welcome screen which redirects to the UM (or it might be in an iframe)
- there the user logs in
- the UM redirects back with an authorization code
- the PM view exchanges the auth code with an access token 

=> normal OAuth
    
For all components to the UM:

- redirect to UM
- get auth code
- retrieve access token for auth code
- retrieve poco

For all components to the PM:

- do a server-server request with a userid and your client credentials
- retrieve information and give it to the JS part



URL naming
----------

- on /api/<version>/<component> we mount API calls which take access tokens. These are for AJAX etc.
- on /<component>/ we mount calls which take cookies. These are not API as they are called by a user in a browser


