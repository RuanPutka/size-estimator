from src.directed_acyclic_graph.directed_acyclic_graph import DirectedAcyclicGraph as DAG
import src.code_utils as code_utils


def rename_verticies(dag, vertices_dictionary):
    """

    Parameters
    ----------
    dag : DirectedAcyclicGraph object.
    vertices_dictionary : Python dictionary.
        Keys are from original name to desired name.

    Returns
    -------
    Renamed DAG.

    """

    renamed_dag = DAG()
    for k, v in dag.items():
        new_key = (vertices_dictionary[k[0]], vertices_dictionary[k[1]])
        renamed_dag.add_vertices(new_key, v)

    return renamed_dag


def rename_edges(dag, edges_dictionary):
    """

    Parameters
    ----------
    dag : DirectedAcyclicGraph object.
    edges_dictionary : Python dictionary.
        Keys are vertices pairs and values are the new edges names.

    Returns
    -------
    Renamed DAG.

    """

    renamed_dag = DAG()
    for k, v in dag.items():
        new_edge = edges_dictionary.get(k)
        renamed_dag.add_vertices(k, new_edge)

    return renamed_dag


def redirect_dag_to_new_sink(dag, new_sink):
    redirected_dag = dag.copy()
    old_sink_vertex = redirected_dag.get_sink_vertices()[0]
    from_vertice = new_sink
    while (from_vertice != old_sink_vertex):
        connected_vertices = dag.get_vertices_coming_from(from_vertice)
        if len(connected_vertices) > 0:
            connected_vertice = connected_vertices
            new_edge = round(1 / redirected_dag[connected_vertice], 2)

            redirected_dag.delete_entry(connected_vertice)
            redirected_dag.add_vertices(code_utils.swap(connected_vertice), new_edge)

    return redirected_dag


def normalize_dag_edges(dag, offset=0, scaling_factor=1):
    """
    Apply Min-Max scaling on DAG edges.

    Parameters
    ----------
    dag : DAG object.

    Returns
    -------
    DAG with normalized edges.

    """
    normalized_dag = DAG()
    highest_value = dag.get_highest_value()
    lowest_value = dag.get_lowest_value()
    for k, v in dag.items():
        normalized_edge = (v-lowest_value)/(highest_value-lowest_value)
        new_edge = normalized_edge*scaling_factor + offset
        normalized_dag.add_vertices(k, new_edge)

    return normalized_dag



    