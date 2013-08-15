#! /usr/bin/env python
# -*- coding: utf-8 -*-

# ==============================================================================
#                                   IMPORTS
# ==============================================================================

# Bulbs
from bulbs.model import NodeProxy
from bulbs.model import RelationshipProxy

from graphalchemy.metadata import BulbsMetadata

# ==============================================================================
#                               IMPLEMENTATION
# ==============================================================================

class BulbsRelationshipRepository(RelationshipProxy): # NodeProxy):

    def __init__(self, element_class, client, graph=None, logger=None):
        super(BulbsRelationshipRepository, self).__init__(element_class, client)



class BulbsNodeRepository(NodeProxy): # NodeProxy):
    """ Thin wrapper around the base Bulbs proxy designed to provide a more 
    SQL-alchemesque interface.
    
    These repositories can be loaded directly from the OGM :
    >>> repository = ogm.repository('User')
    
    Easy entity creation and pre-persistence :
    >>> user = repository(firstname="Bob")
    >>> user = repository.create(firstname="Joe")
    
    SQL-alchemy like API for querying, with automatic index selection :
    >>> users = repository.filter(firstname="Joe")
    >>> users = repository.filter(firstname="Joe", lastname="Miller")
    """
    
    def __init__(self, element_class, client, graph=None, logger=None):
        """ Initializes the repository with the bulbs proxy and our metadata.
        
        :param graph: Bulbs graph object.
        :type graph: bulbs.base.graph.Graph
        :param name: Name of the repository.
        :type name: str
        :param metadata: Metadata associated with the current model.
        :type metadata: graphalchemy.metadata.GraphMetadata
        :param logger: Optional logger to listen on queries.
        :type logger: jerome.application.service.logger.LoggerInterface
        """
        self.graph = graph
        if hasattr(element_class, 'element_type'):
            repository_name = str(element_class.element_type)
        elif hasattr(element_class, 'label'):
            repository_name = str(element_class.label)
        else: 
            raise Exception('Element class seems not to be Node nor Relationship.')
            
        if graph:
            self.graph.add_proxy(repository_name, element_class)
            client = self.graph.client
        self.name = repository_name
        
        super(BulbsNodeRepository, self).__init__(element_class, client)
        
        self.metadata = BulbsMetadata(element_class)
        self.logger = logger
        
        
    def get(self, *args, **kwargs):
        result = super(BulbsNodeRepository, self).get(*args, **kwargs)
        if result.element_type != self.name:
            raise Exception('The entity matching the query does not correspond to the repository.')
        return result
    
        
    def __call__(self, *args, **kwargs):
        """ Thin wrapper for entity creation :
        >>> recipe = repository(firstname='Foo', lastname='Bar')
        
        NB : this will simultaneously persist the entity in the database, so you
        will get an object that already has an eid.
        
        :returns: bulbs.model.Node, bulbs.model.Relationship -- A new object, 
        already pre-persisted in the database.
        """
        return self.create(*args, **kwargs)
        
        
    def filter(self, **kwargs):
        """ Performs a filtering operation on the given repository. Automaticaly
        decides which index to use : 
        - the eid index if provided
        - the first property key index that is matched 
        Will add extra filtering as simple as queries.
        
        Example :
        >>> iterator = repository.filter(firstname='Foo', lastname='Bar')
        >>> iterator = repository.filter(eid=123)
        >>> iterator = repository.filter(indexed_property='Baz')
        
        @todo : it should return an iterator and wait for extra filtering.
        @todo : only limited to filtering on one entity for now.
        
        :returns: generator -- The list of models that match the query.
        """
        # return self.base_repository.index.lookup(**kwargs)
        groovy, params = self._build_query_filter(**kwargs)
        self._log(groovy+u', '+unicode(params))
        return self.graph.gremlin.query(groovy, params)
        
        
    def _build_query_filter(self, **kwargs):
        """ Builds a gremlin query string from a set of filtering arguments.
        @todo : no escaping is implemented yet.
        
        :returns: string, dict -- The gremlin query.
        """
        params = {}
        # If the value is in the parameters :
        if 'eid' in kwargs:
            groovy = u'g.v(eid)'
            params['eid'] = int(kwargs['eid'])
            del kwargs['eid']
        else:
        # If one of the parameters is indexed :
            useful_indices = self._get_index_among(kwargs.keys())
            if useful_indices:
                key = useful_indices[0]
                groovy = u'g.V("'+unicode(key)+'", '+unicode(key)+u')'
                params[unicode(key)] = kwargs[key]
                del kwargs[key]
        # If no parameter is indexed :
            else:
                groovy = u'g.V'
                
        # Fillup with remaining
        for key, val in kwargs.iteritems():
            groovy = groovy+u'.has("'+unicode(key)+u'", '+unicode(key)+u')'
            params[unicode(key)] = val
            
        return groovy, params
        
        
    def _get_index(self):
        """ Returns the list of indices for the current repository.
        
        :returns: list, None -- the list of indices.
        """
        if not self.metadata:
            return None
        return self.metadata.indices
        
        
    def _get_index_among(self, given_indices):
        """ Returns the intersection between the given_indices list and the list
        of indices for the given repository.
        
        :returns: list, None -- the list of indices.
        """
        indices = self._get_index()
        if not indices:
            return None
        useful_indices = list(set(given_indices) & set(indices))
        if not useful_indices:
            return None
        return useful_indices

    
    def _log(self, message, level=10):
        """ Thin wrapper for logging purposes.
        
        :param message: The message to log.
        :type message: str
        :param level: The level of the log.
        :type level: int
        :returns: graphalchemy.repository.BulbsNodeRepository -- this repository
        itself.
        """
        if self.logger:
            self.logger.log(level, message)
        return self
    