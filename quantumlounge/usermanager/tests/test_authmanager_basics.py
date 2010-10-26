import py.test

from quantumlounge.usermanager.authorization import AuthorizationManager
import quantumlounge.usermanager.errors as errors

am = AuthorizationManager()

def test_create_new_token():
    t = am.new_token('mrtopf', 'pm')
    assert t is not None
    assert len(t) == 2

def test_get_token_with_unkown_client_id():
    py.test.raises(errors.ClientNotFound, lambda: am.new_token('mrtopf', 'nopm'))
    
def test_get_token_for_auth_code():
    token, auth_code = am.new_token('mrtopf', 'pm')
    real_token = am.get_token_for_code(auth_code, 'pm')
    assert real_token._id == token
    
def test_get_token_for_auth_code_with_wrong_code():
    token, auth_code = am.new_token('mrtopf', 'pm')
    py.test.raises(errors.AuthorizationCodeNotFound, lambda: am.get_token_for_code("foobar",'pm'))

def test_get_token_for_auth_code_with_wrong_client_id():
    token, auth_code = am.new_token('mrtopf', 'pm')
    py.test.raises(errors.InvalidAuthorizationCode, lambda: am.get_token_for_code(auth_code,'pm2'))

def test_get_token():
    at, auth_code = am.new_token('mrtopf', 'pm')
    token = am.get_token(at)
    assert token.username == 'mrtopf'
    
def test_get_unkown_token_default():
    at, auth_code = am.new_token('mrtopf', 'pm')
    token = am.get_token('foobar',"bar")
    assert token == "bar"
    

    
