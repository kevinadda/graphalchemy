#! /usr/bin/env python
# -*- coding: utf-8 -*-

# ==============================================================================
#                                      IMPORTS
# ==============================================================================

from graphalchemy.fixture.abstract import AbstractFixture


# ==============================================================================
#                                  FIXTURE GENERATION
# ==============================================================================

class WebsiteFixture(AbstractFixture):
    """ Fixture for Websites.
    """
    
    def __init__(self, em):
        super(WebsiteFixture, self).__init__(em)
        self.repository = em.repository('Website')
        

    def clean_self(self):
        query = "g.E.has('label', 'hosts').each{g.removeEdge(it)}"
        self.em.query(query, {})
        query = "g.V.has('element_type', 'Website').filter{it.name == null || it.name.contains('Fixture')}.each{g.removeVertex(it)}"
        self.em.query(query, {})
        self._fixtures = {}
        return self


    def build(self):
        
        # ----------------------------------------------------------------------
        # CusineAZ Publisher website
        # ----------------------------------------------------------------------
        website1 = self.repository.create()
        website1.name = u'Fixture - Website - AllRecipes'
        website1.domain = u'http://www.allrecipes.com'
        self._fixtures['Website1'] = website1
        
        # ----------------------------------------------------------------------
        # Canalblog Blog website
        # ----------------------------------------------------------------------
        website2 = self.repository.create()
        website2.name = u'Fixture - Website - FoodNetwork'
        website2.domain = u'http://www.foodnetwork.com'
        self._fixtures['Website2'] = website2
        
        return self



class PageFixture(AbstractFixture):
    """ Fixture for Pages.
    """
    
    def __init__(self, em):
        super(PageFixture, self).__init__(em)
        self.repository = em.repository('Page')
        self._parent['Website'] = WebsiteFixture(em)
        

    def clean_self(self):
        """ Removes all fixtures from the Database.
        """
        query = "g.E.has('label', 'hosts').each{g.removeEdge(it)}"
        self.em.query(query, {})
        query = "g.V.has('element_type', 'Page').filter{it.title == null || it.title.contains('Fixture')}.each{g.removeVertex(it)}"
        self.em.query(query, {})
        self._fixtures = {}
        return self


    def build(self):
        """ Creates fixtures one by one.
        """

        # ----------------------------------------------------------------------
        # Recipe page from CuisineAZ
        # ----------------------------------------------------------------------
        page1 = self.repository.create()
        page1.title = u"Fixture - Page1"
        page1.url = 'http://www.allrecipes.com/page/1'
        
        self.em.repository('WebsiteHostsPage').create(
            self._parent['Website'].get('Website1'),
            page1
        )
        
        self._fixtures['Website1Page1'] = page1

        # ----------------------------------------------------------------------
        # Recipe page from CuisineAZ
        # ----------------------------------------------------------------------
        page2 = self.repository.create()
        page2.title = u"Fixture - Page2"
        page2.url = 'http://www.allrecipes.com/page/2'
        
        self.em.repository('WebsiteHostsPage').create(
            self._parent['Website'].get('Website1'),
            page2
        )
        
        self._fixtures['Website1Page2'] = page2

        # ----------------------------------------------------------------------
        # Section page from CuisineAZ
        # ----------------------------------------------------------------------
        page3 = self.repository.create()
        page3.title = u"Fixture - Page3"
        page3.url = u'http://www.foodnetwork.com/page3'
        
        self.em.repository('WebsiteHostsPage').create(
            self._parent['Website'].get('Website2'),
            page3
        )
        
        self._fixtures['Website2Page1'] = page3
        
        # ----------------------------------------------------------------------
        # Post page from Canalblog 
        # ----------------------------------------------------------------------
        page4 = self.repository.create()
        page4.title = u'Fixture - Page4'
        page4.url = u'http://www.foodnetwork.com/page4'
        
        self.em.repository('WebsiteHostsPage').create(
            self._parent['Website'].get('Website2'),
            page4
        )
        
        self._fixtures['Website2Page2'] = page4
        
        # ----------------------------------------------------------------------
        # Homepage from Canalblog 
        # ----------------------------------------------------------------------
        page5 = self.repository.create()
        page5.title = u'Fixture - Page5'
        page5.url = u'http://www.foodnetwork.com/page5'
        
        self.em.repository('WebsiteHostsPage').create(
            self._parent['Website'].get('Website2'),
            page5
        )
        
        self._fixtures['Website2Page3'] = page5
        
        return self
    
    