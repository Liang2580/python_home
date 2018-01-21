#!/usr/bin/env python
# _*_coding:utf-8_*_
'''
 * Created on 2017/3/6 21:58.
 * @author: Chinge_Yang.
'''

import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ACCOUNT_DATABASE = {
    'engine': 'file_storage',
    'name': 'accounts',
    'path': "%s/db" % BASE_DIR
}

BASE_DATABASE = {
    'engine': 'file_storage',
    'name': 'base',
    'path': "%s/db" % BASE_DIR
}

LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'system': 'system.log',
}

AUTHORITY = {
    'student': 1,
    'teacher': 2,
    'admin': 8
}

STATUS = {
    'normal': 1,
    'locked': 2
}