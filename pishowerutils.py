#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

# set up logging to file
logging.basicConfig(level=logging.DEBUG,
                    datefmt='%d.%m. %H:%M:%S',
                    format='%(asctime)s %(levelname)-8s %(message)s')

logger = logging.getLogger()

