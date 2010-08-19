import authviews

def setup_handlers(map):
    """setup the handlers for the user facing side of the user manager"""
    with map.submapper(path_prefix="/users") as m:
        m.connect(None, '/authorize', handler=authviews.Authorize)

