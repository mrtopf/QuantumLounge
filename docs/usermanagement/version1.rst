=========
Version 1
=========

Stories
=======

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
 

allow OAuth clients to obtain access tokens for a user
------------------------------------------------------







allow OAuth clients to obtain profile information for users using the access token
----------------------------------------------------------------------------------







