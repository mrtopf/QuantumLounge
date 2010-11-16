import sys
import os
import pkg_resources
import pymongo
import logbook

from quantumcore.storages import AttributeMapper
from quantumcore.resources import CSSResourceManager, css_from_pkg_stream
from quantumcore.resources import JSResourceManager, js_from_pkg_stream, jst_from_pkg_stream
from quantumlounge.usermanager.users import UserManager
from quantumlounge.usermanager.authorization import AuthorizationManager
from quantumlounge.content.basetypedefs import StatusType
from quantumlounge.content.basetypes import FolderType, LinkType
from quantumlounge.content.poll import PollType
from quantumlounge.content.base import ContentManager
from quantumlounge.content.contenttypes import ContentTypeManager

from quantumlounge.framework.utils import get_static_urlparser, TemplateHandler


JS = [
    js_from_pkg_stream(__name__, 'static/js/jquery-1.4.2.min.js', name="jquery", merge=False, prio=1,),
    js_from_pkg_stream(__name__, 'static/js/modernizr-1.5.min.js', name="head", merge=False, prio=1,),

    js_from_pkg_stream(__name__, 'static/js/jquery.NobleCount.min.js', name="", merge=True, prio=1,),

    js_from_pkg_stream(__name__, 'static/js/jsuri-1.0.2-min.js', name="", merge=True, prio=1,),
    js_from_pkg_stream(__name__, 'static/js/jquery.ui.min.js', name="", merge=True, prio=2,),
    js_from_pkg_stream(__name__, 'static/js/sammy.js', name="", merge=True, prio=2,),
    js_from_pkg_stream(__name__, 'static/js/sammy.mustache.min.js', name="", merge=True, prio=3,),
    js_from_pkg_stream(__name__, 'static/js/sammy.title.min.js', name="", merge=True, prio=3,),
    js_from_pkg_stream(__name__, 'static/js/sammy.json.min.js', name="", merge=True, prio=3,),
    js_from_pkg_stream(__name__, 'static/js/underscore-min.js', name="", merge=True, prio=3,),
    js_from_pkg_stream(__name__, 'static/js/jquery.tools.min.js', name="", merge=True, prio=3,),

    js_from_pkg_stream(__name__, 'static/js/plugins.js', name="", merge=True, prio=4,),
    #js_from_pkg_stream(__name__, 'static/js/jquery-1.4.2.min.js', name="external", merge=True, prio=1, auto_reload=True),
    js_from_pkg_stream(__name__, 'static/js/mustache.js', name="external", merge=True, prio=3, auto_reload=True),
    js_from_pkg_stream(__name__, 'static/js/external.js', name="external", merge=True, prio=4, auto_reload=True),
    #js_from_pkg_stream(__name__, 'static/js/jquery-1.4.2.min.js', name="ext_poll", merge=True, prio=1, auto_reload=True),
    js_from_pkg_stream(__name__, 'static/js/mustache.js', name="ext_poll", merge=True, prio=3, auto_reload=True),
    js_from_pkg_stream(__name__, 'static/js/ext_poll.js', name="ext_poll", merge=True, prio=4, auto_reload=True),
    #js_from_pkg_stream(__name__, 'static/js/script.js', name="", merge=False, prio=5,),
]

CSS = [
    css_from_pkg_stream(__name__, 'static/css/screen.css', merge=True, prio=1, auto_reload=True),
    css_from_pkg_stream(__name__, 'static/css/jquery.ui.css', merge=True, prio=1, auto_reload=True),
    css_from_pkg_stream(__name__, 'static/css/handheld.css', media="handheld", merge=True, prio=10, auto_reload=True),

    #css_from_pkg_stream(__name__, 'static/css/ie.css', merge=True, prio=11, auto_reload=True),
]

# TODO: Use URL object

import quantumlounge.http.usermanager
import quantumlounge.http.pm
import quantumlounge.http.api.users

MODULES = [
    quantumlounge.http.usermanager,
    quantumlounge.http.pm,
    quantumlounge.http.api.users
]

for module in MODULES:
    if hasattr(module,"setup_js"):
        JS = JS + module.setup_js()
    if hasattr(module,"setup_css"):
        CSS = CSS + module.setup_css()

def setup(**kw):
    """initialize the setup"""
    settings = AttributeMapper()
    # wo liegt der User Server?
    settings['userserver'] = "http://localhost:9991"
    settings['staticapp'] = get_static_urlparser(pkg_resources.resource_filename(__name__, 'static'))
    tmpls = settings['templates'] = TemplateHandler(__name__)
    
    
    settings['secret_key'] = "czs7s8c6c8976c89c7s6s8976cs87d6" #os.urandom(20)
    
    
    settings['log'] = logbook.Logger("quantumlounge")

    ## content types
    db = pymongo.Connection().pm
    ctm = ContentTypeManager()
    ctm.add(StatusType(db, "contents"))
    ctm.add(FolderType(db, "contents"))
    ctm.add(LinkType(db, "contents"))
    ctm.add(PollType(db, "contents"))
    settings['content1']=ctm

    settings['usermanager'] = UserManager(db,"users")
    settings['authmanager'] = AuthorizationManager(db, "tokens")
    settings['contentmanager'] = ContentManager(db, "contents", ctm, "0")

    # path
    settings['virtual_path'] = ""

    # TODO: enable updating of sub settings via dot notation (pm.client_id)
    settings.update(kw)

    # settings for the project manager
    userserver = settings.userserver
    pm = AttributeMapper()
    pm.client_id = "pm"
    pm.um_authorize_uri = userserver+"/users/authorize"
    pm.um_token_endpoint = userserver+"/api/1/users/token"
    pm.um_poco_endpoint = userserver+"/api/1/users/u/@me/profile"
    settings['pm'] = pm
    
    # setup CSS and JS according to the vpath
    vpath = settings.virtual_path
    settings['css_resources'] = CSSResourceManager(CSS, prefix_url=vpath+"/css", auto_reload=True)
    settings['js_resources'] = JSResourceManager(JS, prefix_url=vpath+"/js", auto_reload=True)
    return settings






