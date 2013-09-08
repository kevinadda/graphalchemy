#! /usr/bin/env python
#-*- coding: utf-8 -*-

# ==============================================================================
#                                      IMPORTS
# ==============================================================================


# ==============================================================================
#                                     SERVICE
# ==============================================================================

class Repository(object):
    """ Repositories are shortcuts that allow simple querying of entities.

    Repositories can be loaded directly from the OGM :
    >>> repository = ogm.repository('Website')

    Easy entity creation and pre-persistence :
    >>> website = repository(domain="http://www.foodnetwork.com")
    >>> website = repository.create(domain="http://www.allrecipes.com")

    SQL-alchemy like API for querying, with automatic index selection :
    >>> repository = ogm.repository('User')
    >>> users = repository.filter(firstname="Joe")
    >>> users = repository.filter(firstname="Joe", lastname="Miller")
    """

    def __init__(self, session, model, class_, logger=None):
        """ Loads a repository.

        :param session: The session to perform requests against.
        :type session: graphalchemy.ogm.session.Session
        :param model: The model instance of the current class.
        :type model: graphalchemy.blueprints.schema.Model
        :param class_: The class that is actually mapped.
        :type class_: object
        :param logger: An optionnal logger.
        :type logger: logging.Logger
        """
        self.session = session
        self.model = model
        self.class_ = class_
        self.logger = logger


    def __call__(self, *args, **kwargs):
        """ Creates an instance of the mapped class, initialized with the
        given parameters.

        Example use:
        >>> website = repository(domain="http://www.foodnetwork.com")

        :param class_: The class that is actually mapped.
        :type class_: object
        """
        return self.create(*args, **kwargs)


    def create(self, *args, **kwargs):
        """ Creates an instance of the mapped class, initialized with the
        given parameters.

        Example use :
        >>> website = repository.create(domain="http://www.allrecipes.com")

        :param class_: The class that is actually mapped.
        :type class_: object
        """
        return self.class_(*args, **kwargs)


    def get(self, id):
        # Retrieve from DB
        response = self.client.get_vertex(id)
        results = response.content['results']
        
        # Verify type
        type = results.pop('type')
        if type != 'vertex' and model.is_node() == False:
            raise Exception('Expected vertex, got '+str(type))
        elif type != 'edge' and model.is_relationship() == False:
            raise Exception('Expected edge, got '+str(type))
        else:
            raise Exception('Unknown type '+str(type))
        
        # Verify id
        _id = results.pop('_id')
        if _id != id:
            raise Exception('Expected '+str(id)+', got '+str(_id))
        
        # Build object
        obj = self.class_()
        for property_db, value_db in results.iteritems():
            found = False
            for property in self.model.properties:
                if property.name_db != property_db:
                    continue
                found = True
                break
            if not found:
                raise Exception('Property retrieved but not found : '+property_db)
            value_py = property.coerce_to_py(value_db)
            setattr(obj, property.name_py, value_py)
            
        
        # Add to the entity map
        id = response.content['results']['_id']
        self.identity_map[obj] = InstanceState(obj)
        self.identity_map[obj].update_id(id)
        self.identity_map[obj].update_attributes(data)
        
        return initialize_element(self.client, resp.results)