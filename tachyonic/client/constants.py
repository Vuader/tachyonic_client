from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys


class _Constant(object):
    class ConstError(TypeError):
        pass

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise self.ConstError("Can't rebind constant(%s)" % key)
        self.__dict__[key] = value

_const = _Constant()

_const.HTTP_GET = 'GET'
_const.HTTP_POST = 'POST'
_const.HTTP_PUT = 'PUT'
_const.HTTP_DELETE = 'DELETE'
_const.HTTP_PATCH = 'PATCH'
_const.HTTP_OPTIONS = 'OPTIONS'
_const.HTTP_HEAD = 'HEAD'
_const.HTTP_TRACE = 'TRACE'
_const.HTTP_CONNECT = 'CONNECT'

_const.HTTP_100 = '100 Continue'.encode('utf-8')
_const.HTTP_101 = '101 Switching Protocols'.encode('utf-8')
_const.HTTP_200 = '200 OK'.encode('utf-8')
_const.HTTP_201 = '201 Created'.encode('utf-8')
_const.HTTP_202 = '202 Accepted'.encode('utf-8')
_const.HTTP_203 = '203 Non-Authoritative Information'.encode('utf-8')
_const.HTTP_204 = '204 No Content'.encode('utf-8')
_const.HTTP_205 = '205 Reset Content'.encode('utf-8')
_const.HTTP_206 = '206 Partial Content'.encode('utf-8')
_const.HTTP_226 = '226 IM Used'.encode('utf-8')
_const.HTTP_300 = '300 Multiple Choices'.encode('utf-8')
_const.HTTP_301 = '301 Moved Permanently'.encode('utf-8')
_const.HTTP_302 = '302 Found'.encode('utf-8')
_const.HTTP_303 = '303 See Other'.encode('utf-8')
_const.HTTP_304 = '304 Not Modified'.encode('utf-8')
_const.HTTP_305 = '305 Use Proxy'.encode('utf-8')
_const.HTTP_306 = '306 Switch Proxy'.encode('utf-8')
_const.HTTP_307 = '307 Temporary Redirect'.encode('utf-8')
_const.HTTP_308 = '308 Permanent Redirect'.encode('utf-8')
_const.HTTP_400 = '400 Bad Request'.encode('utf-8')
_const.HTTP_401 = '401 Unauthorized'.encode('utf-8')  # <-- Really means "unauthenticated"
_const.HTTP_402 = '402 Payment Required'.encode('utf-8')
_const.HTTP_403 = '403 Forbidden'.encode('utf-8')  # <-- Really means "unauthorized"
_const.HTTP_404 = '404 Not Found'.encode('utf-8')
_const.HTTP_405 = '405 Method Not Allowed'.encode('utf-8')
_const.HTTP_406 = '406 Not Acceptable'.encode('utf-8')
_const.HTTP_407 = '407 Proxy Authentication Required'.encode('utf-8')
_const.HTTP_408 = '408 Request Time-out'.encode('utf-8')
_const.HTTP_409 = '409 Conflict'.encode('utf-8')
_const.HTTP_410 = '410 Gone'.encode('utf-8')
_const.HTTP_411 = '411 Length Required'.encode('utf-8')
_const.HTTP_412 = '412 Precondition Failed'.encode('utf-8')
_const.HTTP_413 = '413 Payload Too Large'.encode('utf-8')
_const.HTTP_414 = '414 URI Too Long'.encode('utf-8')
_const.HTTP_415 = '415 Unsupported Media Type'.encode('utf-8')
_const.HTTP_416 = '416 Range Not Satisfiable'.encode('utf-8')
_const.HTTP_417 = '417 Expectation Failed'.encode('utf-8')
_const.HTTP_418 = "418 I'm a teapot".encode('utf-8')
_const.HTTP_422 = "422 Unprocessable Entity".encode('utf-8')
_const.HTTP_426 = '426 Upgrade Required'.encode('utf-8')
_const.HTTP_428 = '428 Precondition Required'.encode('utf-8')
_const.HTTP_429 = '429 Too Many Requests'.encode('utf-8')
_const.HTTP_431 = '431 Request Header Fields Too Large'.encode('utf-8')
_const.HTTP_451 = '451 Unavailable For Legal Reasons'.encode('utf-8')
_const.HTTP_500 = '500 Internal Server Error'.encode('utf-8')
_const.HTTP_501 = '501 Not Implemented'.encode('utf-8')
_const.HTTP_502 = '502 Bad Gateway'.encode('utf-8')
_const.HTTP_503 = '503 Service Unavailable'.encode('utf-8')
_const.HTTP_504 = '504 Gateway Time-out'.encode('utf-8')
_const.HTTP_505 = '505 HTTP Version not supported'.encode('utf-8')
_const.HTTP_511 = '511 Network Authentication Required'.encode('utf-8')

sys.modules[__name__] = _const
