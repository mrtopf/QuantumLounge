from quantumlounge.http.usermanager.usermanager import UserManager
from quantumlounge.http.setup import setup
import werkzeug


def pytest_funcarg__um_client(request):
    """return a client object for testing"""
    um = UserManager(setup())    
    return werkzeug.Client(um, werkzeug.BaseResponse)
    
    