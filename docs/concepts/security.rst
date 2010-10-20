=================
Security Concepts
=================

QuantumLounge consists of several web services which need to work together. In
order to make these safe you need to have an access token to access them. This
access token represents the user and the permission attached.

There are 3 main components in the security scenario:

The UserManager
===============

The UserManager can authorize a user and has a profile stored. 
It can also serve as a source for permissions and roles. A third party service
can obtain a user's profile or permission information by using an OAuth access
token which it can obtain from the ``UserManager`` via the OAuth Web Server
flow.

Moreover the ``UserManager`` serves as an Auhorization Manager in that it is
able to act as a access token broker for other services.

The Frontend
============

The frontend binds everything together. It will send the user to the
``UserManager`` in order to authenticate. It uses the received access token
to read user information from the ``UserManager`` and it can pass a security
token on from the ``UserManager`` to the Content API.

It also receives an access token from the Content API in order to be able to
access that API.


The Content API
===============

The Content API serves content. It needs to access the user and the
roles/permissions of that user in order to be able to decide whether an action
on content is allowed or not.

In order to do this it needs to be able to access the permission and user
detail API of the ``UserManager``. For this is need an OAuth access token which
will be passed in from the frontend (or any other entity which is able to
retrieve one).


The Security Flow
=================

Here is a typical flow in the system:

1. The user enters the system via the frontend
2. The frontend sends the user to the ``UserManager`` OAuth authorize location.
   It does this in order to obtain an UserManager OAuth token to access the
   profile information including the user id.
3. The ``UserManager`` probably needs to login the user then in order to be
   able to provide an access token.
4. The user agrees that the frontend receives an access token from the user
   manager (we omit this step and agree automatically for now based on client
   credentials)
5. The frontend receives the access token and retrieves profile information
6. As we defined ``UserManager``, frontend and ``Content API`` to trust each other 
   we only need client credential flows. Thus the Content API only works with
   the right client credentials from the frontend and the User Manager only
   reacts to the right client credentials from the frontend and from the
   content API. 

Care must be taken that no component reacts to some unkown token. Usually
a token is issued by showing the right client credentials (using an SSL secured
connection).




