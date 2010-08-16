"""
some useful decorators
"""

import werkzeug
import functools
import simplejson

def json(method):
    """takes a dict output of a handler method and returns it as JSON"""
    
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        data = method(*args, **kwargs)
        response = werkzeug.Response(simplejson.dumps(data))
        response.content_type = "application/json"
        return response

    return wrapper
        