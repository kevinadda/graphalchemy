#! /usr/bin/env python
#-*- coding: utf-8 -*-

# ==============================================================================
#                                      IMPORTS
# ==============================================================================

from graphalchemy.tests.abstract import GraphAlchemyTestCase

# Models
from graphalchemy.fixture.model import Recipe
from graphalchemy.fixture.model import WebsiteHostsPage

# Fixtures
from graphalchemy.fixture.instance import PageFixture


# ==============================================================================
#                                 SERVICE TEST
# ==============================================================================

class NodeTest(GraphAlchemyTestCase):
    
    def test___init__(self):
        
        # Ability to create an entity directly from its model :
        recipe = Recipe(timeTotal=30)
        str(recipe)
        self.assertEquals('Recipe', recipe.element_type)
        self.assertEquals(30, recipe.timeTotal)
        self.assertEquals(None, recipe._client)
        self.assertIsInstance(recipe, Recipe)
        self.assertIn('timeTotal', recipe._properties)
        self.assertEquals({}, recipe._data)
        self.assertTrue(recipe._initialized)
        
        # Ability to set a property as a simple setter
        recipe.title = 'Hello'
        self.assertEquals('Hello', recipe.title)
        self.assertIn('title', recipe._properties)
        self.assertEquals({}, recipe._data)
        self.assertTrue(recipe._initialized)
        
        # Ability to load a client
        recipe = Recipe('bla')
        self.assertEquals('bla', recipe._client)
        
        
    def test_create(self):
        
        # Ability to create an entity from the repository :
        recipe = self.ogm.repository('Recipe')(timeTotal=30)
        self.assertEquals(30, recipe.timeTotal)
        self.assertIsInstance(recipe, Recipe)
        
        # Ability to create an entity from the repository create method :
        recipe = self.ogm.repository('Recipe').create(timeTotal=30)
        self.assertEquals(30, recipe.timeTotal)
        self.assertIsInstance(recipe, Recipe)
        
        
    # ======================================================================
    # For future reference, the Node creation process in bulbs : 
    # ======================================================================
    # NodeProxy.create
    #   Element.__init__
    #       self._client = client
    #       self._data = {}
    #       self._result = None
    #       self._vertices = None
    #       self._edges = None
    #       self._initialized = True
    #   Node._create(_data, kwds)
    #       data, index_name, keys = self.get_bundle(_data, **kwds)
    #       resp = self._client.create_indexed_vertex(data, index_name, keys)
    #       result = resp.one()
    #       self._initialize(result)
    #           Element._initialize(self,result)
    #               self._result = result
    #               self._data = result.get_data().copy() 
    #               self._set_pretty_id(self._client)
    #               self._vertices = VertexProxy(Vertex,self._client)
    #               self._edges = EdgeProxy(Edge,self._client)
    #           self._initialized = False
    #           self._set_property_data()
    #               Transfers the stuff in _data to the attributes
    #           self._initialized = True

    def test___init__(self):
        
        # Ability to create an entity directly from its model :
        hosts = WebsiteHostsPage(since=123)
        str(hosts)
        self.assertEquals('hosts', hosts.label)
        self.assertEquals(123, hosts.since)
        self.assertEquals(None, hosts._client)
        self.assertIsInstance(hosts, WebsiteHostsPage)
        self.assertIn('since', hosts._properties)
        self.assertEquals({}, hosts._data)
        self.assertTrue(hosts._initialized)
        
        # Ability to set a property as a simple setter
        hosts.accessible = True
        self.assertEquals(True, hosts.accessible)
        self.assertIn('since', hosts._properties)
        self.assertIn('accessible', hosts._properties)
        self.assertEquals({}, hosts._data)
        self.assertTrue(hosts._initialized)
        
        # Ability to load a client
        hosts = WebsiteHostsPage('bla')
        self.assertEquals('bla', hosts._client)
        

    def test_create(self):
        
        page_fixture = PageFixture(self.ogm)
        page_fixture.clean()
        page_fixture.load()
        inV = page_fixture._parent['Website'].get('Website1')
        outV = page_fixture.get('Website1Page1')
        
        # Ability to create an entity from the repository :
        hosts = self.ogm.repository('WebsiteHostsPage')(outV, inV, since=123)
        self.assertEquals(inV.eid, hosts._inV)
        self.assertEquals(outV.eid, hosts._outV)
        self.assertEquals(123, hosts.since)
        self.assertIsInstance(hosts, WebsiteHostsPage)
        
        # Ability to create an entity from the repository create method :
        hosts = self.ogm.repository('WebsiteHostsPage').create(outV, inV, since=30)
        self.assertEquals(inV.eid, hosts._inV)
        self.assertEquals(outV.eid, hosts._outV)
        self.assertEquals(30, hosts.since)
        self.assertIsInstance(hosts, WebsiteHostsPage)
        
        
    # ======================================================================
    # For future reference, the Relationship creation process in bulbs : 
    # ======================================================================
    # RelationshipProxy.create
    #   Element.__init__
    #       self._client = client
    #       self._data = {}
    #       self._result = None
    #       self._vertices = None
    #       self._edges = None
    #       self._initialized = True
    #   Relationship._create(_data, kwds)
    #       label = self.get_label(self._client.config)
    #       outV, inV = coerce_vertices(outV, inV)  # Returns the ids of the vertixes
    #       data, index_name, keys = self.get_bundle(_data, **kwds)
    #       resp = self._client.create_indexed_edge(outV, label, inV, data, index_name, keys)
    #       result = resp.one()
    #       self._initialize(result)
    #           Element._initialize(self,result)
    #               self._result = result
    #               self._data = result.get_data().copy() 
    #               self._set_pretty_id(self._client)
    #               self._vertices = VertexProxy(Vertex,self._client)
    #               self._edges = EdgeProxy(Edge,self._client)
    #           self._initialized = False
    #           self._set_property_data()
    #               Transfers the stuff in _data to the attributes
    #           self._initialized = True

