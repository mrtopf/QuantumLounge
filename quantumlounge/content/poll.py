from basetypes import Status, StatusCollection
from contenttypes import ContentType

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
        })

    def vote(self, answer_no):
        """vote for answer number ``answer_no``
        TODO: Check if answer_no is valid (number and in range)
        """
        votes = self.votes.get(answer_no, 0)
        votes = votes +1
        self.votes[answer_no] = votes

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
                'question' : self.content,
        }
        answers = []
        i=0
        total=0
        for title in self.answers:
            votes = self.votes.get(str(i),0)
            answer = {
                    'title' : title,
                    'votes' : votes
            }
            total=total + votes
            answers.append(answer)
            i=i+1
        answers.sort(lambda x,y: cmp(y['votes'],x['votes']))
        data['answers'] = answers
        data['votes'] = total
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
        fields = Poll._attribs,
        required_fields = ['answers'],
        mgr = pc,
        cls = Poll,
        reprs = ['default', 'atom'],
        default_repr = "default"
    )


