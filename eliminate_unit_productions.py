"""
The purpose of the file is to provide a way of eliminating unit productions
with a method based on a directed graph approach
"""

import networkx as nx
from networkx import NetworkXNoPath
from collections import defaultdict

def build_graph(unit_productions, terminals):
    """
    Function accepts a dictionary of unit productions in a form:
        {LHS, [RHS1, ...], ...}
    """

    # initialize a directed graph
    unit_productions_graph = nx.DiGraph()

    for LHS in unit_productions.keys():
        unit_productions_graph.add_node(LHS, type="non_terminal")
        for RHS in unit_productions[LHS]:
            unit_productions_graph.add_node(RHS, type="non_terminal")
            # directed edge from LHS to RHS displaying a rule LHS -> RHS
            unit_productions_graph.add_edge(LHS, RHS)
            try:
                for terminal in terminals[RHS]:
                    unit_productions_graph.add_node(terminal, type="terminal")
                    unit_productions_graph.add_edge(RHS, terminal)
            except TypeError:
                print("Key not found")

    # the root is the node that has no incoming edges; in syntax terminology it
    # is the head
    # In unit production elimination we care about finding all the paths that
    # can take us from the root to a terminal node
    # Once a path is found we can use as follows:
    #   1. Get the first and the second to last element of the path (root and
    #   the last non-terminal respectively)
    #   In the `terminals` dictionary we must swap the key: the current one (
    #   the last non-terminal is switched to the root)
    #   2. The remaining nodes must be deleted from the `rules` dictionary

    # TODO: Zaimplementować resztę kodu z notebooku
