from quantumcore.storages import AttributeManager
import copy

class ContentType(AttributeManager):
    """base type for content types. A content type is mostly a dictionary and
    we use this class to define it's attributes"""

    def __init__(self, data):
        """initialize a content type"""

        default = {
            'id' : None,            # required
            'name' : u'',           # human readable name
            'description' : u'',    # human readable description
            'contains' : [],        # list of content type it is allowed to contain or 'all', empty means none
            'fields' : [('title': 'string')],        # list of fields and types this type understands
            'required_fields' : ['title'],          # list of required fields
            'reprs' : ['default', 'contents'],          # list of representations
            'default_repr' : 'default',          # default representation
        }

        d = copy.copy(default)
        d.update(data)

class ContentTypeManager(AttributeManager):
    """a content type manager which is simply a dictionary"""


