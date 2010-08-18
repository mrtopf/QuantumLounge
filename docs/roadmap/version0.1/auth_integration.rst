=========================
Authorization Integration
=========================


Requirements:

- We want some decorator or handler which checks an access token for API endpoints
- e.g. the poco endpoint in the UM wants to know if that user is actually allowed to 
  access it. 
- The same applies to API calls to the PM from JS because we need to make sure it is the
  correct user
- we can here check a local cookie as it's made from the same domain
- if JS from the PM wants to call poco on the UM, then there is another thing
- This JS can also do the redirect flow to obtain it's own access token from the UM
- Now it has an access token which is bound to the user
- if just calling "/poco" with it, it can return the right user
- an access token is more or less a session
- a session can have data attached, like the username
- a handler could obtain the session data for an access token.

Implement an OAuth handler
==========================

- This handler needs access to the Authorization Manager of the user manager.
- This manager is stored in the settings of the app.
- it can be accessed via ``self.app.settings.authorization_manager``
- it can lookup an access token and it's associated data
- it can store this data an self.auth_session as a dict or AttributeMapper

Then the handler methods can check that session to see if e.g. the user matches the one
requested.






