#! /usr/bin/env python
# -*- coding: utf-8 -*-

# ==============================================================================
#                                      IMPORTS
# ==============================================================================

from graphalchemy.blueprints.types import List
from graphalchemy.blueprints.types import Dict

# ==============================================================================
#                                      MODEL
# ==============================================================================

class Model(object):
    """ Holds all the schema characteristics that we want to enforce on an
    Element.

    This is an abstract class that is extended by specializations for Nodes
    and Relationships.
    """

    # The key under which the Model name will be saved
    model_name_storage_key = None
    model_type = None

    def __init__(self, model_name, metadata, *args, **kwargs):
        self.model_name = model_name
        self.metadata = metadata
        self.properties = {}
        self.indices = {}
        self.logger = kwargs.get('logger', None)


    def register_class(self, class_):
        raise NotImplementedError()


    def is_node(self):
        raise NotImplementedError()


    def is_relationship(self):
        raise NotImplementedError()


    def __repr__(self):
        return self.model_name


    def add_property(self, prop):
        if prop.name_py in self.properties:
            raise Exception('Cannot override previously set property.')
        self.properties[prop.name_py] = prop
        if prop.index:
            self.indices[prop.name_py] = prop
        if prop.prefix == True:
            prop.name_db = self.model_name + '_' + prop.name_db
        prop.model = self
        return self


    def _useful_indices_among(self, amongs):
        return [among for among in amongs if (among in self.indices)]



class Node(Model):

    # The key under which the Model name will be saved
    model_name_storage_key = 'element_type'
    model_type = 'vertex'

    def __init__(self, model_name, metadata, *args, **kwargs):
        super(Node, self).__init__(model_name, metadata, *args, **kwargs)
        for prop in args:
            if prop.primaryKey == True:
                raise Exception('Only edge properties can be primaryKeys.')
            self.add_property(prop)

    def register_class(self, class_):
        self.metadata.bind_node(class_, self)

    def is_node(self):
        return True

    def is_relationship(self):
        return False


class Relationship(Model):

    # The key under which the Model name will be saved
    model_name_storage_key = 'label'
    model_type = 'edge'

    IN = 'in'
    OUT = 'out'
    BOTH = 'both'

    def __init__(self, model_name, metadata, *args, **kwargs):
        super(Relationship, self).__init__(model_name, metadata, *args, **kwargs)
        self.directed = kwargs.get('directed', True)
        self.signature = kwargs.get('signature', True)
        for prop in args:
            self.add_property(prop)

    def register_class(self, class_):
        self.metadata.bind_relationship(class_, self)

    def is_node(self):
        return False

    def is_relationship(self):
        return True



# ==============================================================================
#                                    STRUCTURE
# ==============================================================================

class Adjacency(object):
    """ An adjacency defines a constraint that we impose between a relation and a
    node. It imposes :
    - at the database level, unique-IN and unique-OUT constraints
    - at the application level, specifications on the type of node that a given
    relationship connects.
    """

    def __init__(self, node, relationship, nullable=None, unique=False, direction=None):
        """ Defines the constraints to apply on an adjacency.

        :param node: The node model that is connected.
        :type node: graphalchemy.blueprints.schema.Node
        :param relationship: The relationship model that connects.
        :type relationship: graphalchemy.blueprints.schema.Relationship
        :param unique: Whether the given node can be connected to multiple instances
        of the relationship.
        :type unique: bool
        :param nullable: Whether the given node can be connected to no instance of the
        relationship.
        :type nullable: bool
        :param direction: Whether the relation is IN-bound, or OUT-bound.
        :type direction: const
        """
        self.node = node
        self.relationship = relationship
        self.direction = direction
        self.unique = unique
        self.nullable = nullable



