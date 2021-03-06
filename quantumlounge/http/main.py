from quantumlounge.framework import Handler, Application
from quantumlounge.framework.decorators import html

import setup
import usermanager
import api
import pm

class MainHandler(Handler):
    """serve some index document"""

    author = u"Christian Scholz <mrtopf@gmail.com>"
    title = "quantumLOUNGE"
    
    @html
    def get(self):
        print self.context.keys()
        return self.app.settings.templates['templates/master.pt'].render(
            pc = self.context
            )

class StaticHandler(Handler):
    def get(self, path_info):
        return self.settings.staticapp

class CSSResourceHandler(Handler):
    def get(self, path_info):
        return self.settings['css_resources'].render_wsgi
        
class JSResourceHandler(Handler):
    def get(self, path_info):
        return self.settings['js_resources'].render_wsgi


class App(Application):

    def setup_handlers(self, map):
        """setup the mapper"""
        with map.submapper(path_prefix=self.settings.virtual_path) as m:
            print self.settings.virtual_path 
            m.connect(None, "", handler=MainHandler)
            m.connect(None, "/", handler=MainHandler)
            m.connect(None, "/js2/{path_info:.*}", handler=StaticHandler)
            m.connect(None, "/css/{path_info:.*}", handler=CSSResourceHandler)
            m.connect(None, "/js/{path_info:.*}", handler=JSResourceHandler)
            m.connect(None, "/img/{path_info:.*}", handler=StaticHandler)
            m.connect(None, "/jst/{path_info:.*}", handler=StaticHandler)

            api.setup_handlers(m)
            usermanager.setup_handlers(m)
            pm.setup_handlers(m)
    
def main():
    port = 9991
    app = App(setup.setup())
    return webserver(app, port)

def app_factory(global_config, **local_conf):
    settings = setup.setup(**local_conf)
    return App(settings)

def webserver(app, port):
    import wsgiref.simple_server
    wsgiref.simple_server.make_server('', port, app).serve_forever()

if __name__=="__main__":
    main()

