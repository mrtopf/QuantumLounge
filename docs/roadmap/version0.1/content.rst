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

- a data model defining it. This might be implemented with
  ``quantumcore.storages``
- an add and edit view for manipulating it. These are HTML snippets and some
  handler managing and storing it.

The main content type should always be the same though which means that we
always have a text field and certain metadata. All the rest can also be seen
as an attachment and one could imaging that also more than one attachment is
added to a tweet in the end.

Thus the model is:

- a folder with an id and eventually a parent id
- a basic tweet object referencing the folder it is inside
- content types as attachment referencing the tweet object
- file etc. on the filesystem or somewhere else. The attachment type
  will know about it

The text field has no label which means it can mean anything:

- title for an event
- title of the link
- task description
- title for a file
- etc.

Workflows will also be defined on attachments.

There can be definitions of required attachments, like a link for a link
object.


a folder structure
------------------

Here we have folder in folders. This means:

- every folder has an id
- every folder has a parent which can be None
- every tweet contains a folder id in which it belongs

We then can create permissions and such on the folders. 

Tasks
-----

- Create a model for the folder type
- Create tests for writing and reading it into a database
- Create folder management APIs


Implement a basic content type
==============================

This content type should have the following attributes:

- tweet content
- creation date
- publishing date
- folder id
- user id
- editing history with timestamp, user id

and possibly more.

Tasks
-----

- Create a model for the basic type
- Create tests for writing and reading it into a database





