from quantumlounge.framework import Handler, json, html, RESTfulHandler
import werkzeug
import simplejson

import quantumlounge.usermanager.errors as errors

class Users(RESTfulHandler):
    """handle a collection of Users

    **Allowed Methods**: ALL

    TODO: More documentation in Sphinx about it
    
    """

    # TODO: Do this via the content type?
    collection_name = "usermanager"

    @json() # we assume JSON for now
    def get(self, format='json'):
        um = self.settings[self.collection_name]
        ct = self.settings['content1']['tweet']
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

        content = um.index(
            sort_on = so,
            sort_order = sd,
            limit = l,
            offset = o
        )
        content = [c.json for c in content]
        return content
   
    @json()
    def post(self):
        """Create a new item"""
        f = self.request.form
        print "POSTING", f
        return "ok"
            
class User(RESTfulHandler):
    """single item"""
