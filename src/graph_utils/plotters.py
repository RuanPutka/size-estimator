import networkx as nx
import matplotlib.pyplot as plt
import pylab


def plot_dag(dag):
    G = nx.DiGraph()
    for key, value in dag.items():
        key = (str(key[0]), str(key[1]))
        G.add_edges_from([key], weight=value)


    edge_labels=dict([((u,v,), d['weight'])
                     for u,v,d in G.edges(data=True)])
    values = [0.45 for node in G.nodes()]

    plt.figure(figsize=[16, 10])
    pos=nx.spring_layout(G)
    nx.draw(G, pos, node_size=500, alpha=0.75, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    pylab.show()


def _min_max_scale(arr):
    max_value = max(arr)
    min_value = min(arr)

    for value in arr:
        yield (value - min_value)/(max_value - min_value)


def plot_two_dimensional_dag(first_dimension_dag, second_dimension_dag):
    """
    Plot DAG structure according to first_dimension_dag DAG object. The second
    dimensions (line width) comes from the second_dimension_dag object and is
    only exposed in edges that are present in both DAGs.
    

    Parameters
    ----------
    first_dimension_dag : DAG object.
    second_dimension_dag : DAG object.

    Returns
    -------
    None.

    """
    G = nx.DiGraph()
    width_list = []
    for key, value in first_dimension_dag.items():
        width_list.append(second_dimension_dag.get(key))
        key = (str(key[0]), str(key[1]))
        G.add_edges_from([key], weight=value)       

    edge_labels=dict([((u,v,), d['weight'])
                     for u,v,d in G.edges(data=True)])
    values = [0.45 for node in G.nodes()]

    plt.figure(figsize=[16, 10])
    pos=nx.spring_layout(G)
    nx.draw(G, pos, node_size=500, alpha=1, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    nx.draw_networkx_edges(G, pos, width=width_list)

    pylab.show()