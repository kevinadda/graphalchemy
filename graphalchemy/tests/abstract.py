#! /usr/bin/env python
#-*- coding: utf-8 -*-

# ==============================================================================
#                                      IMPORTS
# ==============================================================================

from unittest import TestCase

# Services
from graphalchemy.ogm import BulbsObjectManager


# ==============================================================================
#                                     TESTING
# ==============================================================================

class GraphAlchemyTestCase(TestCase):
    """ Base class for GraphAlchemy tests. Loads the default OGM in the ogm
    attribute;
    """
    
    ogm = BulbsObjectManager(
        "http://localhost:8182/graphs/", 
        "graph", 
        model_paths=['graphalchemy.fixture.model']
    )
    