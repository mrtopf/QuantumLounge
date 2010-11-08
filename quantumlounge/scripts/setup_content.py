"""

script for setting up the base content. We fill the database manually.
We do the following:

* delete all the content
* setup a root node (folder)
* setup two folders: links and messages
* setup some test folders: root/A/B/C/D

"""

import pymongo
import uuid
import datetime
from quantumlounge.content.basetypes import Folder, FolderCollection

def do():
    db = pymongo.Connection().pm
    coll = db.contents
    coll.remove() # delete it

    fm = FolderCollection(db, 'contents')

    # find the user
    user = db.users.find_one()
    uid = unicode(user['_id'])

    # setup the root node
    rf = Folder(_id = "0", user=uid, content="root")
    rfid = fm.put(rf)
    
    f1 = Folder(user=uid, content="links", _parent_id=rfid, subtypes=['link'])
    f2 = Folder(user=uid, content="messages", _parent_id=rfid, subtypes=['status'])
    fm.put(f1)
    fm.put(f2)

    f = Folder(user=uid, content="Folder A", _parent_id=rfid)
    fid = fm.put(f)
    f = Folder(user=uid, content="Folder B", _parent_id=fid)
    fid = fm.put(f)
    f = Folder(user=uid, content="Folder C", _parent_id=fid)
    fid = fm.put(f)
    f = Folder(user=uid, content="Folder D", _parent_id=fid)
    fid = fm.put(f)
    f = Folder(user=uid, content="Folder E", _parent_id=fid)
    fid = fm.put(f)

if __name__ == '__main__':
    do()
