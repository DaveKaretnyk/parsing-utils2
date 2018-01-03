# Copyright (c) 2012-2013 by FEI Company
# All rights reserved. This file includes confidential and proprietary
# information of FEI Company.
import logging

logger = logging.getLogger(__name__)
logger.debug("PAASERVER wrappers.")

from comtraits.wrap import build_module

skiplist = []
build_module('c:\paaserver\paaserver.exe', skiplist=skiplist)

from comtraits.gen.PAAServerLib import *  # noqa