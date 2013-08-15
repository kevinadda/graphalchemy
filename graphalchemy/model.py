#! /usr/bin/env python
# -*- coding: utf-8 -*-

# ==============================================================================
#                                      IMPORTS
# ==============================================================================

from bulbs.model import Node
from graphalchemy.repository import BulbsNodeRepository
from bulbs.model import Relationship
from graphalchemy.repository import BulbsRelationshipRepository

from bulbs.model import STRICT


# ==============================================================================
#                                    RELATIONS
# ==============================================================================

class Relationship(Relationship):
    """ Thin wrapper around the base bulbs.model.Relationship class. It is essentially
    designed to provide more flexibility in the coding.
    
    >>> from my.models.nodes import WebsiteHostsPage
    >>> hosts = WebsiteHostsPage(since=2013)
    >>> hosts.accessible = True
    >>> hosts.set_inV(website)
    >>> hosts.set_outV(page)
    >>> ogm.add(hosts)
    >>> ogm.flush()
    """
    
    def __init__(self, *args, **kwargs):
        """ Overwrites the bulbs.element.Element __init__ method in order to 
        be able to create an Element without passing the client.
        """
        self._outV_vertex = None
        self._inV_vertex = None
        
        # Load keyword arguments
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        # Replace the "client" argument if not provided
        if args is ():
            args = (None, )
                
        # Init the Element with the regular method
        super(Relationship, self).__init__(*args)
    
    
    def set_outV(self, vertex):
        self._outV_vertex = vertex
        return self
    
    
    def set_inV(self, vertex):
        self._inV_vertex = vertex
        return self
    
    
    @classmethod 
    def get_proxy_class(cls):
        return BulbsRelationshipRepository
    
    
    def __unicode__(self):
        """ Overwrites the bulbs.element.Element __unicode__ method in order to 
        prevent it to crash when the client is not initialized.
        
        :returns: str -- A human-readable representation of the Node.
        """
        if self._result is None:
            return '<%s: %s>' % (self.__class__.__name__, 'Not persisted')
        return super(Relationship, self).__unicode__()
    
    

# ==============================================================================
#                                      NODES
# ==============================================================================

class Node(Node):
    """ Thin wrapper around the base bulbs.model.Node class. It is essentially
    designed to provide more flexibility in the coding.
    
    >>> from my.models.nodes import Website
    >>> website = Website(name="AllRecipes")
    >>> website.domain = 'http://www.allrecipes.com'
    >>> ogm.add(website)
    >>> ogm.flush()
    """
    
    """ Use strict mode in order to limit the items persisted in the database.
    """
    __mode__ = STRICT
    
    
    def __init__(self, *args, **kwargs):
        """ Overwrites the bulbs.element.Element __init__ method in order to 
        be able to create an Element without passing the client.
        """
        
        # Load keyword arguments
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        # Replace the "client" argument if not provided
        if args is ():
            args = (None, )
                
        # Init the Element with the regular method
        super(Node, self).__init__(*args)
    
    
    @classmethod 
    def get_proxy_class(cls):
        return BulbsNodeRepository
    
    
    def __unicode__(self):
        """ Overwrites the bulbs.element.Element __unicode__ method in order to 
        prevent it to crash when the client is not initialized.
        
        :returns: str -- A human-readable representation of the Node.
        """
        if self._result is None:
            return '<%s: %s>' % (self.__class__.__name__, 'Not persisted')
        return super(Node, self).__unicode__()
    
    