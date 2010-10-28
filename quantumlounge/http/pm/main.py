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
    
    def __init__(self, msg):
        self.msg = msg
        
class OAuthError(AuthError):
    """an oauth specific error with code and msg"""
    
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg
    
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
    def main_view(self, content_id):
        """render main view"""
        return self.app.settings.templates['templates/master.pt'].render(
            pc = self.context,
            content_id = content_id, # tell the JS where we are, TODO: Make it read this itself
            js_page_links = self.settings['js_resources']("http.pm.main"),
            css_page_links = self.settings['css_resources']("http.pm.main"),
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
        self.settings.log.debug("redirecting to %s" %url)
        
        return werkzeug.redirect(url)
        
    def retrieve_token(self, code):
        """retrieve the access token for an auth code"""
        self.settings.log.debug("retrieving token for code %s" %code)        
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
        self.settings.log.debug("result from token endpoint: %s" %data)        
        if data.has_key('error'):
            raise OAuthError(data['error'], data['error_message'])
        if not data.has_key("access_token"):
            # TODO: What to do about errors which are not supposed to happen?
            raise AuthError("Something technically went wrong. Please try again later")
        return data['access_token']
        
    def retrieve_userdata(self, token):
        """retrieve the user data"""
        self.settings.log.debug("retrieving user data for token %s" %token)
        
        url = self.settings.pm.um_poco_endpoint
        url = url + "?oauth_token=%s" %token
        res = urllib.urlopen(url)
        data = simplejson.loads(res.read())
        self.settings.log.debug("got user data %s" %data)
        return data
        
    def get(self, content_id="0"):
        args = self.request.args
        
        # first check if we received an auth_code, if it's valid and if we can show
        # the main view. 
        if args.has_key("code"):
            self.settings.log.debug("got code '%s' " %(args['code']))
            
            try:
                token = self.retrieve_token(args['code'])
            except AuthError, e:
                self.settings.log.debug("received error on retrieve_token: %s" %e.msg)
                # we now retry the OAuth flow and ignore the OAuth code
                # this can happen if the URL with the code is called again and the server 
                # was restarted inbetween etc.
                return self.start_authorize()
                
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

            # redirect back to this view but without the code
            res = werkzeug.redirect(self.request.base_url)
            res.set_cookie("u", cookie)
            return res
        
        # we got no authorization and thus show no main screen yet
        # try to retrieve the user data from the cookie. If this fails, start authorize
        userdata = self.request.cookies.get("u", None)        
        if userdata is None:
            self.settings.log.debug("no user data found")
            return self.start_authorize()
        userdata = SecureCookie.unserialize(userdata, self.settings.secret_key)
        self.settings.log.debug("found user data: %s" %userdata)
        if userdata.has_key("poco"):
            if userdata['poco'].has_key("error"):
                self.settings.log.debug("userdata contains error, trying again")
                userdata = {}
        else:
            userdata = {}

        if userdata=={}:
            self.settings.log.debug("user data empty, starting OAuth dance")
            return self.start_authorize()
            
        # TODO: Maybe we want to check if the access token is still valid and reload
        # the poco data?

        # remember in this handler
        self.user = userdata['poco']
        
        # render the main template
        return self.main_view(content_id)
        
