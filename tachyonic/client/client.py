from __future__ import absolute_import
from __future__ import unicode_literals

import logging
import thread
import json

try:
    # python 3
    from io import BytesIO
except ImportError:
    # python 2
    from StringIO import StringIO as BytesIO
try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode

from tachyonic.neutrino.restclient import RestClient as NfwRestClient
from tachyonic.neutrino import model as nfw_model
from tachyonic.neutrino import request as nfw_request
from tachyonic.neutrino import constants as const

from tachyonic.common import exceptions

log = logging.getLogger(__name__)

sessions = {}

class Client(NfwRestClient):
    def __init__(self, url, token=None):
        global sessions

        self.thread_id = thread.get_ident()
        if self.thread_id not in sessions:
            sessions[self.thread_id] = {}
        self.session = sessions[self.thread_id]

        self.url = url

        if url in self.session:
            self.tachyonic_headers = self.session[url]['headers']
            super(Client, self).__init__()
        else:
            self.session[url] = {}
            self.session[url]['headers'] = {}
            super(Client, self).__init__()
            self.tachyonic_headers = self.session[url]['headers']

    def authenticate(self, username, password, domain):
        url = self.url
        auth_url = "%s/token" % (url,)

        if 'X-Tenant' in self.tachyonic_headers:
            del self.tachyonic_headers['X-Tenant']
        if 'X-Auth-Token' in self.tachyonic_headers:
            del self.tachyonic_headers['X-Auth-Token']
        self.tachyonic_headers['X-Domain'] = domain

        data = {}
        data['username'] = username
        data['password'] = password
        data['expire'] = 1

        server_headers, result = self.execute("POST", auth_url,
                                              data, self.tachyonic_headers)

        if 'token' in result:
            self.token = result['token']
            self.tachyonic_headers['X-Auth-Token'] = self.token
        #else:
        #    raise tachyonic.common.exceptions.Authentication("Could not connect/authenticate")

        self.session[url]['headers'] = self.tachyonic_headers

        return result

    def token(self, token, domain, tenant):
        url = self.url
        auth_url = "%s/token" % (url,)

        if tenant is not None:
            self.tachyonic_headers['X-Tenant'] = tenant
        self.tachyonic_headers['X-Domain'] = domain
        self.tachyonic_headers['X-Auth-Token'] = token

        server_headers, result = self.execute("GET", auth_url,
                                              None)

        if 'token' in result:
            self.token = token
        else:
            if 'X-Tenant' in self.tachyonic_headers:
                del self.tachyonic_headers['X-Tenant']
            if 'X-Domain' in self.tachyonic_headers:
                del self.tachyonic_headers['X-Domain']
            if 'X-Auth-Token' in self.tachyonic_headers:
                del self.tachyonic_headers['X-Auth-Token']
            #raise tachyonic.common.exceptions.Authentication("Could not connect/authenticate")

        self.session[url]['headers'] = self.tachyonic_headers

        return result

    def domain(self, domain):
        self.tachyonic_headers['X-Domain'] = domain

    def tenant(self, tenant):
        if tenant is None:
            del self.tachyonic_headers['X-Tenant']
        else:
            self.tachyonic_headers['X-Tenant'] = tenant

    def execute(self, request, url, obj=None, headers=None):
        if obj is not None:
            if isinstance(obj, nfw_model.ModelDict):
                m = {}
                for field in obj._declared_fields:
                    if field in obj._data:
                        m[field] = obj._data[field]._data
                data = json.dumps(m)
            elif isinstance(obj, nfw_request.Post):
                for field in obj:
                    m[field] = obj[field].value
                data = json.dumps(m)
            else:
                data = json.dumps(obj)
        else:
            data = None

        if self.url not in url:
            url = "%s/%s" % (self.url, url)
        if headers is None:
            headers = self.tachyonic_headers
        else:
            headers.update(self.tachyonic_headers)

        status, server_headers, response = super(Client, self).execute(request, url, data, headers)
        if status != 200:
            if 'content-type' in server_headers:
                if 'json' in server_headers['content-type']:
                    if response is not None:
                        response = json.loads(response)
                        if 'error' in response:
                            response = response['error']
                            f = "HTTP_%s" % (str(status),)
                            if hasattr(const, f):
                                http_status = getattr(const, f)
                            else:
                                http_status = const.neutrino.HTTP_500

                            title = "RESTAPI: %s" % (response['title'],)
                            raise exceptions.ClientError(title,
                                                         response['description'],
                                                         http_status)

        if response is not None:
            try:
                response = json.loads(response)
            except Exception as e:
                raise exceptions.ClientError('RESTAPI JSON Decode',
                                              e,
                                              const.HTTP_500)
        return [server_headers, response]
