#!python
# coding: utf-8

import importlib.metadata

__author__ = "Demetri Patrinos, https://github.com/dpatrinos"
__version__ = importlib.metadata.version("primerdesigner")

from .primerdesigner import fromCoordinates
from .primerdesigner import fromSJDataset