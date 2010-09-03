import sys
import os
import pkg_resources
import jinja2
from paste.urlparser import StaticURLParser

from quantumcore.storages import AttributeMapper
from quantumcore.resources import CSSResourceManager, css_from_pkg_stream
from quantumcore.resources import JSResourceManager, js_from_pkg_stream, jst_from_pkg_stream
from quantumlounge.usermanager.users import UserManager
from quantumlounge.usermanager.authorization import AuthorizationManager


def get_static_urlparser(filepath, cache_max_age = 3600):
    return StaticURLParser(filepath, cache_max_age=cache_max_age)


class TemplateHandler(object):
    """a class for caching templates"""

    def __init__(self):
        self._cache = {}

    def get_template(self, filename):
        """retrieve templates and store them inside our PageTemplate cache"""
        #if self._cache.has_key(filename):
            #return self._cache[filename]
        data = pkg_resources.resource_string(__name__, filename)
        t = self._cache[filename] = jinja2.Template(data)
        return t

    __getitem__ = get_template



JS = [
    js_from_pkg_stream(__name__, 'static/js/jquery-1.4.2.min.js', name="jquery", merge=False, prio=1,),
    js_from_pkg_stream(__name__, 'static/js/modernizr-1.5.min.js', name="head", merge=False, prio=1,),

    js_from_pkg_stream(__name__, 'static/js/json-template.js', name="", merge=True, prio=4,),
    js_from_pkg_stream(__name__, 'static/js/tmpl.js', name="", merge=True, prio=4,),
    js_from_pkg_stream(__name__, 'static/js/sammy.min.js', name="", merge=False, prio=4,),
    js_from_pkg_stream(__name__, 'static/js/plugins.js', name="", merge=True, prio=4,),
    js_from_pkg_stream(__name__, 'static/js/script.js', name="", merge=False, prio=5,),
]

CSS = [
    css_from_pkg_stream(__name__, 'static/css/screen.css', merge=True, prio=1, auto_reload=True),
    css_from_pkg_stream(__name__, 'static/css/handheld.css', media="handheld", merge=True, prio=10, auto_reload=True),

    #css_from_pkg_stream(__name__, 'static/css/ie.css', merge=True, prio=11, auto_reload=True),
]

# TODO: Use URL object
DOMAIN = "http://localhost:9991"

def setup(**kw):
    """initialize the setup"""
    settings = AttributeMapper()
    settings['staticapp'] = get_static_urlparser(pkg_resources.resource_filename(__name__, 'static'))
    tmpls = settings['templates'] = TemplateHandler()
    #settings['master_template'] = tmpls['templates/master.pt'].macros['master']
    settings['css_resources'] = CSSResourceManager(CSS, prefix_url="/css", auto_reload=True)
    settings['js_resources'] = JSResourceManager(JS, prefix_url="/js", auto_reload=True)
    
    settings['usermanager'] = UserManager()
    settings['authmanager'] = AuthorizationManager()

    settings['secret_key'] = "czs7s8c6c8976c89c7s6s8976cs87d6" #os.urandom(20)
    
    # settings for the project manager
    pm = AttributeMapper()
    pm.client_id = "pm"
    pm.um_authorize_uri = DOMAIN+"/users/authorize"
    pm.um_token_endpoint = DOMAIN+"/api/1/users/token"
    pm.um_poco_endpoint = DOMAIN+"/api/1/users/u/%s/profile"
    settings['pm'] = pm
    
    # TODO: enable updating of sub settings via dot notation (pm.client_id)
    settings.update(kw)
    return settings






