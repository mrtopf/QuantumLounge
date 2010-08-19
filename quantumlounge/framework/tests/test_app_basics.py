from quantumlounge.framework.app import Application
from quantumlounge.framework.handler import Handler
import werkzeug

class TestHandler1(Handler):
    def get(self):
        return werkzeug.Response("test1")

class TestHandler2(Handler):
    def get(self):
        return werkzeug.Response("test2")

class TestHandler3(Handler):
    def get(self, id=''):
        return werkzeug.Response(str(id))
    
class SubApp(Application):
    """a sub application mounted to /subapp in App1"""
    handlers = (
        ("/", TestHandler1),
        ("/foobar", TestHandler2),
    )

class SubApp2(SubApp):
    """another one"""    

class App1(Application):
    
    sub_apps = {
        '/subapp' : SubApp,
        '/subapp/another' : SubApp2}
    
    handlers = (
        ("/", TestHandler1),
        ("/huhu", TestHandler2),
        ("/post/{id}", TestHandler3),
        
    )

def test_app_basics():

    app = App1({'foo':'bar'}) # simple settings dict
    c = werkzeug.Client(app, werkzeug.BaseResponse)

    resp = c.get('/')
    assert resp.status=="200 OK"
    assert resp.data == "test1"
    
    resp = c.get('/huhu')
    assert resp.status=="200 OK"
    assert resp.data == "test2"

    
def test_app_wrong_method():    

    app = App1({'foo':'bar'}) # simple settings dict
    c = werkzeug.Client(app, werkzeug.BaseResponse)

    resp = c.post('/')
    assert resp.status=="405 METHOD NOT ALLOWED"
    
def test_app_unkown_path():

    app = App1({'foo':'bar'}) # simple settings dict
    c = werkzeug.Client(app, werkzeug.BaseResponse)

    resp = c.post('/no')
    assert resp.status=="404 NOT FOUND"
    
def test_subhandler():

    app = App1({'foo':'bar'}) # simple settings dict
    c = werkzeug.Client(app, werkzeug.BaseResponse)

    resp = c.get('/subapp')
    assert resp.status=="200 OK"
    
def test_pathed_subhandler():

    app = App1({'foo':'bar'}) # simple settings dict
    c = werkzeug.Client(app, werkzeug.BaseResponse)

    resp = c.get('/subapp/another')
    assert resp.status=="200 OK"

def test_pathed_subhandler_with_path():

    app = App1({'foo':'bar'}) # simple settings dict
    c = werkzeug.Client(app, werkzeug.BaseResponse)

    resp = c.get('/subapp/another/foobar')
    assert resp.status=="200 OK"

def test_path_params():

    app = App1({'foo':'bar'}) # simple settings dict
    c = werkzeug.Client(app, werkzeug.BaseResponse)

    resp = c.get('/post/33')
    assert resp.status=="200 OK"
    assert resp.data == "33"

        