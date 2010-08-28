from quantumlounge.http.main import App
from quantumlounge.http.setup import setup
import werkzeug

def pytest_funcarg__um_client(request):
    """return a client object for testing"""
    um = App(setup())    
    return werkzeug.Client(um, werkzeug.BaseResponse, use_cookies=True)
    
    
