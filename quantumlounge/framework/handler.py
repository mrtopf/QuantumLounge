
class Handler(object):
    """a request handler which is also the base class for an application"""
    
    def __init__(self, app=None, request=None, settings={}):
        """initialize the Handler with the calling application and the request
        it has to handle."""
        
        self.app = app
        self.request = request
        self.settings = settings
        
        
        
        