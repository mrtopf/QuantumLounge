import usermanager

def setup_handlers(map):
    """setup the handlers"""
    map.connect(None, '/api/1/login', handler=usermanager.Login)
    #with map.submapper(path_prefix="/api/1"):
        #map.connect(None, '/login', handler=usermanager.Login)
    
