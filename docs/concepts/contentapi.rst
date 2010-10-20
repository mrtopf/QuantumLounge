===============
The Content API
===============

The Content API is for storing and managing content. It is path oriented and
access is granted via OAuth access tokens. 

The Content API is based on Content Types. Each type defines the following
things:

* an id of the type (no spaces etc.)
* the name of the type (for human consumption)
* a description
* if it can contain other types
* which other types it is allowed to contain
* a list of possible representations (view, rss entry etc.)

Content Types are defined as dictionaries like this::

    tweet = {
        'id' : 'tweet',
        'name' : 'Tweet',
        'description' : 'A Tweet',
        'contains' : ['File Attachment', 'Link Attachment'],
        'representations' : ['content','view','rss','atom']
        'default_representation' : 'view'
    }


The Content Type Manager
========================

These definitions are configured in the startup code of the framework, e.g. in
``setup.py``. They are stored inside the ``ContentTypeManager`` component::

    ctm = ContentTypeManager()
    ctm.register(tweet)

You can also retrieve a definition again::

    tweet_type = ctm['tweet']

You can get a listing of all types::
    
    types ctm.all


The basic API
=============

The Content Type API basically resembles a containment based content tree by URLs. 
Thus you can address content by knowing it's URL or traversing through
containers::

    GET /folder1/folder2/tweet25252

This will return the default representation. You can also request e.g. the rss
representation::


    GET /folder1/folder2/tweet25252?r=rss

You can also update an entry by POSTing to it::

    POST /folder1/folder2/tweet25252?title=This+is+cool




