
from tachyonic.client import Client
# PLUGIN IS REGISTERED BY API if installed on box... or perhaps a client module
# for the API. Config found in setup.py for example for Users is registered by
# tachyonic.api... 
from tachyonic.client.plugins import Users
from tachyonic.client import constants as const
from tachyonic.client import exceptions

api = Client('http://dev/api')
try:
    print "Authenticating with user pass"
    auth = api.authenticate('root', 'password', 'default')
    print auth
    print ""
    print "Authenticaed with Token"
    print api.token(auth['token'], 'default', None)
    print ""
except exceptions.ClientError as e:
    print e

# SESSION KEPT GLOBALLY - NO NEED TO AUTH AGAIN FOR THREAD
print "Getting Data for Token again with no auth - using globally stored session for thread"
api = Client('http://dev/api')
headers, response = api.execute(const.HTTP_GET,'/v1/token')
print response
api = Users('http://dev/api')
api.execute(const.HTTP_GET, '/blah/blah/get/me/this/network', endpoint='netrino')
print api.list_users()
print api._endpoints


