"""
some useful decorators
"""

import werkzeug
import functools
import simplejson

def html(method):
    """takes a string output of a view and wraps it into a text/html response"""
    
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        response = werkzeug.Response(method(*args, **kwargs))
        response.content_type = "text/html"
        return response

    return wrapper
        

class json(object):
    
    def __init__(self, **headers):
        self.headers = {}
        for a,v in headers.items():
            ps = a.split("_")
            ps = [p.capitalize() for p in ps]
            self.headers["-".join(ps)] = v
    
    def __call__(self, method):
        """takes a dict output of a handler method and returns it as JSON"""

        that = self
    
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            data = method(self, *args, **kwargs)
            s = simplejson.dumps(data)
            if self.request.args.has_key("callback"):
                print "callback"
                callback = self.request.args.get("callback")
                s = "%s(%s)" %(callback, s)
                response = werkzeug.Response(s)
                response.content_type = "application/javascript"
            else:
                response = werkzeug.Response(s)
                response.content_type = "application/json"
            for a,v in that.headers.items():
                response.headers[a] = v
            return response

        return wrapper
        
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
