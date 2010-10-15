=======
Folders
=======

Folders can be nested and we for implementing it we derive the model from 
``quantumcore.storages.MongoObjectStore``. 

The API
=======


The Folder class
----------------

A Folder understands the following attributes:

* ``_id`` is the id of the folder which is also used inside a URL.
* ``title`` is the title of the folder
* ``description`` is an optional description of the folder
* ``parent`` points to the parent folder or ``None``. You can also set it.
* ``parent_id`` is the same as above, just as the id
* ``ancestors`` is a list of ancestors of this folder. You should never set
  this!


Initializing the ``FolderManager``
----------------------------------

Here is a snippet to initialize it::

    import pymongo
    from quantumlounge.content.folders import FolderManager

    db = pymongo.Connection().ql_test
    db.drop_collection("folders")
    fm = FolderManager(db,"folders")


.. note:: 
    Usually this setup code should be in ``setup.py`` or any other initialization
    method. In QuantumLounge you can use the following code inside a handler::

        fm = self.settings.folder_manager


Creating a new folder
---------------------

For this you need to instantiate a new ``Folder`` object and put it into the
database::

    from quantumlounge.content.folders import Folder
    f = Folder(_id="root", title="Testfolder")
    new_id = fm.put(f)

Retrieving a folder by id
-------------------------

This can be accomplished like this::
    
    f = fm['root']

Updating a folder
-----------------

Updating is done using the ``update()`` method of the ``FolderManager`` instance::
    
    f = fm['root']
    f.title="new root"
    fm.update(f)

Deleteing a folder
------------------

Deleting is done using the ``delete()`` method of the ``FolderManager`` instance::
    
    fm.delete('root')


Retrieving the ids of all descendants of a folder
-------------------------------------------------

Sometimes it is necessary to retrieve a list of the ids of all the children of 
a folder recursively, e.g. if you want to collect all tweets from all sub
folders. You can do it like this::

    f = fm['root']
    return f.all_cids