class Property(object):
    """ A property specifies how a property is constrained, and how it is mapped
    to the database. A property can apply to a node as well as a relationship.

    It imposes :
    - a validation on the application side (notably type validation and nullable
    verification)
    - a conversion to the appropriate datatype for database persistence

    It enables :
    - a flexible property mapping (prefixing, property name conversion)
    - indexing on a per-property and per-model basis
    - primaryKey definition for edges
    """

    def __init__(self, name_py, type_, nullable=None, unique=False, index=None, primaryKey=False, group=None, prefix=False, name_db=None):
        """ Defines the constraints to apply on a property.

        :param name_py: The name of the property in the Python objects
        :type name_py: str
        :param type_: The python type, that will be automatically converted to
        a corresponding datatype in the database.
        :type type_: graphalchemy.blueprints.types.Type
        :param nullable: Whether the property can be None.
        :type nullable: bool
        :param unique: Whether the property value is unique in the entire graph.
        This is enforced as a unique-IN constraint in the graph type definition.
        :type unique: bool
        :param index: Which index to use to index the property. If True is
        provided, the default index will be used. Not that this is enforced at
        the database-level, not at the model level, so if this property is used
        in multiple models, it will be indexed on the same index. The Migration
        tool detects such conflicts, and you can use the prefix property to add
        the model name to the node.
        :type index: bool
        :param primaryKey: Whether the property must be used as a primary key
        to index relations.
        :type primaryKey: bool
        :param group: The name of the group to save this relation in.
        :type group: str
        :param prefix: Whether this property must be prefixed by the model name.
        This is typically usefull for indexing purposes, when the property name
        conflicts with other models.
        :type prefix: bool
        :param name_db: The name of the property in the database. Defaults to
        the name of the property in Python.
        """

        self.model = None

        self.name_py = name_py
        self.prefix = prefix
        if name_db is None:
            name_db = name_py
        self.name_db = name_db

        self.type = type_
        self.nullable = nullable

        self.unique_graph = unique
        if index is True:
            index = 'standard'
        if isinstance(self.type, List) \
        or isinstance(self.type, Dict):
            self.unique_node = True
        else:
            self.unique_node = False

        self.index = index

        self.group = group
        self.primaryKey = primaryKey


    def to_py(self, value):
        """ Casts a database value to its correct type in Python, after being
        retrieved from the database for instance.

        :param value: The value to cast.
        :type value: mixed
        :returns: The casted value.
        :type: mixed
        """
        return self.type.to_py(value)


    def to_db(self, value):
        """ Casts a python value to its correct type in the database, before
        being persisted in the database for instance.

        :param value: The value to cast.
        :type value: mixed
        :returns: The casted value.
        :type: mixed
        """
        return self.type.to_db(value)


    def validate(self, value):
        """ Validates a value given the property specifications. Returns False
        and a list of errors if it fails.

        :param value: The value to validate.
        :type value: mixed
        :returns: A boolean and a list of potential errors.
        :rtype: bool, list
        """
        if self.nullable == False \
        and value is None:
            return False, [u'Property is not nullable.']
        return self.type.validate(value)


    def __repr__(self):
        """ Prints a readable representation of the property.

        :rtype: str
        """
        return '<'+str(self.model)+'.'+self.name_py+'('+str(self.type)+')>'



# ==============================================================================
#                                    SERVICES
# ==============================================================================

class MetaData(object):
    """ Holds a map of all available metadata of all mapped models.
    """

    def __init__(self, bind=None, schema=None):
        self._nodes = {}
        self._relationships = {}
        self.schema = schema
        self.bind = bind

    def __repr__(self):
        return 'MetaData(bind=%r)' % self.bind


    def __contains__(self, table_or_key):
        if not isinstance(table_or_key, util.string_types):
            table_or_key = table_or_key.key
        return table_or_key in self.tables

    def for_object(self, obj):
        class_ = obj.__class__
        return self.for_class(class_)

    def for_class(self, class_):
        if class_ in self._nodes:
            return self._nodes[class_]
        if class_ in self._relationships:
            return self._relationships[class_]
        raise Exception('Unmapped class.')

    def for_model(self, model):
        for class_, node_model in self._nodes:
            if model is node_model:
                return class_
        for class_, relationship_model in self._relationships:
            if model is relationship_model:
                return class_
        raise Exception('Unmapped model.')

    def bind_node(self, class_, model):
        if not model.is_node():
            raise Exception('Bound model is not a node !')
        self._nodes[class_] = model
        return self

    def bind_relationship(self, class_, model):
        if not model.is_relationship():
            raise Exception('Bound model is not a relationship !')
        self._relationships[class_] = model
        return self

    def is_node(self, obj):
        return obj.__class__ in self._nodes

    def is_relationship(self, obj):
        return obj.__class__ in self._relationships

    def is_bind(self, obj):
        return self.is_node(obj) or self.is_relationship(obj)



