from quantumlounge.framework import Handler, json, html
import werkzeug
import simplejson

import quantumlounge.usermanager.errors as errors

class Login(Handler):
    """handle logging in users. On a POST it will check username and password 
    passed in a form encoded document and return a JSON encoded status document.
    
    **Allowed Methods**: POST
    
    **Form parameters**: ``username`` and ``password`` have to denote a valid user account.
    Both fields are REQUIRED.
    
    **Return value**: On success it will return the following JSON document::
        
        {
            'status' : 'ok',
            'username' : '<username>',
            'poco' : '<poco data>'
        }
    
    If an error occurred it will return one of the following HTTP errors:
    
    * ``400 Bad Request`` if a required field is missing.
    * ``404 Not Found`` if the user was not found
    * ``401 Unauthorized`` if the username and password did not match
            
    """
    
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
    """Retrieve an access token for an authorization code. This call is used during the 
    :term:`OAuth 2.0` web server flow. The client has an authorization code and wants to exchange 
    it with an access token. For more information check out 
    `the OAuth specification on the token exchange <http://tools.ietf.org/html/draft-ietf-oauth-v2-10#page-21>`_
    
    .. note::
    
        Note that we only support the web server flow at this point and thus only the
        ``authorization_code`` grant type. 
        
    
    **Allowed Methods**: GET
    
    **URL parameters**: 
    
    * ``grant_type`` being ``authorization code`` (REQUIRED)
    * ``client_id`` being the registered client id (REQUIRED)
    * ``code`` the authorization code provided by the authorization endpoint (REQUIRED)
    * ``redirect_uri`` the same redirect URI  provided to the authorization endpoint to check for security reasons (REQUIRED) (TODO)
    * ``scope`` the scope also provided to the authorization endpoint. We ignore this for now. (OPTIONAL)
    
    **Return value**: On success it will return the following JSON document::
        
        {
          "access_token" : "<access token>",
          "username" : "<username>",
        }
        
    .. note::
        
        The ``username`` field is not part of OAuth 2.0 but we put it here for simplicity for now.
        This will be replace by a ``@me`` PoCo endpoint soon.
        
    If an error occurred it will return a JSON document like this::

        {
            'error' : code,
            'error_message' : error_message
        }
        
    Possible error codes are:

        * ``invalid_request`` a required parameter was missing from the request
        * ``unauthorized_client`` if the authorization code is not found or invalid
        * ``invalid_client`` if the client_id is invalid

    """

    # TODO: Implement the check for the grant_type and redirect_uri check.
    # TODO: remove the username from the response after poco change.
    
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
    """Return data about a user using the :term:`Portable Contacts` format.
    
    **Allowed Methods**: GET
    
    **URL parameters**: 
    
    * ``access_token`` needs to be valid :term:`OAuth 2.0`` access token
    
    The username is part of the path.
    
    **Return value**: On success it will return a :term:`Portable Contacts` formatted JSON document, e.g.::
        
        {
            "id": 'mrtopf',
            "thumbnailUrl": 'http://...',
            "name": {
                "formatted": 'Christian Scholz,
            },
            "email" : 'somewhere@on.earth.com'
        }
        
    If an error occurred it will return a JSON document like this::

        {
            'error' : code,
            'error_message' : error_message
        }
        
    Possible error codes are:
    
    * ``invalid_grant`` if the access token is invalid because it's not found or does not match the user it was issued for
    * ``invalid_request`` the access token is missing from the request)
    
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
