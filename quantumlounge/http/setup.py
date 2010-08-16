import sys
import os
import pkg_resources

from quantumcore.storages import AttributeMapper
from quantumcore.resources import CSSResourceManager, css_from_pkg_stream
from quantumcore.resources import JSResourceManager, js_from_pkg_stream, jst_from_pkg_stream

from paste.urlparser import StaticURLParser

def get_static_urlparser(filepath, cache_max_age = 3600):
    return StaticURLParser(os.path.split(filepath)[0], cache_max_age=cache_max_age)


import jinja2

class TemplateHandler(object):
    """a class for caching templates"""

    def __init__(self):
        self._cache = {}

    def get_template(self, filename):
        """retrieve templates and store them inside our PageTemplate cache"""
        if self._cache.has_key(filename):
            return self._cache[filename]
        data = pkg_resources.resource_string(__name__, filename)
        t = self._cache[filename] = jinja2.Template(data)
        return t

    __getitem__ = get_template



JS = [
    js_from_pkg_stream(__name__, 'static/js/plugins.js', name="", merge=False, prio=4,),
    js_from_pkg_stream(__name__, 'static/js/script.js', name="", merge=False, prio=4,),
]

CSS = [
    #css_from_pkg_stream(__name__, 'static/css/screen.css', merge=True, prio=10, auto_reload=True),
    #css_from_pkg_stream(__name__, 'static/css/ie.css', merge=True, prio=11, auto_reload=True),
]



def setup(**kw):
    """initialize the setup"""
    settings = AttributeMapper()
    settings['staticapp'] = get_static_urlparser(pkg_resources.resource_filename(__name__, 'static'))
    tmpls = settings['templates'] = TemplateHandler()
    #settings['master_template'] = tmpls['templates/master.pt'].macros['master']
    settings.update(kw)
    return settings





