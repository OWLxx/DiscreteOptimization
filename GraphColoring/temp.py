# -*- coding: utf-8 -*-
"""
Greedy graph coloring using various strategies.
"""
#    Copyright (C) 2014 by
#    Christian Olsson <chro@itu.dk>
#    Jan Aagaard Meier <jmei@itu.dk>
#    Henrik Haugbølle <hhau@itu.dk>
#    All rights reserved.
#    BSD license.
import networkx as nx
import random
import itertools
from . import greedy_coloring_with_interchange as _interchange

__author__ = "\n".join(["Christian Olsson <chro@itu.dk>",
                        "Jan Aagaard Meier <jmei@itu.dk>",
                        "Henrik Haugbølle <hhau@itu.dk>"])
__all__ = [
    'greedy_color',
    'strategy_largest_first',
    'strategy_random_sequential',
    'strategy_smallest_last',
    'strategy_independent_set',
    'strategy_connected_sequential',
    'strategy_connected_sequential_dfs',
    'strategy_connected_sequential_bfs',
    'strategy_saturation_largest_first'
]


def min_degree_node(G):
    return min(G, key=G.degree)


def max_degree_node(G):
    return max(G, key=G.degree)


def strategy_largest_first(G, colors):
    """
    Largest first (lf) ordering. Ordering the nodes by largest degree
    first.
    """
    nodes = G.nodes()
    nodes.sort(key=lambda node: -G.degree(node))

    return nodes


def strategy_random_sequential(G, colors):
    """
    Random sequential (RS) ordering. Scrambles nodes into random ordering.
    """
    nodes = G.nodes()
    random.shuffle(nodes)

    return nodes


def strategy_smallest_last(G, colors):
    """
    Smallest last (sl). Picking the node with smallest degree first,
    subtracting it from the graph, and starting over with the new smallest
    degree node. When the graph is empty, the reverse ordering of the one
    built is returned.
    """
    len_g = len(G)
    available_g = G.copy()
    nodes = [None] * len_g

    for i in range(len_g):
        node = min_degree_node(available_g)

        available_g.remove_node(node)
        nodes[len_g - i - 1] = node

    return nodes


def strategy_independent_set(G, colors):
    """
    Greedy independent set ordering (GIS). Generates a maximal independent
    set of nodes, and assigns color C to all nodes in this set. This set
    of nodes is now removed from the graph, and the algorithm runs again.
    """
    len_g = len(G)
    no_colored = 0
    k = 0

    uncolored_g = G.copy()
    while no_colored < len_g:  # While there are uncolored nodes
        available_g = uncolored_g.copy()

        while len(available_g):  # While there are still nodes available
            node = min_degree_node(available_g)
            colors[node] = k  # assign color to values

            no_colored += 1
            uncolored_g.remove_node(node)
            # Remove node and its neighbors from available
            available_g.remove_nodes_from(available_g.neighbors(node) + [node])
        k += 1
    return None


def strategy_connected_sequential_bfs(G, colors):
    """
    Connected sequential ordering (CS). Yield nodes in such an order, that
    each node, except the first one, has at least one neighbour in the
    preceeding sequence. The sequence is generated using BFS)
    """
    return strategy_connected_sequential(G, colors, 'bfs')


def strategy_connected_sequential_dfs(G, colors):
    """
    Connected sequential ordering (CS). Yield nodes in such an order, that
    each node, except the first one, has at least one neighbour in the
    preceeding sequence. The sequence is generated using DFS)
    """
    return strategy_connected_sequential(G, colors, 'dfs')


def strategy_connected_sequential(G, colors, traversal='bfs'):
    """
    Connected sequential ordering (CS). Yield nodes in such an order, that
    each node, except the first one, has at least one neighbour in the
    preceeding sequence. The sequence can be generated using both BFS and
    DFS search (using the strategy_connected_sequential_bfs and
    strategy_connected_sequential_dfs method). The default is bfs.
    """
    for component_graph in nx.connected_component_subgraphs(G):
        source = component_graph.nodes()[0]

        yield source  # Pick the first node as source

        if traversal == 'bfs':
            tree = nx.bfs_edges(component_graph, source)
        elif traversal == 'dfs':
            tree = nx.dfs_edges(component_graph, source)
        else:
            raise nx.NetworkXError(
                'Please specify bfs or dfs for connected sequential ordering')

        for (_, end) in tree:
            # Then yield nodes in the order traversed by either BFS or DFS
            yield end


def strategy_saturation_largest_first(G, colors):
    """
    Saturation largest first (SLF). Also known as degree saturation (DSATUR).
    """
    len_g = len(G)
    no_colored = 0
    distinct_colors = {}

    for node in G.nodes_iter():
        distinct_colors[node] = set()

    while no_colored != len_g:
        if no_colored == 0:
             # When sat. for all nodes is 0, yield the node with highest degree
            no_colored += 1
            node = max_degree_node(G)
            yield node
            for neighbour in G.neighbors_iter(node):
                distinct_colors[neighbour].add(0)
        else:
            highest_saturation = -1
            highest_saturation_nodes = []

            for node, distinct in distinct_colors.items():
                if node not in colors:  # If the node is not already colored
                    saturation = len(distinct)
                    if saturation > highest_saturation:
                        highest_saturation = saturation
                        highest_saturation_nodes = [node]
                    elif saturation == highest_saturation:
                        highest_saturation_nodes.append(node)

            if len(highest_saturation_nodes) == 1:
                node = highest_saturation_nodes[0]
            else:
                # Return the node with highest degree
                max_degree = -1
                max_node = None

                for node in highest_saturation_nodes:
                    degree = G.degree(node)
                    if degree > max_degree:
                        max_node = node
                        max_degree = degree

                node = max_node

            no_colored += 1
            yield node
            color = colors[node]
            for neighbour in G.neighbors_iter(node):
                distinct_colors[neighbour].add(color)


