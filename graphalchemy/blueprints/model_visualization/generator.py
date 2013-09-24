#! /usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
#                                      IMPORTS
# =============================================================================

import itertools
from collections import Iterable


# =============================================================================
#                    VISUALIZATION GENERATOR ABSTRACT CLASS
# =============================================================================

class VisualizationGenerator(object):

    """ Parse a graphalchemy metadata object and generate a code formatted text
        toward model visualization.

        This abstract class does not implement output formatting methods.
        This class should be extended with implementation of formatting methods
        to be adapted to different visualization-wise programming languages.
    """

    def __init__(self, metadata_map, logger=None,
                 output_path=None):
        """ Creates a visualization generator.

            :param metadata_map: Implemented model metadata.
            :type metadata_map: graphalchemy.blueprints.schema.MetaData
            :param logger: An optionnal logger.
            :type logger: logging.Logger
            :param output_path: The path where the output should be written.
            :type output_path: str
        """
        self.metadata_map = metadata_map
        self.logger = logger

        self._nodes = []
        self._relationships = []
        self._properties = {}
        self._labels = {}
        self._groups = {}
        self.output_path = output_path
        self.graph_title = "graphalchemy - Data model diagram."

# -----------------------------------------------------------------------------
# Metadata parsing method
# -----------------------------------------------------------------------------

    def run(self):
        """ Iterates on node then relationship to generate visualization code.
        """
        # Iterates on nodes
        for node in self.metadata_map._nodes.values():
            self.run_node(node)
        # Iterates on relationships
        for relationship in self.metadata_map._relationships.values():
            self.run_relationship(relationship)

        # Generate output in a
        self.generate_output()
        return self

    def run_node(self, node):
        """ Process one node to feed self._nodes:

        :param node: The node object to be treated.
        :type node: graphalchemy.blueprints.schema.Node
        """
        name = str(node)
        properties = [prop.name_py for prop in node._properties.values()]
        node_dot_instance = self._generate_node_instance(name, properties)
        self._nodes.append(node_dot_instance)
        return

    def run_relationship(self, relationship):
        """ Process one relationship to feed self._relationships:

        :param relationship: A relationship object to be treated.
        :type node: graphalchemy.blueprints.schema.Relationship
        """
        # List of properties
        properties = [prop.name_py
                      for prop in relationship._properties.values()]
        _adjacencies = relationship._adjacencies.values()
        # List of in-directed adjacencies
        _ins = [adjacency for adjacency in _adjacencies
                if adjacency.direction is 'in']
        # List of in-directed adjacencies
        _outs = [adjacency for adjacency in _adjacencies
                 if adjacency.direction is 'out']
        # List of adjacencies couples defining a relationship
        _bindings = [{'in': _in, 'out': _out}
                     for _in, _out in itertools.product(_ins, _outs)
                     if _in.relationship == _out.relationship]

        for _binding in _bindings:
            # Create relationship between those nodes
            relationship_dot_instance = self \
                ._generate_relationship_instance(_binding, properties)
            self._relationships.append(relationship_dot_instance)
        return

# -----------------------------------------------------------------------------
# Output retrieval methods
# -----------------------------------------------------------------------------

    def write_output(self):
        """ Write formatted output in a file.
        """
        with open(self.output_path, 'w') as f:
            f.write(self._output)
        return

    def get_output(self):
        """ Returns output as a string.

            :returns: formatted output.
            :rtype: str
        """
        return self._output

    def set_output_path(self, path):
        """ Set output_path.

            :param output_path: the output file destination.
            :type output_path: str
        """
        self.output_path = path
        return self

    def set_graph_title(self, title):
        """ Set graph title.

            :param title: the title of the outputted graph.
            :type title: str
        """
        self.graph_title = title
        return self

# -----------------------------------------------------------------------------
# Visualization language dependent methods
# -----------------------------------------------------------------------------

    def _generate_node_instance(self, name, properties):
        """ Generate output format for node instantiation based on
            its name and properties:

        :param name: The name of the model defining the node.
        :type name: str
        :param properties: The list of node properties.
        :type properties: list<str>
        :returns: The dot code instantiation of the node.
        :rtype: str
        """
        raise NotImplementedError(("Output formatting method are not "
                                   "implemented in %s") % str(self.__class__))

    def _generate_relationship_instance(self, binding, properties):
        """ Generate output format for relationship instantiation based on
            its adjacencies and properties:

        :param binding: A dictionary with keys ('in', 'out') which defines a
                        pair of adjacencies defining a permitted relationship
                        neighborhood.
        :type binding: dict
        :param properties: The list of relationship properties.
        :type name: list<str>
        :returns: The dot code instantiation of the relationship.
        :rtype: str
        """
        raise NotImplementedError(("Output formatting method are not "
                                   "implemented in %s") % str(self.__class__))

    def _get_formatted_property_list(self, property_list, limit):
        """ Generate formatted property lists for a node or a relationship.

        :param property_list: The list of node/relationship properties.
        :type property_list: list<str>
        :param limit: The maximum number of properties per node/relationship
                      to fit visualization requirements.
        :type limit: int
        :returns: The formatted limited list of properties.
        :rtype: str
        """
        raise NotImplementedError(("Output formatting method are not "
                                   "implemented in %s") % str(self.__class__))

    def generate_output(self):
        """ Generate output from _nodes and _relationships attributes
            into self.output.
        """
        raise NotImplementedError(("Output formatting method are not "
                                   "implemented in %s") % str(self.__class__))


