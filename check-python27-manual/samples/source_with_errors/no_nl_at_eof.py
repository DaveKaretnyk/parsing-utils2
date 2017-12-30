import os
import logging

logger = logging.getLogger(__name__)
logger.debug("blah wrappers")

from comtraits.wrap import build_module  # noqa

skiplist = []

build_module(r'C:\some\dir\blah.exe')


from comtraits.gen.blah import *  # noga