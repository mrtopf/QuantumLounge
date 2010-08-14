class UserManagerError(Exception):
    """just a base class for all exceptions around the user manager"""
    
class UserNotFound(UserManagerError):
    """a user was not found in the database"""
    
    def __init__(self, username):
        self.username = username
        
class ClientNotFound(UserManagerError):
    """exception raised if an unkown client_id is retrieved"""
    
    def __init__(self, client_id):
        """store client id in question"""
        self.client_id = client_id
        
class AuthorizationCodeNotFound(UserManagerError):
    """exception raised if an unkown auth code is retrieved"""
    
    def __init__(self, auth_code):
        self.auth_code = auth_code
        
class InvalidAuthorizationCode(UserManagerError):
    """exception raised if authorization code and client do not match"""
    
    def __init__(self, auth_code, client_id):
        self.auth_code = auth_code
        self.client_id = client_id
