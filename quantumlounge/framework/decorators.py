"""
some useful decorators
"""

import werkzeug
import functools
import simplejson

def html(method):
    """takes a string output of a view and wraps it into a text/html response"""
    
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        response = werkzeug.Response(method(*args, **kwargs))
        response.content_type = "text/html"
        return response

    return wrapper
        

def json(method):
    """takes a dict output of a handler method and returns it as JSON"""
    
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        data = method(*args, **kwargs)
        response = werkzeug.Response(simplejson.dumps(data))
        response.content_type = "application/json"
        return response

    return wrapper
        