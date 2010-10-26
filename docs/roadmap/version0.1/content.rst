=============
Content Types
=============

Create a data model
===================

The data model should support the following components:

Tweets as content types
-----------------------

There should be different types of tweet objects, some might have links, some
are events, some are tasks or bug reports. Every tweet object thus has

- a data model defining it. This will be implemented with ``quantumcore.storages``
- a RESTful content API protected by OAuth access tokens. For now we reuse the
  Usermanager access token, later on we will have our own one.
- A JS UI for manipulating those content objects via the RESTful API.

All content types are derived from a base ``Status`` type and the types to
implement are ``Folder`` and ``Link`` additionally.

The actual ``content`` of the ``Status`` object will be reused as title for the
Folder.

a folder structure
------------------

Here we have folder in folders. This means:

- every folder has an id
- every folder has a parent which can be None
- every folder has a list of ancestors
- every content is embedded in a folder like object except the root object

Tasks
-----

- Create a model for the base type, folder and link object
- Implement a generic path based RESTful API
- Secure it via OAuth access tokens
- think about a JS UI for these things. 
- Create tests for writing and reading it into a database


