from quantumlounge.framework import Handler, Application
import werkzeug
import simplejson

class Login(Handler):
    """handle logging in users. On a POST it will check username and password 
    passed in a form encoded document and return a JSON encoded status document."""
    
    def post(self):
        """we except ``username`` and ``password`` in a form encoded document"""
        
        f = self.request.form
        username = f.get("username", None)
        password = f.get("password", None)
        if username is None or password is None:
            return werkzeug.exceptions.BadRequest(description=u"username or password missing")
        
        print self.app.settings
        um = self.app.settings['usermanager']
        user = um.get(username)
        if user is None:
            return werkzeug.exceptions.NotFound(description=u"user not found")
        if password!=user.password:
            return werkzeug.exceptions.Unauthorized(description=u"password wrong")
            
        data = {
            'status' : 'ok',
            'username' : user.username,
            'poco' : user.get_poco()
        }
        res = werkzeug.Response(simplejson.dumps(data))
        res.content_type = "application/json"
        return res


class UserManager(Application):
    
    handlers = (
        ('/login', Login),
    )