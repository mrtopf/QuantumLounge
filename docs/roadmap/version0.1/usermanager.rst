============
User Manager
============

store a fixed set of users in a dictionary
------------------------------------------

Data provided:
- username
- password
- full name
- email address

Dictionary format::

    users = [
        {'username' : 'mrtopf',
         'password' : 'foobar',
         'fullname' : 'Christian Scholz',
         'photo'    : 'http://mrtopf.de/profile.png',
         'email'    : 'mrtopf@gmail.com'},
         
         ....
    ]

In version 1 the user manager only has the following methods::

    usermanagager = UserManager()
    user = usermanager['mrtopf']
    
    if usermanager.login('mrtopf', 'foobar'): 
        ...
    print user.email
    print user.username
    print user.fullname
    
    >>> print user.get_poco()
    {
      "id": "mrtopf",
      "thumbnailUrl": "http://mrtopf.de/profile.png",
      "name": {
        "formatted": "Christian Scholz"
      },
      "email" : "mrtopf@gmail.com"
    }

This will be implemented in a module called ``users.py`` inside a class ``UserManager``.
This story has no web API.

User login
----------

URL: ``/users/login``

- show a login form with username and password
- verify credentials on submission
- either login and return "logged in" or show form with error message again
- there can be a ``?popup=true`` parameter to format this for a popup
 

allow OAuth clients to obtain access tokens for a user
------------------------------------------------------

For this we use the `Web Server profile of OAuth2.0 <http://tools.ietf.org/html/draft-ietf-oauth-v2-10#page-10>`_ which works as follows:


1. The client redirects the user to the usermanagers *end-user authorization endpoint*.
2. The user has to login at this endpoint and needs to grant the access token to the client
3. The usermanager redirects the user back to the client with an authorization code
4. The client exchanges the authorization code with an access token at the *token endpoint* of the usermanager

In our story we do it like this:

- We preregister the client id manually between usermanager and project management server
- Granting an access token is done automatically as the client is known. Only login is necessary
- The login URL above will act as the *end-user authorization endpoint* 
- The *token endpoint* will be ``/users/token``


Views to create:

- extend the login view under ``users/authorize`` to
    - eventually login the user if not done yet
    - create an access token
    - create an authorization code
    - redirect the user back to the client based on the ``redirect_uri``
- create a the token endpoint view under ``users/token`` to
    - extract the authorization code
    - retrieve the access token for it
    - return the access token

Implements the following components:


AuthorizationManager
********************

handles everything regarding access tokens and authorization codes.

- ``new_token(username, client_id)`` creates a new access token and an authorization code and returns them for the user and client. It also stores it internally in a list.
- ``get_token(authorization_code)`` returns the access token for that authorization code or an exception if something went wrong. For now only ``NotFound`` is an exception.
- It has a list (of one) ``client_id`` stored statically in a list


allow OAuth clients to obtain profile information for users using the access token
----------------------------------------------------------------------------------

This is implemented by providing the endpoint `/users/<username>?access_token=<access_token>`. 

It will 

- check if the access token is valid and belongs to the username requested
- it will return the user information in Portable Contacts JSON format.



