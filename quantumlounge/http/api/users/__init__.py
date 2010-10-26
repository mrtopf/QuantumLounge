import users

def setup_handlers(map):
    """setup the handlers

    Idea:

    POST on item creates a new sub item
    GET retrieves the default representation (e.g. index listing or details)
    PUT updates an object
    DELETE deletes an object (called on item URL)
    """
    with map.submapper(path_prefix="/api/1/users2") as m:
        # for POST, GET, PUT on the collection
        m.connect(None, '/', handler = users.Users)
        # for POST, GET, PUT on user objects etc. 
        m.connect(None, '/{user}{.format}', handler = users.User)
    
