#!/usr/bin/env python
# _*_coding:utf-8_*_
'''
 * Created on 2017/3/2 22:56.
 * @author: Chinge_Yang.
'''

import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from core import main

if __name__ == '__main__':
    main.run()