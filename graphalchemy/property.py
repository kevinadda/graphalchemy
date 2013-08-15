#! /usr/bin/env python
# -*- coding: utf-8 -*-

# ==============================================================================
#                                      IMPORTS
# ==============================================================================

from bulbs.property import Integer
from bulbs.property import String


# ==============================================================================
#                                    EXTENSIONS
# ==============================================================================

class Boolean(Integer):
    pass

class Const(Integer):
    pass

class Url(String):
    pass

