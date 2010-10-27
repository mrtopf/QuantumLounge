import api

def setup_handlers(map):
    """setup the handlers"""
    with map.submapper(path_prefix="/api/1/content") as m:
        m.connect(None, '/{content_id}{.format}', handler=api.Item)

