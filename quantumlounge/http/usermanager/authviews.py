import werkzeug
import urllib
import simplejson

from quantumlounge.framework import Handler
from quantumlounge.framework.decorators import html, json

import quantumlounge.usermanager as usermanager

from werkzeug.contrib.securecookie import SecureCookie

class Authorize(Handler):
    """handles the OAuth authorize endpoint. For this we need to do the following things:

    * check if the user is logged in by checking the cookie
    * if the user is logged in:
        * create a new auth code for the user
        * return the auth code within the redirect
    * if the user is not logged in:
        * show the login screen
        
    For the :term:`OAuth 2.0` part check out 
    `this section of the OAuth 2.0 spec <http://tools.ietf.org/html/draft-ietf-oauth-v2-10#page-16>`_

    **Allowed Methods** : GET
    
    **URL parameters**
    
    The following OAuth 2.0 parameters are handled:

    * ``response_type`` should be ``code`` (REQUIRED)
    * ``client_id`` is the pre-registered OAuth client id (REQUIRED)
    * ``redirect_uri`` is the URI to which the user manager is supposed to redirect with the auth code (REQUIRED)
    * ``scope`` This is not yet used (and OPTIONAL)
    * ``state`` This is a state variable which is passed back to the client on redirection (OPTIONAL)
    
    **Remarks**
    
    We show the login form via a JavaScript view.
    
    TODO: How are errors handled? They should be shown on the screen as a message which a user
    can understand. So it's actually 200 OK request. We also need to display it with JS probably,
    maybe /authorize#error 
    
    """

    @html
    def error(self, msg):
        return msg

    @html
    def login_form(self):
        """render the login form"""
        return self.app.settings.templates['templates/master.pt'].render(
            pc = self.context,
            js_page_links = self.settings['js_resources']("http.usermanager.authorize"),
            )
        
        
    def get(self):
        args = self.request.args
        response_type = args.get("response_type")
        client_id = args.get("client_id")
        redirect_uri = args.get("redirect_uri")
        scope = args.get("scope")
        state = args.get("state","")

        if response_type is None or client_id is None or redirect_uri is None:
            return self.error("The request invalid")

        data = self.request.cookies.get("l")
        if data is not None:
            login_data = SecureCookie.unserialize(data, self.settings.secret_key)
        else:
            self.settings.log.debug("cookie for user login data not found")
            login_data = {}
        if not login_data.has_key("username"):
            # not logged in, show login form
            self.settings.log.debug("redirecting to login form")
            return self.login_form()
        else: 
            # logged in, retrieve an auth code and do the redirect
            username = login_data['username']
            am = self.settings.authmanager
            try:
                token, auth_code = am.new_token(username, client_id)
            except usermanager.errors.ClientNotFound, e:
                return self.error("the client_id is incorrect")
            q = {
                'code' : auth_code,
                'state' : state,
            }
            url = redirect_uri+"?"+urllib.urlencode(q)
            return werkzeug.redirect(url)

class Login(Handler):
    """handle logging in users. On a POST it will check username and password 
    passed in a form encoded document and return a JSON encoded status document.
    
    This is similar to the API call but we actually set a cookie which is the reason
    why it's duplicated here. (TODO: Is this really necessary? Does the API call make 
    sense at all?)    
    
    This view is used during the :term:`OAuth 2.0` authorization process started with the view above.
    It's called from the JavaScript view.
    
    **Allowed methods**: GET
    
    **form parameters**
    
    * ``username`` (REQUIRED)
    * ``password`` (REQUIRED)
    
    **Return value**
    
    If the user can be logged in this view returns a JSON document like this::
    
        {
            'status' : 'ok',
            'username' : "username",
            'poco' : <portable contacts dict>
        }
    
    In the case of an error it will return JSON as well like this::
    
        {
            'error' : 'CREDENTIALS_WRONG',
            'error_message' : 'error message'
        }
        
    The following errors are defined:
    
    * ``CREDENTIALS_WRONG`` if username and password do not match
    * ``USER_NOT_FOUND`` if the username could not be found in the database
    * ``BAD_REQUEST`` if something else goes wrong, description in the message field.
    
    **Cookie format**
    
    The cookie will only contain the ``username``. We use ``SecureCookie`` from werkzeug here.
    
    """
    
    # TODO: make the error codes lower case 
    # TODO: get rid of status. If error is in the result, then it's an error
    
    @json()
    def error(self, code, msg=u""):
        return {
            'error' : code,
            'error_message': msg
        }

    def post(self):
        """we except ``username`` and ``password`` in a form encoded document"""
        self.settings.log.debug("logging user in")
        f = self.request.form
        username = f.get("username", None)
        password = f.get("password", None)
        if username is None or password is None:
            self.settings.log.debug("login failed: username and pw missing")
            return self.error("bad_request",u"username or password missing")
        
        um = self.app.settings['usermanager']
        user = um.get_by_username(username)
        if user is None:
            self.settings.log.debug("login failed: user %s not found" %username)
            return self.error("user_not_found",u"user not found")
        if password!=user.password:
            self.settings.log.debug("login for %s failed: password wrong" %username)
            return self.error("credentials_wrong",u"username and password do not match")
            
        # apparently we are logged in, so lets set a cookie
        cookie = SecureCookie({
            'username' : user.username
            }, self.settings.secret_key).serialize()

        data = {
            'status' : 'ok',
            'username' : user.username,
            'poco' : user.get_poco()
        }
        self.settings.log.debug("sending data: %s" %data)
            
        res = werkzeug.Response(simplejson.dumps(data))
        res.content_type = "application/json"
        res.set_cookie('l', cookie, httponly=True)
        return res

class AuthCode(Handler):
    """create a new auth token and auth code and return the auth code as JSON to the user
    
    This is another view called from the JavaScript view during the :term:`OAuth 2.0` 
    authorization process. It will check if the user is logged in and if so generate
    an authorization code and access token using the :mod:`quantumcore.usermanager` component.
    
    **Allowed method** : GET

    **URL parameters** 
    
    * ``client_id`` being the client id of the client requesting a token (usually the project management)
    
    Moreover we rely on the login cookie to be set and read the username from it.
    
    TODO: Is the client_id really all we need? 
    
    **Return value**
    
    As JSON::

        q = {
            'code'      : <auth_code>,
        }
        
    If something goes wrong we return the following error document as JSON::
    
        {
            error: '<error_code>',
            error_msg: '<optional error message>'
        }
    
    The following error codes are defined:
    
    * ``unauthorized_client`` if the client id is unkown
    * ``user_not_logged_in`` if the user is not logged in or the cookie couldn't be found
    
    
    TODO: Clean this up, this is doubled code!
    TODO: Test error conditions and success condition
    """
    
    def error(self, error_code, error_message=u""):
        return {
            'error' : error_code,
            'error_message' : error_message
        }

    @json()
    def get(self):
        client_id = self.request.args.get('client_id')
        
        data = self.request.cookies.get("l")
        if data is not None:
            login_data = SecureCookie.unserialize(data, self.settings.secret_key)
        else:
            login_data = {}
        if not login_data.has_key("username"):
            return self.error("user_not_logged_in", "The user is not logged in or the cookie is gone")
        # logged in, retrieve an auth code and do the redirect
        username = login_data['username']
        am = self.settings.authmanager
        try:
            token, auth_code = am.new_token(username, client_id)
        except usermanager.errors.ClientNotFound, e:
            return self.error("unauthorized_client", "The client id is unknown")
        q = {
            'code'      : auth_code,
        }
        return q
