from base import Content, ContentManager
from contenttypes import ContentType
import datetime

class Tweet(Content):
    """example content type defining a tweet"""
    TYPE = "tweet"
    _attribs = ['content','date','user']
    _defaults = {
        'content' : u'',
        'date' : None,
        'user' : u'',
    }

    def _after_init(self):
        """fix data"""
        self.date = datetime.datetime.now()

class TweetManager(ContentManager):
    """manages tweets"""

    data_class = Tweet


def TweetType(db, coll):
    tm = TweetManager(db, coll)
    return ContentType(
        u"tweet",
        name = u"Tweet",
        description = "a status message",
        fields = Tweet._attribs,
        required_fields = ['content'],
        mgr = tm,
        cls = Tweet,
        reprs = ['default', 'atom'],
        default_repr = "default"
    )

