from quantumlounge.framework import Handler, json
from werkzeug.contrib.securecookie import SecureCookie

class Var(Handler):
    """Var Handler

    Description
    -----------
    
    This handler returns all necessary variables for the JS to work in form of
    a JSON structure. This is:

    * access token for the user manager
    * user_id of the logged in user
    """

    @json()
    def get(self):
        """return the user related data"""
        userdata = self.request.cookies.get("u", None)        
        userdata = SecureCookie.unserialize(userdata, self.settings.secret_key)
        cm = self.settings.contentmanager
        d = {
            'userdata' : userdata,
            'poco' : userdata['poco'],
            'token' : userdata['token'],
            'root' : cm.root.json,
            'types' : cm.content_types.json,
            'scraper' : 'http://pagescraper.mrtopf.clprojects.net'
        }
        return d
