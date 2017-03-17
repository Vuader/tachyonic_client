# -*- coding: utf-8 -*-
"""Tachyonic Clients"""

from exceptions import *
from restclient import RestClient
from client import Client

from tachyonic.clients import metadata

__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright
