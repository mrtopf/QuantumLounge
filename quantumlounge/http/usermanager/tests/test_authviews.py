import simplejson

def test_authorize_loop(um_client):
    """functional test for testing the whole authorize loop"""
    r = um_client.get("/users/authorize", 
        query_string={'client_id': 'pm', 
              'redirect_uri' : 'something',
              'response_type' : 'code'})
    
    assert r.status=="200 OK"
    assert len(r.data)>1000 # TODO: use better checking for success as everything is 200 OK
    
    # the login form should be showing now, let's emulate the login
    r = um_client.post("/users/authorize/login",
        data={'username': 'mrtopf', 'password' : 'foobar'})
    assert r.status=="200 OK"
    json = simplejson.loads(r.data)
    assert not json.has_key("error")

    # we are logged in and should have a cookie    
    assert r.headers.has_key("Set-Cookie")
    assert r.headers['Set-Cookie'].startswith("l=")

    # now we can try to obtain the auth code
    r = um_client.get("/users/authorize/authcode",
        query_string={'client_id': 'pm'})
    assert r.status=="200 OK"
    json = simplejson.loads(r.data)
    assert not json.has_key("error")
    assert json.has_key("code")
    
    
    # now we exchange the code with an access token
    r = um_client.get("/api/1/users/token",
        query_string={'client_id': 'pm',
                      'redirect_uri' : 'something',
                      'code' : json['code'],
                      'grant_type' : 'authorization_code'})
    assert r.status=="200 OK"
    json = simplejson.loads(r.data)
    token = json["access_token"]
    
    # now we try to retrieve the PoCo data for @me
    r = um_client.get("/api/1/users/u/@me/profile",
        query_string={'access_token' : token})
        
    assert r.status=="200 OK"
    poco = simplejson.loads(r.data)
    assert poco['id'] == "mrtopf"
    
def test_login_wrong_pw(um_client):
    r = um_client.post("/users/authorize/login",
        data={'username': 'mrtopf', 'password' : 'nothing'})
    assert r.status=="200 OK"
    json = simplejson.loads(r.data)
    assert json.has_key("error")
    assert json['error']=="credentials_wrong"
    
def test_login_wrong_user(um_client):
    r = um_client.post("/users/authorize/login",
        data={'username': 'notopf', 'password' : 'nothing'})
    assert r.status=="200 OK"
    json = simplejson.loads(r.data)
    assert json.has_key("error")
    assert json['error']=="user_not_found"

def test_login_missing_params(um_client):
    r = um_client.post("/users/authorize/login",
        data={})
    assert r.status=="200 OK"
    json = simplejson.loads(r.data)
    assert json.has_key("error")
    assert json['error']=="bad_request"

def test_authcode_not_logged_in(um_client):
    r = um_client.get("/users/authorize/authcode",
        query_string={'client_id': 'pm'})
    assert r.status=="200 OK"
    json = simplejson.loads(r.data)
    assert json.has_key("error")
    assert json['error']=="user_not_logged_in"

def test_authcode_wrong_client_id(um_client):
    um_client.post("/users/authorize/login",
        data={'username': 'mrtopf', 'password' : 'foobar'})
    r = um_client.get("/users/authorize/authcode",
        query_string={'client_id': 'pm2'})
    assert r.status=="200 OK"
    json = simplejson.loads(r.data)
    assert json.has_key("error")
    assert json['error']=="unauthorized_client"



