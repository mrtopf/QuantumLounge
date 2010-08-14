from quantumlounge.usermanager.users import UserManager

um = UserManager()

def test_retrieve_existing_user():
    u = um.get('mrtopf')
    assert u is not None
    
def test_retrieve_nonexisting_user():
    u = um.get('nobody')
    assert u is None
    
def test_retrieve_via_getitem():
    u = um['mrtopf']
    assert u is not None

def test_user_attribs():
    u = um.get('mrtopf')
    assert u.username=="mrtopf"
    assert u.email=="mrtopf@gmail.com"
    assert u.fullname=="Christian Scholz"
    assert u.password=="foobar"

def test_poco():
    u = um.get('mrtopf')
    poco = u.get_poco()
    assert poco['id']=="mrtopf"
    assert poco['email']=="mrtopf@gmail.com"
    assert poco['name']['formatted']=="Christian Scholz"
    