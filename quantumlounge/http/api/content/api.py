from quantumlounge.framework import RESTfulHandler, json, html
import werkzeug
import simplejson
import uuid
import functools
import pprint

class role(object):
    """check if roles are present in the session"""
    def __init__(self, *roles):
        self.roles = roles

    def __call__(self, method):
        """creating a wrapper to check roles. We do this as follows:
            
        * get the session via the access token
        * retrieve the roles of the user from the session
        * check if one of the roles given to the decorator is inside the session
        """
   
        possible_roles = self.roles
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            session = self.session
            if session is None:
                roles = []
            else:
                roles = session.roles
            if len(set(possible_roles).intersection(set(roles)))==0:
                # TODO: find a better way
                self.settings.log.error("access for session %s not authorized: roles needed: %s, roles found: %s"
                        %(session, possible_roles, roles))
                return None
            return method(self, *args, **kwargs)
        return wrapper

class Item(RESTfulHandler):
    """handle all methods for an item
    """

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

    @role("admin")
    def r_subtree(self, content_id):
        """all recursively all nodes in the subtree of this object"""
        query = {
            '_ancestors' : content_id
        }
        return self._query_objs(query)

    def r_jsview(self, content_id):
        """return a JSON structure of the most recent item of the given
        type which is passed in as ``jsview_type`` in the request"""
        t = self.request.args.get("jsview_type","status")
        query = {
            '_ancestors' : "0",
            '_type' : t
        }
        return self._query_objs(query)

    @role("admin")
    def r_parents(self, content_id):
        """all recursively all nodes in the subtree of this object"""
        ct = self.settings.contentmanager
        item = ct.get(content_id)
        ancestors = item._ancestors
        res = []
        for a in ancestors:
            res.append(ct.get(a).json)
        return res

    @role("admin")
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

    @role("admin")
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
            return {r : m(content_id)}
        return {'error' : 'representation not found'}

    
    @json(content_type="application/json")
    @role("admin")
    def post(self, content_id, format = None):
        """POSTing to an item means creating a new one"""
        d = self.request.values.to_dict()
        d['_parent_id'] = content_id
        _type = d['_type']
        ct = self.settings['content1'][_type]
        for field in ct.required_fields:
            if field not in d.keys():
                self.settings.log.error("required field '%s' missing" %field)
                return self.error("required field '%s' missing" %field)
       
        # create a new tweet and store it
        item = ct.cls(**d)
        item.oid = unicode(uuid.uuid4())
        i = ct.mgr.put(item)
        item = ct.mgr[i]
        # post the new item back
        return item.json

    
