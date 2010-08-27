======
/users
======

The user manager is defined in the ``/users`` URL namespace. It handles user management 
and authorization. These views are usually directly used by a user. There might be JavaScript views involved which need to call additional endpoints. These are either
OAuth protected called which go into the ``/api`` namespace or they might need cookies
to be set (like the Authorization views) and then they go under this namespace.

Usually the views needed by a JavaScript view are included in the same Python module
as the view generating that JavaScript view. Moreover they are also prefixed with the original URL.

.. note::

    As an example look into ``authviews.py`` where ``/authorize`` returns a JavaScript
    view which needs to call the ``/authorize/login`` and ``/authorize/authcode``
    endpoints which are in the same file.
    
You can find the implementation in ``http/usermanager/``


/users/authorize
****************

.. autoclass:: quantumlounge.http.usermanager.authviews.Authorize


/users/authorize/login
**********************

.. autoclass:: quantumlounge.http.usermanager.authviews.Login


/users/authorize/authcode
*************************

.. autoclass:: quantumlounge.http.usermanager.authviews.AuthCode

