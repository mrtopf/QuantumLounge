from quantumlounge.framework import Handler, json, html
import werkzeug
import simplejson

import quantumlounge.usermanager.errors as errors

class Login(Handler):
    """handle logging in users. On a POST it will check username and password 
    passed in a form encoded document and return a JSON encoded status document."""
    
    def post(self):
        """we except ``username`` and ``password`` in a form encoded document"""
        f = self.request.form
        username = f.get("username", None)
        password = f.get("password", None)
        if username is None or password is None:
            return werkzeug.exceptions.BadRequest(description=u"username or password missing")
        
        um = self.app.settings['usermanager']
        user = um.get(username)
        if user is None:
            return werkzeug.exceptions.NotFound(description=u"user not found")
        if password!=user.password:
            return werkzeug.exceptions.Unauthorized(description=u"password wrong")
            
        data = {
            'status' : 'ok',
            'username' : user.username,
            'poco' : user.get_poco()
        }
        res = werkzeug.Response(simplejson.dumps(data))
        res.content_type = "application/json"
        return res

class Token(Handler):
    """Retrieve an access token for an authorization code
    
    TODO: Add description of view
    """
    
    def error(self, code="invalid_request", error_message=''):
        return {
            'error' : code,
            'error_message' : error_message
        }

    @json(cache_control = "no-store")
    def get(self):
        code = self.request.args.get("code", None)
        client_id = self.request.args.get("client_id", None)
        if code is None or client_id is None:
            return self.error("invalid_request", "code or client_id missig from request")
        
        # try to obtain an access token for the auth code sent
        am = self.app.settings['authmanager']
        try:
            token = am.get_token_for_code(code, client_id)
        except errors.UserManagerError, e:
            return self.error(e.code, e.msg)

        return {
            'access_token' : token.token,
            'username' : token.username
        }

class PoCo(Handler):
    """Return the Portable Contacts data for a user.
    
    We receive an access token in the request parameters which we will check for validity
    
    TODO: Add description of view
    """
    
    def error(self, code="invalid_request", error_message=u''):
        return {
            'error' : code,
            'error_message' : error_message
        }
    
    @json()
    def get(self, username):
        am = self.app.settings['authmanager']
        um = self.app.settings['usermanager']
        
        access_token = self.request.args.get("access_token", None)
        if access_token is None:
            return self.error(error_message="no access token was given")
        token = am.get_token(access_token, None)
        if token is None:
            return self.error('invalid_grant', 'The authorization token is not valid')
        if token.username != username:
            return self.error('invalid_grant', 'The authorization token is not valid')
        
        # finally do somethign
        u = um.get('mrtopf')
        if u is None:
            return self.error(error_message="no access token was given")
        return u.get_poco()
