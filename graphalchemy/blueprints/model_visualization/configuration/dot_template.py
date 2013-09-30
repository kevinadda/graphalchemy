#! /usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
#                            GRAPHVIZ TEMPLATE
# =============================================================================

# Graph parameters can be modified here.

_template = '''
digraph G
{

// ============================================================================
//                        GRAPH STYLE CONFIG
// ============================================================================

        // Title
        labelloc="t";
        label="%(TITLE)s";

        // Graph config
        graph [ fontname = "Helvetica",
                fontsize = 37,
        //size = "500,500",
                splines=true,
                overlap=true,
                ratio=.4
               ];

        // Node config
        node [shape = oval,
              style=filled,
              fixedsize=true,
              fontname = "Helvetica",
              fontsize=21,
              width=6,
              height=5
              ];

        // Edge config
        edge [ color="#142b30",
               arrowhead="vee",
               fontname = "Helvetica",
               fontsize=25,
               arrowsize=1.95,
               penwidth=2,
               labelangle=30
             ];

// ============================================================================
//                        ENTITIES INSTANTIATIONS
// ============================================================================

// ----------------------------------------------------------------------------
//                                  Nodes
// ----------------------------------------------------------------------------

%(NODES)s

// ----------------------------------------------------------------------------
//                                  Relationships
// ----------------------------------------------------------------------------

%(RELATIONSHIPS)s

}

'''
