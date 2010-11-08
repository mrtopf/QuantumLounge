from base import Status, StatusCollection
from contenttypes import ContentType

class Folder(Status):
    """a folder"""
    TYPE = "folder"
    _attribs = Status._attribs+['subtypes']
    _defaults = Status._defaults
    _defaults.update({
        'subtypes' : None # means all are allowed
    })

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


class Poll(Status):
    """a poll object. It stores the question as the main status message and
    the answers as a list of lines. It also stores votes in a vote dictionary.
    There's a list of userids for each answer::

        votes = {
            0 : [uid1, uid2, ...],
            1 : [uid1, uid2, ...],
        }

    There is an additional field ``voters`` which stores the list of all voting uids.
    
    """
    TYPE = "poll"
    _attribs = Status._attribs+['answers','votes','voters']
    _defaults = Status._defaults
    _defaults.update({
        'answers' : [],
        'votes' : {},
        'voters' : [],
        })

    def vote(self, answer_no, uid):
        """vote with uid for answer number ``answer_no``
        TODO: Check if answer_no is valid (number and in range)
        """
        self.votes.setdefault(answer_no,[]).append(uid)

    @property
    def results(self):
        """return all results of the poll in the following form::
            'question' : "This is the question",
            'answers' :[
                {
                    'title' : 'Answer Text 3',
                    'votes' : 123,
                },
                {
                    'title' : 'Answer Text 1',
                    'votes' : 98,
                },
                ...
            ],
            'total' : 397

            """
        data = {
                'question' : self.status,
        }
        answers = []
        for answer_no, uids in self.votes.items():
            title = self._answers[answer_no]
            answer = {
                    'title' : title,
                    'votes' : len(uids),
            }
            answers.append(answer)
        answers.sort(lambda x,y: cmp(x['votes'],y['votes']))
        data['answers'] = answers
        data['votes'] = len(self.voters)
        return data

class PollCollection(StatusCollection):
    """manages Polls"""
    data_class = Poll

def PollType(db, coll):
    pc = PollCollection(db, coll)
    return ContentType(
        u"poll",
        name = u"Poll",
        description = "a poll",
        fields = Link._attribs,
        required_fields = ['answers'],
        mgr = pc,
        cls = Poll,
        reprs = ['default', 'atom'],
        default_repr = "default"
    )
