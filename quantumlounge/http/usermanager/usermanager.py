from quantumlounge.framework import Handler, Application
import api

class UserManager(Application):
    """a RESTful user manager"""
    
    handlers = [
        ('/api/login', api.LoginHandler)
    ]