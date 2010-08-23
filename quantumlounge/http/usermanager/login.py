from quantumlounge.framework import Handler
from quantumlounge.framework.decorators import html
import werkzeug
from werkzeug.contrib.securecookie import SecureCookie

import quantumlounge.usermanager as usermanager

class Login(Handler):
    """logs the user in or shows the login form.
    
    If a GET is performed, then the form is rendered, if a POST is performed
    than credentials are checked and a cookie is set if they are correct. On POST you
    can also specify the output type, e.g. if it's JSON or a redirect on success.
    
    For this you need to set the attribute ``success_method`` to either ``json`` or 
    ``redirect``. In the latter case you also need to include a ``redirect_uri`` in the
    data. The default is ``json``. TODO: make some HTML default page the default
    
    If a ``came_from`` parameter is passed to the login form on GET then a ``redirect``
    method will be used on POST meaning that the described parameters will be passed in 
    the form as hidden values.
    
    """

    @html
    def error(self, msg):
        return msg
        
    def post(self):
        """check login form data and log the user in. """
        f = self.request.form
        username = f.get("username", None)
        password = f.get("password", None)
        success_method = f.get("success_method",u"json")
        if username is None or password is None:
            return werkzeug.exceptions.BadRequest(description=u"username or password missing")
        
        username = 

    def get(self):
        # TODO: implement login form
        raise NotImplemented
        return werkzeug.exceptions.MethodNotAllowed("not implemented yet!")
        
