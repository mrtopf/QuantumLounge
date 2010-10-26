from quantumlounge.framework import RESTfulHandler, json, html
import werkzeug
import simplejson
import uuid

class TweetHandler(RESTfulHandler):
    """return a tweet"""

    @json()
    def get(self, tweet_id):
        """we a tweet id and return the tweet as JSON"""
        ct = self.settings['content1']['tweet']
        tweet = ct.mgr[tweet_id]
        return tweet.json

class ContentHandler(RESTfulHandler):
    """create a tweet and return a list of tweets
    """

    @json(content_type="application/json")
    def post(self, tweet_id=None):
        """create a new tweet"""
        d = self.request.values.to_dict()
        ct = self.settings['content1']['status']
        for field in ct.required_fields:
            if field not in d.keys():
                self.settings.log.error("required field '%s' missing" %field)
                return self.error("required field '%s' missing" %field)
        
        # TODO: Better validation

        # create a new tweet and store it
        tweet = ct.cls(**d)
        tweet.oid = unicode(uuid.uuid4())
        i = ct.mgr.put(tweet)
        tweet = ct.mgr[i]
        return tweet.json

    def error(self, msg):
        return { 'error' : msg }


    @json()
    def get(self):
        """return an index for the tweets"""
        ct = self.settings['content1']['status']
        so = self.request.values.get("so","date") # sort order
        sd = self.request.values.get("sd","down") # sort direction
        try:
            l = int(self.request.values.get("l","10")) # limit
        except:
            return self.error("wrong value for 'l'")
        try:
            o = int(self.request.values.get("o","0")) #offset
        except:
            return self.error("wrong value for 'o'")

        tweets = ct.mgr.index(
            sort_on = so,
            sort_order = sd,
            limit = l,
            offset = o
        )
        tweets = [t.json for t in tweets]
        return tweets
    
