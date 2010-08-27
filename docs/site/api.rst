====
/api
====

In the ``/api`` namespace we have all those views which make up the API. This means that

* these views do not render HTML
* these views are mostly protected by some :term:`OAuth 2.0` access token

We also denote the API version in the URL as second part of it like this::

    /api/1/apimethod
    
Usually we also further scope individual API components by a URL namespace.

You can find the implementation in ``http/api/``


/api/1/users/login
******************

.. autoclass:: quantumlounge.http.api.usermanager.Login


/api/1/users/token
******************

.. autoclass:: quantumlounge.http.api.usermanager.Token



/api/1/users/u/<username>/profile
*********************************

.. autoclass:: quantumlounge.http.api.usermanager.PoCo

