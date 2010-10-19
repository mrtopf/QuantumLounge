from quantumcore.storages.mongoobjectstore import MongoObjectStore, Model
from pymongo.code import Code
import copy

class Content(object):
    """a data model based on quantumcore.storages but copied here to make
    it more flexible. We provide the following features:
        
    * a list of basic attributes a type always needs to provide, like
    ** ``_id`` as the unique id in the storage
    ** ``_parent_id`` pointing to a parent node or ``None``
    ** ``_type`` containing the name of the content type
    ** ``_ancestors`` containing a link of all the ancestores (this is implementation dependant though)
    * a list of additional attributes per type
    * a default set for basic and additional attributes
    * making sure that read only attributes are really just read only
    """

    ###
    ### in a subclass you can override these attributes:
    ###

    _attribs = []
    _defaults = {}
    TYPE = "CONTENT"

    ###
    ### do not change things from on here
    ###

    # base attributes we always need
    _base_attribs = ['_id','_type','_parent_id','_ancestors']
    # additional attributes a type can define
    _base_defaults = {
            '_parent_id' : None,
            '_ancestors' : [],
    }

    def __init__(self, _id=None, _store = None, **kwargs):
        """initialize the database object class. """
        data = copy.copy(self._base_defaults)
        for a,v in self._defaults.items():
            if a in self._base_attribs:
                raise KeyError("default contains key %s which is already in base defaults" %a)
            data[a] = v

        # update defaults with kwargs
        data.update(kwargs)

        # store dictionary as attributes
        for a,v in data.items():
            if a in self._attribs+self._base_attribs and a!="_type":
                setattr(self, a, data[a])

        # now some manual storage of internal attributes
        self._id = _id
        self._store = _store
        if self._ancestors is None:
            self._ancestors = []

        self._after_init()

    def _after_init(self):
        """hook for updating data after init"""

    def _to_dict(self):
        """serialize this object to a dictionary"""
        d={}
        for attrib in self._attribs+self._base_attribs:
            if attrib=='_id' and self._id is None:
                continue
            d[attrib] = getattr(self, attrib, u'')
        return d
    
    @property
    def json(self):
        """return the JSON representation excluding internal attributes"""
        d={}
        for attrib in self._attribs+['_id','_type']:
            d[attrib] = getattr(self, attrib, u'')
        return self.jsonify(d) # eventually convert data

    def jsonify(self, data):
        """hook for converting a dictionary to valid JSON. Input is a
        dictionary in ``data`` which might contain e.g. datetime elements
        which need to be converted to JSON compatible data.

        This hook should return a new (or updated) dictionary. 
        """
        return data

    @classmethod
    def from_dict(cls, d, store):
        """create an entry from the data given in d"""
        d = dict([(str(a),v) for a,v in d.items()])
        d['_store']=store
        return cls(**d)

    def _get_parent(self):
        """return the parent object if it exists or None"""
        pid = self._parent_id
        return self._store.get(pid)

    def _set_parent(self, parent):
        """set the parent object if it exists or None. It also updates
        the ancestor relationships"""
        if parent is not None:
            self._parent_id = parent._id
        else:
            self._parent_id = None
        
    _parent = property(_get_parent, _set_parent)

    @property
    def _type(self):
        """_type is readonly"""
        return self.TYPE

    @property
    def subtree_ids(self):
        """return recursively all children ids of a subtree starting with this node"""
        cids = [f['_id'] for f in self._store.collection.find( { '_ancestors' : self._id }, '_id')]
        return cids

    @property
    def subtree(self):
        """return recursively all children of a subtree starting with this node"""
        return self._store.find({ '_ancestors' : self._id })

    def set_id(self, id_):
        self._id = id_

    def get_id(self):
        return self._id

    oid = property(get_id, set_id)

class ContentManager(MongoObjectStore):
    """This is the base content manager from which all other managers should derive."""

    data_class = Content

    def _after_save_hook(self, folder):
        """compute ancestors for a folder and it's children. This needs
        to be done recursively. We also use direct access to the database
        instead of using objects."""
        coll = self.collection
    
        # first compute our own list
        parent = folder._parent
        if parent is None:
            ancestors = folder._ancestors = []
        else:
            ancestors = copy.copy(parent._ancestors)
            ancestors.append(parent._id)
            folder._ancestors = ancestors
        d = folder._to_dict()
        coll.save(d)

        # now go recursively through all child folders. Every child folder gets
        # the ancestors plus this folder's id as ancestors. 
        # Recursively it's own id is added.
        
        def set_ancestors(folder, ancestors):
            new_ancestors = copy.copy(ancestors)
            new_ancestors.append(folder['_id']) # create the new list
            children = coll.find({'_parent_id':folder['_id']})
            for child in children:
                coll.update({'_id': child['_id']}, {'_ancestors' : new_ancestors})
                set_ancestors(child, new_ancestors)
        
        set_ancestors(d, ancestors)





