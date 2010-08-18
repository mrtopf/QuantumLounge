===============================
HTTP interface for User Manager
===============================

cerate a user manager application
---------------------------------

Create a application for exposing the user manager via HTTP API
under ``/users``.


create a login API method under /user/api/login (DONE)
-------------------------------------------------------

Create a handler for the user manager listening on ``/api/login`` and
taking a username and password via POST, checking it and either returning an HTTP error
or returning a status=ok, username and poco contents.

add cookie handling to the login
--------------------------------

extend the login API with some new parameter "cookie=1" which is supposed to set
a cookie on login. Further login attempts are supposed ignore the cookie though.

This is supposed to be used via AJAX. 


implement /authorize
--------------------

The basic workflow is OAuth:

- a third party component calls ``/authorize``
- we check if the user is logged in, if not show the login screen
- after login we automatically grant an access token and store it in the database
- we redirect back with the generated auth code to the third party
- on another endpoint we allow an auth code to be exchanged by an access token

Javascript implementation
*************************

In this case we implement all screens with javascript, in this case only the login screen.

- on authorize we check if we can directly redirect back or not. If so, we do with an auth code. This is the case if the user is logged in
- The following parameters are given:
    - response_type = "code"
    - client_id
    - redirect_uri 
    - scope = "poco" which probably is not needed as it's all we have anyway
    - an optional state
    
- for login the server serves an empty template and some JS code with templates
- the JS code displays a template with a login form
- the user enters some data 
- the form is submitted to ``api/login`` and a response is returned
- if login was not ok, errors are displayed with the same form
- the JS now can redirect back to authorize actually as it will redirect now
- otherwise the JS can retrieve an auth code for the user at ``/users/auth_code`` 
  which will return an auth code for the logged in user. It can then do the redirect.

Endpoints
*********

- ``/um/authorize`` checks if the user is logged in and does a redirect if so and shows  ``/um/authorize/#login`` if it's not the case.
- ``#login`` displays the login form via JS (all included in the page returned by authorize)
- ``/um/login`` logs the user in and remembers a cookie. It's AJAX but with a cookie.
- ``/um/get_auth_code`` creates a new auth code and returns it as JSON (AJAX call). It uses cookie information to attach the right user.
- ``/api/token`` returns a token for an auth code.