class Validator(object):
    """ Validates each property value of the given object against its specifications.

    Example use :
    >>> ok, errors = self.validator.run(obj)
    True, {}
    """

    def __init__(self, metadata_map, logger=None):
        """ Initializes the validator with a specific metadata map.

        :param metadata_map: The metadata map to validate objects agains.
        :type metadata_map: graphalchemy.blueprints.schema.MetaData
        :param logger: An optionnal logger.
        :type logger: logging.Logger
        """
        self.metadata_map = metadata_map
        self.logger = logger


    def run(self, obj):
        """ Validates an object against its specification.

        :param obj: The object to validate.
        :type obj: graphalchemy.blueprints.schema.Model
        :returns: A boolean stating if the validation was successfull, and the
        eventual list of errors.
        :rtype: boolean, dict<string, list>
        """
        metadata = self.metadata_map.for_object(obj)
        all_errors = {}
        ok = True
        for property in metadata.properties.values():
            python_value = getattr(obj, property.name_py)
            _ok, errors = property.validate(python_value)
            if _ok:
                self._log('  Property '+str(property)+' is valid')
            else:
                all_errors[property.name_py] = errors
                ok = False
                self._log('  Property '+str(property)+' is invalid : '+" ".join(errors))
        return ok, all_errors


    def _log(self, message, level=10):
        """ Thin wrapper for logging purposes.

        :param message: The message to log.
        :type message: str
        :param level: The level of the log.
        :type level: int
        :returns: This object itself.
        :rtype: graphalchemy.blueprints.schema.Validator
        """
        if self.logger is not None:
            self.logger.log(level, message)
        return self


