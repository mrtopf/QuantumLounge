from quantumcore.storages import AttributeMapper


class User(AttributeMapper):
    """a user"""
    
    def get_poco(self):
        """return the user as a Portable Contact instance"""
        return {
          "id": self.username,
          "thumbnailUrl": self.photo,
          "name": {
            "formatted": self.fullname,
          },
          "email" : self.email
        }

class UserManager(object):
    """the user manager manages user profiles and is able to verify user credentials"""
    
    # the users stored for now
    userstore = [
        {'username' : 'mrtopf',
         'password' : 'foobar',
         'fullname' : 'Christian Scholz',
         'photo'    : 'http://mrtopf.de/profile.png',
         'email'    : 'mrtopf@gmail.com'}
    ]
    
    
    def get(self, username):
        """return a user based on it`s ``username``. This returns an instance of 
        ``User``. In case it's not found it returns None"""
        for u in self.userstore:
            if u['username']==username:
                return User(u)
        return None
    
    __getitem__ = get
        