# =============================================================================
#                      GRAPHVIZ VISUALIZATION GENERATOR
# =============================================================================

class GraphvizVisualizationGenerator(VisualizationGenerator):

    def __init__(self, metadata_map, logger=None, output_path=None):
        """ Creates a Graphiz visualization generator.

            Example of use:

            python:
            > visualizer = GraphvizVisualizationGenerator(myMetadata)
            > visualizer.set_output_path('/tmp/viz.dot').run().write_output()

            shell:
            $ dot -Tjpg /tmp/viz.dot -o /tmp/viz.jpeg
            $ eog /tmp/viz.jpg

            :param metadata_map: Implemented model metadata.
            :type metadata_map: graphalchemy.blueprints.schema.MetaData
            :param logger: An optionnal logger.
            :type logger: logging.Logger
            :param output_path: The path where the output should be written.
            :type output_path: str
        """
        super(GraphvizVisualizationGenerator, self).__init__(metadata_map,
                                                             logger,
                                                             output_path)
        # Load colors
        self.load_colors()

        # Load template
        from configuration.dot_template import _template
        self._template = _template

# -----------------------------------------------------------------------------
# Visualization language dependent methods
# -----------------------------------------------------------------------------

    def _generate_node_instance(self, name, properties):
        """ Generate dot code node instantiation based on its
            name and properties:
        """
        property_labels = self._get_formatted_property_list(properties)

        return " ".join(["node_" + name,
                         "[",
                         "label = ",
                         '"[%s] \\n\\n\\' % name,
                         '%s",\n' % property_labels,
                         'color = "%s" ' % self._set_color(name),
                         "];"])

    def _generate_relationship_instance(self, binding, properties):
        """ Generate dot code relationship instantiation based on its
            adjacencies and properties:
        """
        property_labels = self._get_formatted_property_list(properties)
        return " ".join(['"node_%s"' % str(binding['out'].node),
                         '->',
                         '"node_%s"' % str(binding['in'].node),
                         "[",
                         'label = "%s \\n\ %s "' % (binding['out'].relationship,
                                                    property_labels),
                         'taillabel="%s"' % ('1\t'
                                             if binding['out'].unique
                                             else 'N\t'),
                         'headlabel="%s"' % ('\t1'
                                             if binding['in'].unique
                                             else '\tN'),
                         "];"])

    def _get_formatted_property_list(self, property_list, limit=10):
        """ limit should be set to fit node size.
        """
        if len(property_list) <= limit:
            return "\\n\\\n".join(["- %s" % prop for prop in property_list])
        return self._get_formatted_property_list(property_list[:limit - 1] + ['...'])

    def generate_output(self):
        """ Generate dot code formatted output.
        """
        node_instantiations = "\n\n".join([inst for inst in self._nodes])
        relationships_instantiations = "\n\n".join([inst
                                                    for inst
                                                    in self._relationships])

        self._output = self._template \
            % {'TITLE': self.graph_title,
               'NODES': node_instantiations,
               'RELATIONSHIPS': relationships_instantiations}
        return

# -----------------------------------------------------------------------------
# Color generation
# -----------------------------------------------------------------------------

    def load_colors(self):
        """ Loads colors from color_settings configuration file.
            color_settings is by default a list of colors.
            color_settings can be a dictionary mapping node names to colors.

            :param color_settings: A list of colors, or a dictionary mapping
                                   node names (key) to colors (value).
            :type color_settings: list<color:str>
                                  or dict(node_name<str>: color<str>)
        """
        from configuration.color_settings import colors
        if isinstance(colors, list):
            self.color_generator = (it for it in colors)
        elif isinstance(colors, dict):
            self.color_generator = colors
        else:
            raise TypeError("%s does not handle type %s"
                            % (__name__, str(type(colors))))

    def _set_color(self, node_name=None):
        """ Generate node color from color_settings.

            :param node_name: the name of the node.
            :type node_name: str
            :returns: a Graphviz color.
            :rtype: str
        """
        if isinstance(self.color_generator, Iterable):
            return self.color_generator.next()
        else:
            return self.color_generator[node_color_key]


# =============================================================================
#                                 TEST
# =============================================================================

def main():
    from jerome.model.ogm.abstract import metadata

    vizgenerator = GraphvizVisualizationGenerator(metadata)
    vizgenerator.set_output_path('/tmp/model_visualization.dot') \
        .set_graph_title('Jerome core data model diagram') \
        .run().write_output()

    from subprocess import call
    call(["dot", "-Tjpg", "/tmp/model_visualization.dot",
          "-o", "/tmp/model_visualization.jpg"])
    call(["eog", "/tmp/model_visualization.jpg"])
    return


if __name__ == '__main__':
    main()
