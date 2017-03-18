# -*- coding: utf-8 -*-
"""Tachyonic Clients"""

from . import metadata
from . import plugins

__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright

from .restclient import RestClient
from .client import Client

from pkg_resources import iter_entry_points
for entry_point in iter_entry_points(group='tachyonic.client.plugins', name=None):
    setattr(plugins, entry_point.name, entry_point.load())