class MigrationGenerator(object):
    """ Generates the groovy schema declaration from the current metadata.
    """

    def __init__(self, metadata_map, logger=None):
        """ Initializes the migration generator from :

        :param metadata_map: The metadata holder.
        :type metadata_map: graphalchemy.blueprints.schema.MetaData
        :param logger: An optionnal logger.
        :type logger: logging.Logger
        """
        self.metadata_map = metadata_map
        self.logger = logger

        self._queries = []
        self._properties = {}
        self._labels = {}
        self._groups = {}


    def run(self):
        """ Generates all queries.

        :returns: This object itself.
        :rtype: graphalchemy.blueprints.schema.MigrationGenerator
        """
        for node in self.metadata_map._nodes.values():
            self.run_node(node)
        for relationship in self.metadata_map._relationships.values():
            self.run_relationship(relationship)
        for i, name in enumerate(self._groups.keys()):
            self.make_group(name, i + 2) # Indexing starts at 2
        return self


    def run_node(self, node):
        """ Generates all queries for a given node model.

        :param node: The node to generate the label from.
        :type node: graphalchemy.blueprints.schema.Node
        :returns: This object itself.
        :rtype: graphalchemy.blueprints.schema.MigrationGenerator
        """
        for prop in node.properties.values():
            self.make_property_key(node, prop)
        return self


    def run_relationship(self, relationship):
        """ Generates all queries for a given relationship model.

        :param relationship: The relationship to generate the label from.
        :type relationship: graphalchemy.blueprints.schema.Relationship
        :returns: This object itself.
        :rtype: graphalchemy.blueprints.schema.MigrationGenerator
        """
        for prop in relationship.properties.values():
            self.make_property_key(relationship, prop)
        self.make_edge_label(relationship)
        return self


    def make_edge_label(self, relationship):
        """ Creates the query for an edge label.

        :param relationship: The relationship to generate the label from.
        :type relationship: graphalchemy.blueprints.schema.Relationship
        :returns: This object itself.
        :rtype: graphalchemy.blueprints.schema.MigrationGenerator
        """
        query = 'graph.makeType()'
        query += '.name("'+relationship.model_name+'")'
        # query += '.indexed('+'Edge.class'+')'
        # query += '.unique(Direction.BOTH).makePropertyKey()'

        # primaryKey
        pks = [for prop in relationship.properties.values() if prop.primaryKey]
        if len(pks) > 1:
            raise Exception('More than one private key was defined.')
        if len(pks) == 1
            query += '.primaryKey('+pks[0].name_db+')'

        # Signature
        # @todo

        # Direction
        if relationship.directed:
            query += '.directed()'
        else:
            query += '.undirected()'

        query += '.makeEdgeLabel()'
        query += ';'
        self._push_label(relationship.model_name, query)
        return self


    def make_property_key(self, model, property):
        """ Creates the query for a property key.

        :param model: The model to generate the property from.
        :type model: graphalchemy.blueprints.schema.Model
        :param property: The property to create.
        :type property: graphalchemy.blueprints.schema.Property
        :returns: This object itself.
        :rtype: graphalchemy.blueprints.schema.MigrationGenerator
        """
        query = 'graph.makeType()'

        # Groups
        if property.group is not None:
            query += '.group("'+property.group+'")'
            self._push_group(property.group, None)

        # Name
        query += '.name("'+property.name_db+'")'

        # Type
        query += '.dataType('+property.type.name_db+')'

        # Indexing
        if property.index is not None:
            query += '.indexed("' + property.index + '", ' + ('Vertex.class' if model.is_node() else 'Edge.class')+')'

        # Uniqueness
        if property.unique_graph and not property.unique_node:
            query += '.unique(Direction.BOTH)'
        else:
            if property.unique_graph:
                query += '.unique(Direction.IN)'
            if not property.unique_node:
                query += '.unique(Direction.OUT)'

        # Type
        query += '.makePropertyKey()'
        query += ';'
        self._push_property(property.name_db, query)
        return self


    def make_group(self, name, id):
        """ Creates the query for a group.

        :param name_db: The name of the property in the database.
        :type name_db: str
        :param query: The corresponding query.
        :type query: str
        :returns: This object itself.
        :rtype: graphalchemy.blueprints.schema.MigrationGenerator
        """
        query = 'TypeGroup ' + name + ' = TypeGroup.of(' + str(id) + ',"' + name + '");'
        self._queries.append(query)
        return self


    def _push_property(self, name_db, query):
        """ Adds a property to the creation list. This is usefull to detect and
        resolve conflicts at model definition runtime.

        :param name_db: The name of the property in the database.
        :type name_db: str
        :param query: The corresponding query.
        :type query: str
        :returns: This object itself.
        :rtype: graphalchemy.blueprints.schema.MigrationGenerator
        """
        if name_db in self._properties:
            raise Exception('This property is already used : '+str(name_db))
        self._properties[name_db] = query
        self._queries.append(query)
        return self


    def _push_label(self, name_db, query):
        """ Adds a label to the creation list. This is usefull to detect and
        resolve conflicts at model definition runtime.

        :param name_db: The name of the label in the database.
        :type name_db: str
        :param query: The corresponding query.
        :type query: str
        :returns: This object itself.
        :rtype: graphalchemy.blueprints.schema.MigrationGenerator
        """
        if name_db in self._labels:
            raise Exception('This label is already used : '+str(name_db))
        self._labels[name_db] = query
        self._queries.append(query)
        return self


    def _push_group(self, name_db, query):
        """ Adds a group to the creation list. This is usefull to detect and
        resolve conflicts at model definition runtime.

        :param name_db: The name of the property in the database.
        :type name_db: str
        :returns: This object itself.
        :rtype: graphalchemy.blueprints.schema.MigrationGenerator
        """
        self._groups[name_db] = query
        return self


    def __str__(self):
        """ Returns a readable version of the required queries.

        :rtype: str
        """
        return "\n".join(self._queries)

