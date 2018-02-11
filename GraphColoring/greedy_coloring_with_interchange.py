import itertools
def greedy_color(G, strategy=strategy_largest_first, interchange=False):
    """Color a graph using various strategies of greedy graph coloring.
    The strategies are described in [1]_.

    Attempts to color a graph using as few colors as possible, where no
    neighbours of a node can have same color as the node itself.

    Parameters
    ----------
    G : NetworkX graph

    strategy : function(G, colors)
       A function that provides the coloring strategy, by returning nodes
       in the ordering they should be colored. G is the graph, and colors
       is a dict of the currently assigned colors, keyed by nodes.

       You can pass your own ordering function, or use one of the built in:

       * strategy_largest_first
       * strategy_random_sequential
       * strategy_smallest_last
       * strategy_independent_set
       * strategy_connected_sequential_bfs
       * strategy_connected_sequential_dfs
       * strategy_connected_sequential
         (alias of strategy_connected_sequential_bfs)
       * strategy_saturation_largest_first (also known as DSATUR)

    interchange: bool
       Will use the color interchange algorithm described by [2]_ if set
       to true.

       Note that saturation largest first and independent set do not
       work with interchange. Furthermore, if you use interchange with
       your own strategy function, you cannot rely on the values in the
       colors argument.

    Returns
    -------
    A dictionary with keys representing nodes and values representing
    corresponding coloring.

    Examples
    --------
    >>> G = nx.cycle_graph(4)
    >>> d = nx.coloring.greedy_color(G, strategy=nx.coloring.strategy_largest_first)
    >>> d in [{0: 0, 1: 1, 2: 0, 3: 1}, {0: 1, 1: 0, 2: 1, 3: 0}]
    True

    References
    ----------
    .. [1] Adrian Kosowski, and Krzysztof Manuszewski,
       Classical Coloring of Graphs, Graph Colorings, 2-19, 2004.
       ISBN 0-8218-3458-4.
    .. [2] Maciej M. Syslo, Marsingh Deo, Janusz S. Kowalik,
       Discrete Optimization Algorithms with Pascal Programs, 415-424, 1983.
       ISBN 0-486-45353-7.
    """
    colors = {}  # dictionary to keep track of the colors of the nodes

    if len(G):
        if interchange and (
                strategy == strategy_independent_set or
                strategy == strategy_saturation_largest_first):
            raise nx.NetworkXPointlessConcept(
                'Interchange is not applicable for GIS and SLF')

        nodes = strategy(G, colors)

        if nodes:
            if interchange:
                return (_interchange
                        .greedy_coloring_with_interchange(G, nodes))
            else:
                for node in nodes:
                     # set to keep track of colors of neighbours
                    neighbour_colors = set()

                    for neighbour in G.neighbors_iter(node):
                        if neighbour in colors:
                            neighbour_colors.add(colors[neighbour])

                    for color in itertools.count():
                        if color not in neighbour_colors:
                            break

                     # assign the node the newly found color
                    colors[node] = color

    return colors
