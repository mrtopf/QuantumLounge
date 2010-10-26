from base import Status, StatusCollection
from contenttypes import ContentType

class Folder(Status):
    """a folder"""
    TYPE = "folder"

class FolderCollection(StatusCollection):
    """manages folders"""
    data_class = Folder

class Link(Status):
    """a link object"""
    TYPE = "link"
    _attribs = Status._attribs+['link', 'link_title', 'link_image','link_description']
    _defaults = Status._defaults
    _defaults.update({
        'link' : u'',
        'link_title' : u'',
        'link_image' : u'',
        'link_description' : u'',
        })

class LinkCollection(StatusCollection):
    """manages links"""
    data_class = Link


def FolderType(db, coll):
    tm = FolderCollection(db, coll)
    return ContentType(
        u"folder",
        name = u"Folder",
        description = "a folder",
        fields = Folder._attribs,
        required_fields = ['content', 'user'],
        mgr = tm,
        cls = Folder,
        reprs = ['default', 'atom'],
        default_repr = "default"
    )


def LinkType(db, coll):
    tm = LinkCollection(db, coll)
    return ContentType(
        u"link",
        name = u"Link",
        description = "a link",
        fields = Link._attribs,
        required_fields = ['content', 'user', 'link', 'link_title'],
        mgr = tm,
        cls = Link,
        reprs = ['default', 'atom'],
        default_repr = "default"
    )


