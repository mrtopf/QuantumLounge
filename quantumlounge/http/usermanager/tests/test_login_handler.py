import simplejson

def test_login(um_client):
    r = um_client.post("/api/1/users/login", data={'username': 'mrtopf', 'password' : 'foobar'})
    assert r.headers['Content-Type'] == "application/json"
    assert r.status == "200 OK"
    d = simplejson.loads(r.data)
    assert d['username'] == "mrtopf"

def test_login_with_wrong_pw(um_client):
    r = um_client.post("/api/1/users/login", data={'username': 'mrtopf', 'password' : 'foobar2'})
    assert r.status == "401 UNAUTHORIZED"

def test_login_with_wrong_user(um_client):
    r = um_client.post("/api/1/users/login", data={'username': 'mrtopf222', 'password' : 'foobar'})
    assert r.status == "404 NOT FOUND"

def test_login_with_missing_parameters(um_client):
    r = um_client.post("/api/1/users/login", data={})
    assert r.status == "400 BAD REQUEST"
    r = um_client.post("/api/1/users/login", data={'username' : 'mrtopf'})
    assert r.status == "400 BAD REQUEST"
    r = um_client.post("/api/1/users/login", data={'password' : 'nopw'})
    assert r.status == "400 BAD REQUEST"
    
    

