from quantumlounge.framework import Handler, Application
from quantumlounge.framework.decorators import html

import setup
from usermanager import UserManager

class MainHandler(Handler):
    """serve some index document"""

    author = u"Christian Scholz <mrtopf@gmail.com>"
    title = "quantumLOUNGE"
    
    @html
    def get(self):
        return self.app.settings.templates['templates/master.pt'].render(handler = self)


class App(Application):
    
    sub_apps = {
        'users' : UserManager,
    }

    handlers = (
        ('/',   MainHandler),
    )

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

