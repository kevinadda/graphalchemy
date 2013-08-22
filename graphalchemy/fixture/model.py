#! /usr/bin/env python
# -*- coding: utf-8 -*-

# ==============================================================================
#                                      IMPORTS
# ==============================================================================

from graphalchemy.model import Node
from graphalchemy.model import Relationship

from bulbs.property import Integer
from bulbs.property import Float
from bulbs.property import String
from graphalchemy.property import Url
from graphalchemy.property import Boolean


# ==============================================================================
#                                     NODES
# ==============================================================================

class Website(Node):
    element_type                = "Website"
    name                        = String(indexed=True)
    description                 = String()
    content                     = String()
    domain                      = Url()
    
    def hosts(self):
        return self.outV('hosts')


class Page(Node):
    element_type                = "Page"
    url                         = Url(indexed=True)
    title                       = String()
    
    def isHostedBy(self):
        website = self.inV('hosts')
        if website:
            return next(website)
        return None


class Recipe(Node):
    element_type                = "Recipe"
    timeTotal                   = Float()
    timePreparation             = Float()
    title                       = String()


# ==============================================================================
#                                   RELATIONS
# ==============================================================================

class WebsiteHostsPage(Relationship):
    label                       = 'hosts'
    since                       = Integer()
    accessible                  = Boolean()
    # from_type                 = Website
    # to_type                   = Page


class PageDescribesRecipe(Relationship):
    label                       = 'describes'
    # from_type                 = Page
    # to_type                   = Recipe
