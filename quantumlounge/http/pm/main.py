import werkzeug
import urllib
import simplejson
from werkzeug.contrib.securecookie import SecureCookie

from quantumlounge.framework import Handler, html


def jsonify(d):
    """return a JSON response"""
    res = werkzeug.Response(simplejson.dumps(d))
    res.content_type = "application/javascript"
    return res
    
class AuthError(Exception):
    """an authorization error. It stores the error handler to be returned"""
    
    def __init__(self, error_handler):
        self.error_handler = error_handler
        
class Token(object):
    """a token representing an access token
    
    TODO: Do we still need this?
    """
    
    def __init__(self, token):
        self.token = token
        

class Main(Handler):
    """Main Handler
    
    Description
    -----------
    
    This handler is the entry point to the project manager. For the project manager to work
    it needs to know the user identity. It stores this in a session cookie. 
    To obtain user identity it needs an access token from the user manager to be able to call
    the Portable Contacts endpoint at ``/users/u/<username>/profile/?format=json``.
    
    The following logic is implemented:
    
    1. Check for the session cookie to obtain user information. If it is there, render
       the main page at ``/pm/#!main``.
    2. If no session is available, redirect the user to ``/users/authorize`` with this
       page as redirect_uri.
    3. If a response with ``code`` as parameter is returned:
        1. retrieve the token 
        2. retrieve the PoCo data
        3. store it in a session 
        4. show the main screen
    
    """

    @html
    def error(self, msg):
        return msg
        
    @html
    def main_view(self):
        """render the login form"""
        return self.app.settings.templates['templates/master.pt'].render(
            pc = self.context,
            initial_view = "pm/main"
        )
        
        return self.app.settings.templates['templates/master.pt'].render(
            handler = self,
            js_jquery_link = self.settings['js_resources']("jquery"),            
            js_head_link = self.settings['js_resources']("head"),
            jslinks = self.settings['js_resources'](),
            csslinks = self.settings['css_resources'](),
            initial_view = "pm/main"
            )

    def start_authorize(self):
        """start the authorization process"""
        url = self.settings.pm.um_authorize_uri
        q = {
            'client_id' : self.settings.pm.client_id,
            'redirect_uri' : self.request.base_url,
            'response_type' : 'code'
        }
        url = url+"?"+urllib.urlencode(q)
        return werkzeug.redirect(url)
        
    def retrieve_token(self, code):
        """retrieve the access token for an auth code"""
        url = self.settings.pm.um_token_endpoint
        q = {
            'code' : code,
            'client_id' : self.settings.pm.client_id
        }
        url = url+"?"+urllib.urlencode(q)
        res = urllib.urlopen(url)
        # TODO: add some error handling here in case if !=200
        # even write a special handler for this which can do it async.
        d = res.read()
        data = simplejson.loads(d)
        if data.has_key('error'):
            raise AuthError("an error occurred. error_code=%(error)s, error_message=%(error_message)s" %data)
        if not data.has_key("access_token"):
            # TODO: What to do about errors which are not supposed to happen?
            raise AuthError("Something technically went wrong. Please try again later")
        return Token(data['access_token'])
        
    def retrieve_userdata(self, token):
        """retrieve the user data"""
        url = self.settings.pm.um_poco_endpoint
        url = url + "?access_token=%s" %token.token
        res = urllib.urlopen(url)
        data = simplejson.loads(res.read())
        return data
        
    def get(self):
        args = self.request.args
        
        # first check if we received an auth_code, if it's valid and if we can show
        # the main view. 
        if args.has_key("code"):
            try:
                token = self.retrieve_token(args['code'])
            except AuthError, e:
                return e.error_handler
                
            userdata = self.retrieve_userdata(token)
            if userdata is None:
                return self.error("error! no user data found")
                
            # remember userdata in this handler
            self.user = userdata
            
            # set the cookie
            cookie = SecureCookie({
                'poco' : userdata,
                'token' : token
            }, self.settings.secret_key).serialize()
            res = self.main_view()
            res.set_cookie("u", cookie)
            return res
        
        # we got no authorization and thus show no main screen yet
        # try to retrieve the user data from the cookie. If this fails, start authorize
        userdata = self.request.cookies.get("u", None)
        if userdata is None:
            return self.start_authorize()
        userdata = SecureCookie.unserialize(userdata, self.settings.secret_key)
        if userdata=={}:
            return self.start_authorize()
            
        # TODO: Maybe we want to check if the access token is still valid and reload
        # the poco data?

        # remember in this handler
        self.user = userdata['poco']
        
        # render the main template
        return self.main_view()
        
