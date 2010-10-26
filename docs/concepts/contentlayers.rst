==============
Content Layers
==============

There are several layers involved in providing a UI to the user:

1. The **Database Layer** stores and retrieves data objects (usually in MongoDB)
2. The **Content API** is a RESTful layer on top of it. It provides a RESTful
   interface to the database layer.
3. The **UI Layer** uses the RESTful layer to display objects to the user as well
   as let the user modify, add and delete content.

Database Layer
==============

The database layer consists of two elements: A Model class and a Collection
class. These exist for each content type. They are based on
``quantumcore.storages.mongoobjectstore``.

It can be accessed by Python without any restrictions.

Content API
===========

The Content API uses the Database Layer and publishes it to the web as
a RESTful service. To do so it needs to fulfil the following requirements:

* It must restrict access to only those people who have the correct permissions
* It must eventually filter out data which is not supposed to be seen by that
  particular user accessing the data.
* It must be able to process data from the database to e.g. format it for the
  web.
* It must be able to support different formats, e.g. JSON and XML.
* It must support different representations of an object, e.g. a listing of
  sub-objects, a representation with only basic information and a full version.


Access Restrictions
-------------------

Every client is sending an access token along with a request. This access token
is stored in a database and attached to it are permissions or roles. For now we
only use roles.

These roles determine what information can be accessed by that user. You can
see the information attached to a token as a session and this session data
should be available to the implementation.

Thus for a user it might only be allowed to set a password if you are either
that user or have the admin role.

The session is retrieved inside the ``RESTfulHandler`` implementation. It is
available as ``self.session`` variable. 

Where does the session come from?
*********************************

The Session is managed by the session manager. Via default the session manager
is available in ``self.settings.sessionmanager``. If you want to change it you
need to derive from ``RESTfulHandler`` and overwrite the ``sessionmanager``
class variable::

    class MyHandler(RESTfulHandler):

        sessionmanager = "mymanager"

The Session Manager
*******************

The Session Manager is a Model and Collection itself. It has the following
API::

    new_session_id = sm.new(username=username, valid_until datetime.DateTime(...),
            roles=['admin','user','hausmeister']) 
    session = sm[session_id]
    sm.invalidate(session_id)
    sm.invalidate_by_user(username)

Formats
-------

The format is determined by an optional extension, e.g. ``/users/mrtopf.json``
or ``/users/mrtopf.xml``. The format is passed to the handler so it can format
it accordingly. A handler needs to implement methods for converting
a dictionary to the right format.

Representations
---------------

A representation is sort of a view on the data. On folderish objects you might
want to have the following representations:

* A list of all sub-objects
* A small data set with the main metadata of the object itself
* A version which only includes the text which is supposed to be searchable
* A version with all information




