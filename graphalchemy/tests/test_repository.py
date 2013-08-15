#! /usr/bin/env python
# -*- coding: utf-8 -*-

# ==============================================================================
#                                      IMPORTS
# ==============================================================================

from graphalchemy.tests.abstract import GraphAlchemyTestCase

from graphalchemy.repository import BulbsNodeRepository
from graphalchemy.repository import BulbsRelationshipRepository
from graphalchemy.metadata import BulbsMetadata

from mock import Mock
from graphalchemy.fixture.model import Website
from graphalchemy.fixture.instance import PageFixture


# ==============================================================================
#                                     LOCAL FIXTURES
# ==============================================================================

class TestGraph():
    def __init__(self):
        self.Website = None
        self.client = None
    def add_proxy(self, repository_name, element_class):
        return


# ==============================================================================
#                                     BASE CLASS
# ==============================================================================

class BulbsNodeRepositoryTestCase(GraphAlchemyTestCase):
            
        
    def test__get_index(self):
        
        self.graph = TestGraph()
        self.graph.client = self.ogm.client
        self.metadata = BulbsMetadata(Website)
        
        repository = BulbsNodeRepository(Website, self.graph.client, graph=self.graph)
        repository.metadata=None
        self.assertIs(None, repository._get_index())
        
        self.metadata.indices = []
        repository = BulbsNodeRepository(Website, self.graph.client, graph=self.graph)
        repository.metadata=self.metadata
        self.assertEquals([], repository._get_index())
        
        self.metadata.indices = ['name']
        repository = BulbsNodeRepository(Website, self.graph.client, graph=self.graph)
        repository.metadata=self.metadata
        self.assertEquals(['name'], repository._get_index())
    
    
    def test__get_index_among(self):
        
        self.graph = TestGraph()
        self.graph.client = self.ogm.client
        self.metadata = BulbsMetadata(Website)
        self.metadata.indices = Mock()
        
        repository = BulbsNodeRepository(Website, self.graph.client, graph=self.graph)
        repository.metadata=None
        self.assertIs(None, repository._get_index_among([]))
        
        self.metadata.indices = []
        repository = BulbsNodeRepository(Website, self.graph.client, graph=self.graph)
        repository.metadata=self.metadata
        self.assertIs(None, repository._get_index_among([]))
        
        self.metadata.indices = ['name']
        repository = BulbsNodeRepository(Website, self.graph.client, graph=self.graph)
        repository.metadata=self.metadata
        self.assertEquals(['name'], repository._get_index_among(['name', 'content']))
    
        self.metadata.indices = ['name']
        repository = BulbsNodeRepository(Website, self.graph.client, graph=self.graph)
        repository.metadata=self.metadata
        self.assertEquals(None, repository._get_index_among(['content', 'description']))
    
    
    def test__build_query_filter(self):
        
        self.graph = TestGraph()
        self.graph.client = self.ogm.client
        self.metadata = BulbsMetadata(Website)
        
        # No metadata
        metadata = None
        repository = BulbsNodeRepository(Website, self.graph.client, graph=self.graph)
        repository.metadata=metadata
        self.assertEquals((
            u'g.v(eid)', 
            {'eid': 123}
        ), repository._build_query_filter(eid=123))
        self.assertEquals((
            u'g.V.has("name", name)', 
            {u'name': 'Foo'}
        ), repository._build_query_filter(name='Foo'))
        self.assertEquals((
            u'g.V.has("content", content).has("name", name)', 
            {u'content': 'Bar', u'name': 'Foo'}
        ), repository._build_query_filter(name='Foo', content='Bar'))
        
        # Empty metadata
        self.metadata.indices = []
        repository = BulbsNodeRepository(Website, self.graph.client, graph=self.graph)
        repository.metadata=self.metadata
        self.assertEquals((
            u'g.v(eid)',
            {'eid': 123}
        ), repository._build_query_filter(eid=123))
        self.assertEquals((
            u'g.V.has("name", name)', 
            {u'name': 'Foo'}
        ), repository._build_query_filter(name='Foo'))
        self.assertEquals((
            u'g.V.has("content", content).has("name", name)', 
            {u'content': 'Bar', u'name': 'Foo'}
        ), repository._build_query_filter(name='Foo', content='Bar'))
        
        # Metadata with an index
        self.metadata.indices = ['name']
        repository = BulbsNodeRepository(Website, self.graph.client, graph=self.graph)
        repository.metadata=self.metadata
        self.assertEquals((
            u'g.v(eid)', 
            {'eid': 123}
        ), repository._build_query_filter(eid=123))
        self.assertEquals((
            u'g.V("name", name)',
            {u'name': 'Foo'}
        ), repository._build_query_filter(name='Foo'))
        self.assertEquals((
            u'g.V("name", name).has("content", content)', 
            {u'content': 'Bar', u'name': 'Foo'}
        ), repository._build_query_filter(name='Foo', content='Bar'))
        self.assertEquals((
            u'g.v(eid).has("name", name)', 
            {'eid': 123, u'name': 'Foo'}
        ), repository._build_query_filter(eid=123, name='Foo'))
        

    def test_create(self):        
        
        repository = self.ogm.repository('Website')
        
        recipe = repository.create(title='Fixture - Create')
        self.assertEquals(recipe.title, 'Fixture - Create')
        
        recipe = repository(title='Fixture - Create')
        self.assertEquals(recipe.title, 'Fixture - Create')
        

    def test_filter_true(self):
        
        # Load repository
        repository = self.ogm.repository('Page')
        page_fixture = PageFixture(self.ogm)
        page_fixture.clean()
        page_fixture.load()
        
        # Load objects
        website = page_fixture._parent['Website'].get('Website1')
        page = page_fixture.get('Website1Page1')
        
        # Ability to get()
        page_found = repository.get(page.eid)
        self.assertEquals(page_found.eid, page.eid)
        self.assertEquals(page_found.isHostedBy().eid, website.eid)
        
        # Ability to filter on eid
        results = repository.filter(eid=page.eid)
        page_found = next(results)
        self.assertEquals(page_found.eid, page.eid)
        self.assertEquals(page_found.isHostedBy().eid, website.eid)
        
        # Ability to filter on a set of parameters
        results = repository.filter(
            title=page.title,
            url=page.url
        )
        page_found = next(results)
        self.assertEquals(page_found.eid, page.eid)
        self.assertEquals(page_found.isHostedBy().eid, website.eid)
        
        # Ability to lazy-load
        pages = list(website.hosts())
        self.assertEquals(pages[0].eid, page.eid)
        # self.assertEquals(website.hosts()[0], page)
        self.assertEquals(len(pages), 2)
        