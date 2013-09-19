#! /usr/bin/env python
#-*- coding: utf-8 -*-

# ==============================================================================
#                                      IMPORTS
# ==============================================================================

from unittest import TestCase

# Services to test
from graphalchemy.blueprints.schema import Node
from graphalchemy.blueprints.schema import Relationship
from graphalchemy.blueprints.schema import MetaData
from graphalchemy.blueprints.schema import Validator
from graphalchemy.blueprints.schema import Property
from graphalchemy.blueprints.schema import MigrationGenerator
from graphalchemy.blueprints.schema import Adjacency

# Fixtures
from graphalchemy.fixture.declarative import Website
from graphalchemy.fixture.declarative import Page
from graphalchemy.fixture.declarative import WebsiteHostsPage
from graphalchemy.fixture.declarative import website
from graphalchemy.fixture.declarative import page
from graphalchemy.fixture.declarative import websiteHostsPageZ

# Types
from graphalchemy.blueprints.types import List
from graphalchemy.blueprints.types import String
from graphalchemy.blueprints.types import Boolean
from graphalchemy.blueprints.types import Url
from graphalchemy.blueprints.types import DateTime

# Auxiliary
from graphalchemy.ogm.mapper import Mapper

from datetime import datetime


# ==============================================================================
#                                     TESTING
# ==============================================================================

class MetadataTestCase(TestCase):

    def test_is_relationship(self):

        metadata = MetaData()
        self.assertFalse(metadata.is_node(Website()))
        self.assertFalse(metadata.is_relationship(Website()))
        self.assertFalse(metadata.is_bind(Website()))
        self.assertFalse(metadata.is_node(WebsiteHostsPage()))
        self.assertFalse(metadata.is_relationship(WebsiteHostsPage()))
        self.assertFalse(metadata.is_bind(WebsiteHostsPage()))

        metadata.bind_node(Website, website)
        metadata.bind_relationship(WebsiteHostsPage, websiteHostsPageZ)
        self.assertTrue(metadata.is_node(Website()))
        self.assertFalse(metadata.is_relationship(Website()))
        self.assertTrue(metadata.is_bind(Website()))
        self.assertFalse(metadata.is_node(WebsiteHostsPage()))
        self.assertTrue(metadata.is_relationship(WebsiteHostsPage()))
        self.assertTrue(metadata.is_bind(WebsiteHostsPage()))


class ValidatorTestCase(TestCase):

    def setUp(self):
        self.mapper = Mapper()
        self.metadata = MetaData()
        self.validator = Validator(self.metadata)

    def test_run(self):

        class Website(object):
            def __init__(self):
                self.name = None
                self.url = None
        website = Node('Website', self.metadata,
            Property('name', String(127), nullable=False, index=True),
            Property('url', Url(), nullable=False, index=True),
        )
        self.mapper(Website, website)
        obj = Website()

        # Null value
        obj.name = None
        obj.url = None
        ok, errors = self.validator.run(obj)
        self.assertFalse(ok)
        self.assertEquals({
            "name":[u'Property is not nullable.'],
            'url': [u'Property is not nullable.']
        }, errors)

        # Ability to reach to the second level
        obj.name = "*"*128
        obj.url = "http://www.url.com/"
        ok, errors = self.validator.run(obj)
        self.assertFalse(ok)
        self.assertEquals({"name":[u'Value is too long : 128 > 127']}, errors)

        # Ability to check various properties
        obj.name = "*"*127
        obj.url = "bla"
        ok, errors = self.validator.run(obj)
        self.assertFalse(ok)
        self.assertEquals({'url': [u'Unable to parse URL']}, errors)

        # Ability to accumulate errors on various properties
        obj.name = "*"*128
        obj.url = "bla"
        ok, errors = self.validator.run(obj)
        self.assertFalse(ok)
        self.assertEquals({"name":[u'Value is too long : 128 > 127'], 'url': [u'Unable to parse URL']}, errors)

        # Return value if success
        obj.name = "*"*127
        obj.url = "http://www.url.com/"
        ok, errors = self.validator.run(obj)
        self.assertTrue(ok)
        self.assertEquals({}, errors)


class TestMigrationGenerator(TestCase):

    def setUp(self):
        self.mapper = Mapper()
        self.metadata = MetaData()
        self.validator = Validator(self.metadata)


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





