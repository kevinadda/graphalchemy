#! /usr/bin/env python
#-*- coding: utf-8 -*-

# ==============================================================================
#                                      IMPORTS
# ==============================================================================

from unittest import TestCase

# Services to test
from graphalchemy.blueprints.migration import MigrationGenerator

# Model
from graphalchemy.blueprints.schema import Node
from graphalchemy.blueprints.schema import Relationship
from graphalchemy.blueprints.schema import MetaData
from graphalchemy.blueprints.schema import Property
from graphalchemy.blueprints.schema import Adjacency

# Types
from graphalchemy.blueprints.types import List
from graphalchemy.blueprints.types import String
from graphalchemy.blueprints.types import Boolean
from graphalchemy.blueprints.types import Url
from graphalchemy.blueprints.types import DateTime

# Auxiliary
from graphalchemy.ogm.mapper import Mapper


# ==============================================================================
#                                     TESTING
# ==============================================================================

class TestMigrationGenerator(TestCase):

    def setUp(self):
        self.mapper = Mapper()
        self.metadata = MetaData()


    def test_node(self):

        class Website(object):
            def __init__(self):
                self.name = None
                self.url = None
        website = Node('Website', self.metadata,
            Property('name', String(127), nullable=False, index='search', group='name', prefix=True),
            Property('url', Url(), nullable=False, index=True, unique=True),
            Property('tags', List(), nullable=False, index=None),
        )

        class WebsiteHostsPage(object):
            def __init__(self, *args, **kwargs):
                self.label = 'hosts'
                self.since = None
                self.accessible = None
        websiteHostsPage = Relationship('hosts', self.metadata,
            Property('since', DateTime, nullable=False, primaryKey=True),
            Property('accessible', Boolean())
        )

        websiteHostsPage_out = Adjacency(website, websiteHostsPage,
            direction=Relationship.OUT,
            unique=True,
            nullable=False
        )



        self.mapper(WebsiteHostsPage, websiteHostsPage)
        self.mapper(Website, website, properties={
            'hosts': websiteHostsPage_out
        })

        self.migration_generator = MigrationGenerator(self.metadata)

        self.migration_generator.run()
        print self.migration_generator.__str__()
        assert False

