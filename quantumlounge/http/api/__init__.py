import usermanager

def setup_handlers(map):
    """setup the handlers"""
    with map.submapper(path_prefix="/api/1/users") as m:
        m.connect(None, '/login', handler=usermanager.Login)
    
