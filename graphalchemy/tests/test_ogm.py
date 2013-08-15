#! /usr/bin/env python
# -*- coding: utf-8 -*-

# ==============================================================================
#                                      IMPORTS
# ==============================================================================

from graphalchemy.tests.abstract import GraphAlchemyTestCase

from graphalchemy.fixture.model import Recipe


# ==============================================================================
#                                     BASE CLASS
# ==============================================================================

class BulbsObjectManagerTestCase(GraphAlchemyTestCase):
    
    def test_run(self):
        
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
        
        # Flush the recipe
        self.ogm.add(recipe)
        self.ogm.flush()
        
        # Verify
        eid = recipe.eid
        self.assertTrue(eid > 0)
        self.assertEquals('Recipe', recipe.element_type)
        self.assertEquals(30, recipe.timeTotal)
        self.assertEquals('Hello', recipe.title)
        self.assertEquals({u'element_type': u'Recipe', u'timeTotal': 30, u'title': u'Hello'}, recipe._data)
        self.assertTrue(recipe._initialized)
        recipe_titan = self.ogm.repository('Recipe').get(eid)
        recipe_titan = self.ogm.query('g.v(eid)', {'eid':eid})
        recipe_titan = next(recipe_titan)
        self.assertEquals(eid, recipe_titan.eid)
        self.assertEquals('Recipe', recipe_titan.element_type)
        self.assertEquals(30, recipe_titan.timeTotal)
        self.assertEquals('Hello', recipe_titan.title)
        
        # Update
        recipe.title = 'Hello2'
        recipe.timeTotal = 35
        recipe.timePreparation = 40
        self.assertEquals('Recipe', recipe.element_type)
        self.assertEquals(35, recipe.timeTotal)
        self.assertEquals(40, recipe.timePreparation)
        self.assertEquals('Hello2', recipe.title)
        
        # Re-update
        self.ogm.flush()
        self.assertEquals(eid, recipe.eid)
        self.assertEquals(35, recipe.timeTotal)
        self.assertEquals(40, recipe.timePreparation)
        self.assertEquals('Hello2', recipe.title)
        recipe_titan = self.ogm.repository('Recipe').get(eid)
        recipe_titan = self.ogm.query('g.v(eid)', {'eid':eid})
        recipe_titan = next(recipe_titan)
        self.assertEquals(eid, recipe_titan.eid)
        self.assertEquals('Recipe', recipe_titan.element_type)
        self.assertEquals(35, recipe_titan.timeTotal)
        self.assertEquals(40, recipe_titan.timePreparation)
        self.assertEquals('Hello2', recipe_titan.title)

