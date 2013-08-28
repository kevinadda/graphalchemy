#! /usr/bin/env python
# -*- coding: utf-8 -*-

# ==============================================================================
#                                      IMPORTS
# ==============================================================================

# ==============================================================================
#                                    EXTENSIONS
# ==============================================================================


class Type(object):
    def __init__(self, *args, **kwargs):
        pass
    
    def coerce(self, value):
        return value
    
    def validate(self, value):
        return True
    
    def __repr__(self):
        return self.__class__.__name__


class Integer(Type):
    def __init__(self):
        pass

    def coerce(self, value):
        return int(value)


class DateTime(Type):
    pass


class Boolean(Integer):
    pass


class Const(Integer):
    pass


class String(Type):
    def __init__(self, size):
        self.size = size


class Url(String):
    pass

