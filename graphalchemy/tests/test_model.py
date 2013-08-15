#! /usr/bin/env python
#-*- coding: utf-8 -*-

# ==============================================================================
#                                      IMPORTS
# ==============================================================================

from graphalchemy.tests.abstract import GraphAlchemyTestCase

# Models
from graphalchemy.fixture.model import Recipe


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
    # For future reference, the entity creation process in bulbs : 
    # ======================================================================
    # _properties : set in meta
    #   Element.__init__
    #       self._client = client
    #       self._data = {}
    #       self._result = None
    #       self._vertices = None
    #       self._edges = None
    #       self._initialized = True
    #   recipe._create(_data, kwds)
    #       data, index_name, keys = self.get_bundle(_data, **kwds)
    #       resp = self._client.create_indexed_vertex(data, index_name, keys)
    #       result = resp.one()
    #       self._initialize(result)
    #           Vertex._initialize(self,result)
    #               self._result = result
    #               self._data = result.get_data().copy() 
    #               self._set_pretty_id(self._client)
    #               self._vertices = VertexProxy(Vertex,self._client)
    #               self._edges = EdgeProxy(Edge,self._client)
    #           self._initialized = False
    #           self._set_property_data()
    #               Transfers the stuff in _data to the attributes
    #           self._initialized = True

