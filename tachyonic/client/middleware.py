from __future__ import absolute_import
from __future__ import unicode_literals

import logging

from tachyonic import app
from tachyonic.client import Client

log = logging.getLogger(__name__)


class Token(object):
    def __init__(self, interface='ui'):
        self.interface = interface

    def pre(self, req, resp):
        resp.headers['content-type'] = 'application/json; charset=UTF-8'.encode('utf-8')
        req.context['token'] = None
        req.context['email'] = None
        req.context['username'] = None
        req.context['login'] = False
        req.context['domain_admin'] = False
        req.context['domain_id'] = None
        req.context['domain'] = None
        req.context['domains'] = []
        req.context['tenant_id'] = None
        req.context['tenant'] = None
        req.context['expire'] = None
        req.context['roles'] = []

        if 'token' in req.session:
            token = req.session.get('token')
        else:
            token = req.headers.get('X-Auth-Token')

        req.context['restapi'] = app.config.get("tachyon").get("restapi","http://127.0.0.1")
        if token is not None:
            api = Client(req.context['restapi'])
            # Get Domain
            if self.interface == 'ui' and req.post.get('domain', None) is not None:
                domain = req.post.get('X-domain', 'default')
            elif self.interface == 'ui' and 'domain' in req.session:
                domain = req.session.get('domain', 'default')
            else:
                domain = req.headers.get('X-Domain', 'default')

            # Get Tenant
            if self.interface == 'ui' and req.post.get('tenant', None) is not None:
                tenant = req.post.get('tenant', None)
            elif self.interface == 'ui' and 'tenant' in req.session:
                tenant = req.session.get('tenant')[0]
            else:
                tenant = req.headers.get('X-Tenant')

            # Validate against API and get details...
            auth = api.token(token, domain, tenant)

            req.context['token'] = auth['token']
            req.context['email'] = auth['email']
            req.context['username'] = auth['username']
            req.context['login'] = True
            req.context['domains'] = []
            req.context['expire'] = auth['expire']
            req.context['roles'] = []
            for r in auth['roles']:
                if r['domain_name'] not in req.context['domains']:
                    req.context['domains'].append(r['domain_name'])

                req.context['roles'].append(r['role_name'])
                if r['domain_name'] == domain or r['domain_id'] == domain:
                    if r['tenant_id'] is None:
                        req.context['domain_admin'] = True

                    req.context['domain_id'] = r['domain_id']
                    req.context['domain'] = r['domain_name']

                if r['tenant_name'] == tenant or r['tenant_id'] == tenant:
                    req.context['tenant_id'] = r['tenant_id']
                    req.context['tenant'] = r['tenant_name']

        if hasattr(self, 'init'):
            self.init(req, resp)
