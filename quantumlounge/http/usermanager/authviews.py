from quantumlounge.framework import Handler
from quantumlounge.framework.decorators import html
import werkzeug
from werkzeug.contrib.securecookie import SecureCookie

import quantumlounge.usermanager as usermanager


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

        login_cookie = self.request.cookies.get("l")
        if login_cookie is not None:
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

        
