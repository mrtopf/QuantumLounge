import pkg_resources
import main
import var
from quantumlounge.framework import StaticHandlerFactory
from quantumcore.resources import js_from_pkg_stream, css_from_pkg_stream

def setup_handlers(map):
    """mapper setup for the project manager"""
    with map.submapper(path_prefix="/pm") as m:
        m.connect(None, '/templates/{path_info:.*}', handler = StaticHandlerFactory(pkg_resources.resource_filename(__name__, 'templates')))
        m.connect(None, '', handler=main.Main)
        m.connect(None, '/var', handler=var.Var)
        m.connect(None, '/{content_id}', handler=main.Main)

def setup_js():
    return [
        js_from_pkg_stream(__name__, 'main.js', name="http.pm.main", merge=False, prio=5, auto_reload=True),
    ]
    
def setup_css():
    return [
        css_from_pkg_stream(__name__, 'pm.css', name="http.pm.main", merge=False, prio=5,auto_reload=True),
    ]
    
