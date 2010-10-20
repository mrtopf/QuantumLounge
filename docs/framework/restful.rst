===================
Restful Content API
===================

The RESTful API models the content tree available in the system including all 
content types. It has the following features:

* map the content tree to URLs
* permission handling
* mix HTML and machine readable formats

Some examples
=============

* ``/folder1/folder2/`` display the HTML overview for ``folder2``
* ``/folder1/folder2/?fmt=json`` returns the JSON formatted content of
  ``folder2`` which might look like this::

    [
        {'_id' : 'folder1',
         '_type' : 'folder',
         'title' : 'Folder 1',
         'description' : 'This is folder 1'
        },
        {'_id' : '8d78s7zcds87zcs',
         '_type' : 'tweet',
         'content' : 'This is a very cool tweet'
        }
    ]
* You can also select by type and other stuff::
    ``/folder1/folder2?fmt=json&type=tweet&amount=10&start=10&order_by=date&order_dir=asc``


