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

    The following OAuth 2.0 parameters are handled:

    * ``response_type`` '''REQUIRED'''
    * ``client_id`` '''REQUIRED'''
    * ``redirect_uri`` '''REQUIRED'''
    * ``scope`` '''OPTIONAL''' (we only support "poco" for now which is the default anyway)
    * ``state`` '''OPTIONAL''' (need to be remembered)

    TODO: How are errors handled? They should be shown on the screen as a message which a user
    can understand. So it's actually 200 OK request. We also need to display it with JS probably,
    maybe /authorize#error 
    
    TODO: Add login form

    """

    @html
    def error(self, msg):
        return msg

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
            login_data = {}
        if not login_data.has_key("username"):
            # not logged in, show login form
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
    
    Additionally it will set a cookie to mark the user as logged in.
    
    In the case of an error it will return JSON as well like this::
    
        {
            'error' : 'CREDENTIALS_WRONG',
            'error_message' : 'error message'
        }
        
    The following errors are defined:
    
    * ``CREDENTIALS_WRONG`` if username and password do not match
    * ``USER_NOT_FOUND`` if the username could not be found in the database
    * ``BAD_REQUEST`` if something else goes wrong, description in the message field.
    
    """
    
    @json
    def error(self, code, msg=u""):
        return {
            'error' : code,
            'error_message': msg
        }

    def post(self):
        """we except ``username`` and ``password`` in a form encoded document"""
        f = self.request.form
        username = f.get("username", None)
        password = f.get("password", None)
        if username is None or password is None:
            return self.error("BAD_REQUEST",u"username or password missing")
        
        um = self.app.settings['usermanager']
        user = um.get(username)
        if user is None:
            return self.error("USER_NOT_FOUND",u"user not found")
        if password!=user.password:
            return self.error("CREDENTIALS_WRONG",u"username and password do not match")
            
        # apparently we are logged in, so lets set a cookie
        cookie = SecureCookie({
            'username' : user.username
            }, self.settings.secret_key).serialize()

        data = {
            'status' : 'ok',
            'username' : user.username,
            'poco' : user.get_poco()
        }
            
        res = werkzeug.Response(simplejson.dumps(data))
        res.content_type = "application/json"
        res.set_cookie('l', cookie, httponly=True)
        return res

