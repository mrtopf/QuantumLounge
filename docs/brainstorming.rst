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


