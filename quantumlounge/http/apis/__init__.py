from quantumlounge.framework import Handler, Application, json
import usermanager

class APIManager(Application):
    """API handler"""
    
    sub_apps = {
        'users' : usermanager.UserManager,
    }
    