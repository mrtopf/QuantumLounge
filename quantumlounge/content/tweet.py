from quantumlounge.content import Model, Collection, Status, StatusCollection
from contenttypes import ContentType
import datetime

class Tweet(Status):
    """example content type defining a tweet"""
    TYPE = "tweet"

class TweetManager(StatusCollection):
    """manages tweets"""

    data_class = Tweet


def TweetType(db, coll):
    tm = TweetManager(db, coll)
    return ContentType(
        u"tweet",
        name = u"Tweet",
        description = "a status message",
        fields = Tweet._attribs,
        required_fields = ['content', 'user'],
        mgr = tm,
        cls = Tweet,
        reprs = ['default', 'atom'],
        default_repr = "default"
    )

