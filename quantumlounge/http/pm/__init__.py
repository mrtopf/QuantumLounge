import main
from quantumcore.resources import js_from_pkg_stream, css_from_pkg_stream

def setup_handlers(map):
    """mapper setup for the project manager"""
    with map.submapper(path_prefix="/pm") as m:
        m.connect(None, '', handler=main.Main)

def setup_js():
    return [
        js_from_pkg_stream(__name__, 'js/timeline.js', name="http.pm.timeline", merge=False, prio=5,),
    ]
    
def setup_css():
    return [
        css_from_pkg_stream(__name__, 'css/pm.css', name="http.pm.timeline", merge=False, prio=5,),
    ]
    