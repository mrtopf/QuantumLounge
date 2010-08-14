import uuid

import errors

class Token(object):
    """an Access token for OAuth based authorization"""
    
    def __init__(self, username, client_id):
        """create a new token"""
        self.username = username
        self.client_id = client_id
        self.token = uuid.uuid4() 

class AuthorizationManager(object):
    """the AuthorizationManager handles everything around OAuth based authorization
    such as access tokens, authorization codes and clients"""
    
    client_ids = ['pm'] # our one client id for now
    tokens = {} # the list of tokens this manager manages
    authorization_codes = {} # mapping from code -> access token
    
    
    def new_token(self, username, client_id):
        """create a new access token and authorization code for it and
        store it related to this user"""
        if client_id not in self.client_ids:
            raise errors.ClientNotFound(client_id)
        token = Token(username, client_id)
        auth_code = uuid.uuid4()
        
        self.authorization_codes[auth_code] = token
        self.tokens[token.token] = token
        
        return token.token, auth_code
        
    def get_token(self, authorization_code, client_id):
        """return the token for the given authorization code. Will raise an
        ``AuthorizationCodeNotFound`` exception if it's not found"""
        if self.authorization_codes.has_key(authorization_code):
            token = self.authorization_codes[authorization_code]
            if token.client_id != client_id:
                raise errors.InvalidAuthorizationCode(authorization_code, client_id)
            return token
        raise errors.AuthorizationCodeNotFound(authorization_code)