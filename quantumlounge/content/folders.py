from quantumcore.storages.mongoobjectstore import MongoObjectStore, Model
from pymongo.code import Code
import copy

class Folder(Model):
    """a folder object with a parent"""
    _attribs = ['_id','title','description','parent_id','ancestors']
    _defaults = {
            'parent_id' : None,
            'description' : '',
            'title' : '',
            'ancestors' : [],
    }

    def _after_init(self):
        """fix data"""
        if self.ancestors is None:
            self.ancestors = []

    def _get_parent(self):
        """return the parent object if it exists or None"""
        pid = self.parent_id
        return self._store.get(pid)

    def _set_parent(self, parent):
        """set the parent object if it exists or None. It also updates
        the ancestor relationships"""
        if parent is not None:
            self.parent_id = parent._id
        else:
            self.parent_id = None
        
    parent = property(_get_parent, _set_parent)

    @property
    def all_cids(self):
        """return recursively all children ids of a subtree starting with this node"""
        cids = [f['_id'] for f in self._store.collection.find( { 'ancestors' : self._id }, '_id')]
        return cids

class FolderManager(MongoObjectStore):
    """manages folders"""

    data_class = Folder

    def _after_save_hook(self, folder):
        """compute ancestors for a folder and it's children. This needs
        to be done recursively. We also use direct access to the database
        instead of using objects."""
        coll = self.collection
    
        # first compute our own list
        parent = folder.parent
        if parent is None:
            ancestors = folder.ancestors = []
        else:
            ancestors = copy.copy(parent.ancestors)
            ancestors.append(parent._id)
            folder.ancestors = ancestors
        d = folder._to_dict()
        coll.save(d)

        # now go recursively through all child folders. Every child folder gets
        # the ancestors plus this folder's id as ancestors. 
        # Recursively it's own id is added.
        
        def set_ancestors(folder, ancestors):
            new_ancestors = copy.copy(ancestors)
            new_ancestors.append(folder['_id']) # create the new list
            children = coll.find({'parent_id':folder['_id']})
            for child in children:
                coll.update({'_id': child['_id']}, {'ancestors' : new_ancestors})
                set_ancestors(child, new_ancestors)
        
        set_ancestors(d, ancestors)



