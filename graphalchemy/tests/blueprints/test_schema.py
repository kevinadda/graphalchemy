#! /usr/bin/env python
#-*- coding: utf-8 -*-

# ==============================================================================
#                                      IMPORTS
# ==============================================================================

from unittest import TestCase

# Services to test
from graphalchemy.blueprints.validation import Validator

# Model
from graphalchemy.blueprints.schema import MetaData

# Fixtures
from graphalchemy.fixture.declarative import Website
from graphalchemy.fixture.declarative import Page
from graphalchemy.fixture.declarative import WebsiteHostsPage
from graphalchemy.fixture.declarative import website
from graphalchemy.fixture.declarative import page
from graphalchemy.fixture.declarative import websiteHostsPageZ


# ==============================================================================
#                                     TESTING
# ==============================================================================

class MetadataTestCase(TestCase):

    def test_is_relationship(self):

        # Local fixtures
        d0 = {
            'title': 'Foo',
            'content': 'Bar',
        }
        d1 = {
            'title': 'Foo',
            'content': 'Bar',
            website.model_name_storage_key: website.model_name
        }
        d2 = {
            'title': 'Foo',
            'content': 'Bar',
            websiteHostsPageZ.model_name_storage_key: websiteHostsPageZ.model_name
        }
        metadata = MetaData()

        # Initialization, no model loaded.
        self.assertFalse(metadata.is_node(Website()))
        self.assertFalse(metadata.is_relationship(Website()))
        self.assertFalse(metadata.is_bind(Website()))
        self.assertFalse(metadata.is_node(WebsiteHostsPage()))
        self.assertFalse(metadata.is_relationship(WebsiteHostsPage()))
        self.assertFalse(metadata.is_bind(WebsiteHostsPage()))
        self.assertIsNone(metadata.for_dict(d0))
        self.assertIsNone(metadata.for_dict(d1))
        self.assertIsNone(metadata.for_dict(d2))

        # Bind nodes
        metadata.bind_node(Website, website)
        metadata.bind_relationship(WebsiteHostsPage, websiteHostsPageZ)

        # Models bound.
        self.assertTrue(metadata.is_node(Website()))
        self.assertFalse(metadata.is_relationship(Website()))
        self.assertTrue(metadata.is_bind(Website()))
        self.assertFalse(metadata.is_node(WebsiteHostsPage()))
        self.assertTrue(metadata.is_relationship(WebsiteHostsPage()))
        self.assertTrue(metadata.is_bind(WebsiteHostsPage()))
        self.assertIsNone(metadata.for_dict(d0))
        self.assertIs(website, metadata.for_dict(d1))
        self.assertIs(websiteHostsPageZ, metadata.for_dict(d2))
