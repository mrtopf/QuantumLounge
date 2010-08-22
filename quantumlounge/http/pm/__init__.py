import main

def setup_handlers(map):
    """mapper setup for the project manager"""
    with map.submapper(path_prefix="/pm") as m:
        m.connect(None, '', handler=main.Main)
