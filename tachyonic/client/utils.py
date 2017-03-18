from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys


def if_unicode_to_utf8(string):
    if sys.version_info[0] == 2:
        if isinstance(string, unicode):
            return string.encode('utf-8')
        else:
            return string
    else:
        if isinstance(string, str):
            return string.encode('utf-8')
        else:
            return string


def is_byte_string(string):
    if sys.version_info[0] == 2:
        if isinstance(string, str):
            return True
        else:
            return False
    else:
        if isinstance(string, bytes):
            return True
        else:
            return False
