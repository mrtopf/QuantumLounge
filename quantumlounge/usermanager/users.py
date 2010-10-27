from quantumcore.storages import AttributeMapper
from quantumlounge.content import Model, Collection


class User(Model):
    """a user"""
    TYPE = "user"
    _attribs = ['username','photo','fullname','email','password']
    
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

    def jsonify(self, data):
        """convert the dictionary to a JSON representation"""
        data['_id'] = unicode(data['_id'])
        del data['password'] # only updatable with the right permissions
        return data

class UserManager(Collection):
    """the user manager manages user profiles and is able to verify user credentials"""

    data_class = User
    
    def get_by_username(self, username):
        """return a user based on it`s ``username``. This returns an instance of 
        ``User``. In case it's not found it returns None"""
        r = self.find({'username':username})
        if len(r)==0:
            return None
        return r[0]
