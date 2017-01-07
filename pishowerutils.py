#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" PiShower project
    @copyright  Christian Daehn (c) 2006, http://3dh.de
    @license    MIT license
"""


import logging

# set up logging to file
logging.basicConfig(level=logging.DEBUG,
                    datefmt='%d.%m. %H:%M:%S',
                    format='%(asctime)s %(levelname)-8s %(message)s')

logger = logging.getLogger()

