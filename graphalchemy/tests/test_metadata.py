#! /usr/bin/env python
# -*- coding: utf-8 -*-

# ==============================================================================
#                                      IMPORTS
# ==============================================================================

from graphalchemy.tests.abstract import GraphAlchemyTestCase

from graphalchemy.metadata import BulbsMetadata
from graphalchemy.model import Node
from bulbs.property import String


# ==============================================================================
#                                     LOCAL FIXTURES
# ==============================================================================

class User(Node):
    element_type = 'User'
    firstname = String(indexed=True)
    lastname = String()
    

# ==============================================================================
#                                     BASE CLASS
# ==============================================================================

class BulbsMetadataTestCase(GraphAlchemyTestCase):
    
    def test___init__(self):
        
        metadata = BulbsMetadata(User)
        self.assertEquals(metadata.indices, ['firstname'])

        