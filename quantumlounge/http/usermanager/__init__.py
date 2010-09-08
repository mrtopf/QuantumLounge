import pkg_resources

import authviews
import master
from quantumlounge.framework import StaticHandlerFactory
from quantumcore.resources import js_from_pkg_stream, css_from_pkg_stream


def setup_handlers(map):
    """setup the handlers for the user facing side of the user manager"""
    with map.submapper(path_prefix="/users") as m:
        m.connect(None, '/templates/{path_info:.*}', handler = StaticHandlerFactory(pkg_resources.resource_filename(__name__, 'templates')))
        m.connect(None, '/authorize/login', handler=authviews.Login)
        m.connect(None, '/authorize/authcode', handler=authviews.AuthCode)
        m.connect(None, '/authorize', handler=authviews.Authorize)
        m.connect(None, '', handler=master.Master)
        

def setup_js():
    return [
        js_from_pkg_stream(__name__, 'authorize.js', name="http.usermanager.authorize", merge=False, prio=5,),
    ]
    
def setup_css():
    return [
        #css_from_pkg_stream(__name__, 'css/usermanager.css', name="http.usermanager", merge=False, prio=5,),
    ]

        
