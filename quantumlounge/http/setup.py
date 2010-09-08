import sys
import os
import pkg_resources
import logbook

from quantumcore.storages import AttributeMapper
from quantumcore.resources import CSSResourceManager, css_from_pkg_stream
from quantumcore.resources import JSResourceManager, js_from_pkg_stream, jst_from_pkg_stream
from quantumlounge.usermanager.users import UserManager
from quantumlounge.usermanager.authorization import AuthorizationManager

from quantumlounge.framework.utils import get_static_urlparser, TemplateHandler


JS = [
    js_from_pkg_stream(__name__, 'static/js/jquery-1.4.2.min.js', name="jquery", merge=False, prio=1,),
    js_from_pkg_stream(__name__, 'static/js/modernizr-1.5.min.js', name="head", merge=False, prio=1,),

    js_from_pkg_stream(__name__, 'static/js/jsuri-1.0.2-min.js', name="", merge=True, prio=1,),
    js_from_pkg_stream(__name__, 'static/js/sammy.js', name="", merge=False, prio=2,),
    js_from_pkg_stream(__name__, 'static/js/sammy.template.js', name="", merge=False, prio=3,),

    js_from_pkg_stream(__name__, 'static/js/json-template.js', name="", merge=True, prio=4,),
    js_from_pkg_stream(__name__, 'static/js/tmpl.js', name="", merge=True, prio=4,),
    js_from_pkg_stream(__name__, 'static/js/plugins.js', name="", merge=True, prio=4,),
    #js_from_pkg_stream(__name__, 'static/js/script.js', name="", merge=False, prio=5,),
]

CSS = [
    css_from_pkg_stream(__name__, 'static/css/screen.css', merge=True, prio=1, auto_reload=True),
    css_from_pkg_stream(__name__, 'static/css/handheld.css', media="handheld", merge=True, prio=10, auto_reload=True),

    #css_from_pkg_stream(__name__, 'static/css/ie.css', merge=True, prio=11, auto_reload=True),
]

# TODO: Use URL object
DOMAIN = "http://localhost:9991"

import quantumlounge.http.usermanager
MODULES = [
    quantumlounge.http.usermanager
]

for module in MODULES:
    if hasattr(module,"setup_js"):
        JS = JS + module.setup_js()
    if hasattr(module,"setup_css"):
        CSS = CSS + module.setup_css()

def setup(**kw):
    """initialize the setup"""
    settings = AttributeMapper()
    settings['staticapp'] = get_static_urlparser(pkg_resources.resource_filename(__name__, 'static'))
    tmpls = settings['templates'] = TemplateHandler(__name__)
    
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
    pm.um_poco_endpoint = DOMAIN+"/api/1/users/u/@me/profile"
    settings['pm'] = pm
    
    settings['log'] = logbook.Logger("quantumlounge")

    # TODO: enable updating of sub settings via dot notation (pm.client_id)
    settings.update(kw)
    return settings






