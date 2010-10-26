=============
Content Types
=============

The base types are:

* a ``Folder`` which has a title and can contain other items (unrestricted for
  now)
* a ``Status`` which is a normal text message
* a ``Link`` object which is a status with a link field

``Status`` is the base type. For a Folder the status field is the title, for
a link it's the same but another field is added.


Implementation
==============

The implementation is as follows:

* The database classes are defined in ``content/base.py```, ``folder.py`` and
  ``link.py``.
* The content API is defined in ``http/api/content/``
* The JS UI layer is defined in ``http/content/`` similar to how ``main`` is
  implemented. 
