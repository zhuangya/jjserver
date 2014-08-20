#! /usr/bin/env python
# -*- coding: utf-8 -*-

import string
import random

def gen_vcode():
    """
    """
    return ''.join(random.choice(string.digits) for x in range(6))
