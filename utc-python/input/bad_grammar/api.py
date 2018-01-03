# Copyright (c) 2012-2016 by FEI Company
# All rights reserved. This file includes confidential and proprietary
# information of FEI Company.
import os
import logging

logger = logging.getLogger(__name__)
logger.debug("FEI Calgetter wrappers.")

from comtraits.wrap import build_module  # noqa

skiplist = []

build_module(r'C:\titan\options\calgetter.exe')


from comtraits.gen.CalGetter import *  # noga