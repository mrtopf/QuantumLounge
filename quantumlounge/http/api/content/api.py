from quantumlounge.framework import RESTfulHandler, json, html
import werkzeug
import simplejson
import uuid

class Item(RESTfulHandler):
    """handle all methods for an item
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

    def _query_objs(self, query):
        """perform the query using the sort order etc. passed in to the 
        request and return a list of JSON formatted objects"""
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
    
        items = self.settings.contentmanager.index(
            query = query,
            sort_on = so,
            sort_order = sd,
            limit = l,
            offset = o
        )
        items = [i.json for i in items]
        return items

    def r_subtree(self, content_id):
        """all recursively all nodes in the subtree of this object"""
        query = {
            '_ancestors' : content_id
        }
        return self._query_objs(query)

    def r_children(self, content_id):
        """return all direct children of this object"""
        query = {
            '_parent_id' : content_id
        }
        return self._query_objs(query)
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
    
        # we need to find all sub objects of this object
        # and sort the results accordingly
        query = {
            '_parent_id' : content_id
        }
        
        items = self.settings.contentmanager.index(
            query = query,
            sort_on = so,
            sort_order = sd,
            limit = l,
            offset = o
        )
        items = [i.json for i in items]
        return items

    def r_default(self, content_id):
        """return the default representation meaning the actual payload"""
        item = self.settings.contentmanager.get(content_id)
        return item.json


    @json()
    def get(self, content_id, format = None):
        """return an index for the tweets"""
        cm = self.settings.contentmanager
        # retrieve object
        r = self.request.args.get("r","default")
        rname = "r_%s" %r
        m = getattr(self, rname, None)
        if m is not None:
            return m(content_id)
        return {'error' : 'representation not found'}

    
