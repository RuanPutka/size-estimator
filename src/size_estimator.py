import sys, os

cwd = os.getcwd()
sys.path.append(cwd.replace("/src", ""))

import pandas as pd
import numpy as np

import src.code_utils as code_utils
from src.directed_acyclic_graph.directed_acyclic_graph import DirectedAcyclicGraph as DAG

def create_size_relationships_dag(arr, verbose=True):
    dag = DAG()
    options = code_utils.get_number_of_intersections(arr)
    point_of_sales = list(range(arr.shape[0]))

    first_pair = options.get_key_with_highest_value()
    first_edge = round(code_utils.calculate_rows_ratio(arr, first_pair), 5)
    options.delete_entry(first_pair)
    dag.add_vertices(first_pair, first_edge)

    from_vertices = [first_pair[0]]
    to_vertices = [first_pair[1]]
    unprocessed_vertices = [v for v, _ in enumerate(point_of_sales) if v not in from_vertices]

    if verbose == True:
        print("From vertices: {0}".format(from_vertices))
        print("To vertices: {0}".format(to_vertices))
        print(50*'=')
    for _ in range(len(point_of_sales) - 2):
        last_pair = dag.get_last_added_key()
        next_pair = options.get_key_with_highest_value(having_any=list(last_pair),
                                                        without=from_vertices)
        
        while not next_pair:
            options.delete_entry(next_pair)
            unprocessed_vertices = [v for v, _ in enumerate(point_of_sales) if v
                                    not in from_vertices and v not in to_vertices]
            print("unprocessed_vertices ", unprocessed_vertices)
            random_vertex = np.random.choice(unprocessed_vertices)
            print("options ", {k: v for k, v in options.items() if k[0] == random_vertex \
                                               or k[1] == random_vertex})
            next_pair = options.get_key_with_highest_value(having_any=[random_vertex])
            if (next_pair[0] in from_vertices) and (next_pair[1] in from_vertices):
                next_pair = None
            elif (next_pair[0] in from_vertices):
                next_pair = code_utils.swap(next_pair)
                if (next_pair[0] in to_vertices):
                    next_pair = None

        next_edge = round(code_utils.calculate_rows_ratio(arr, next_pair), 5)
        from_vertices.append(next_pair[0])
        to_vertices.append(next_pair[1])
        options.delete_entry(next_pair)
        dag.add_vertices(next_pair, next_edge)
        if verbose == True:
            print("From vertices: {0}".format(from_vertices))
            print("To vertices: {0}".format(to_vertices))
            print("{0}: {1}".format(next_pair, next_edge))
            print(50*'=')

    return dag


if __name__ == "__main__":
    from src.graph_utils.reducers import multiplication_reductor
    from src.graph_utils.plotters import plot_dag, plot_two_dimensional_dag
    from src.graph_utils.utils import rename_verticies, rename_edges,redirect_dag_to_new_sink, normalize_dag_edges 


    df = pd.DataFrame(np.random.normal(loc=60, scale=15, size=(100, 8)))
    df = df.mask(np.random.random(df.shape) < .6)
    arr = df.T.values

    dag = create_size_relationships_dag(arr)
    options_dag = code_utils.get_number_of_intersections(arr)
    options_dag_normalized = normalize_dag_edges(options_dag, offset=1, scaling_factor=6)
    plot_two_dimensional_dag(dag, options_dag_normalized)
    plot_dag(rename_edges(dag, options_dag))
    
    minimal_dag = multiplication_reductor(dag)
    plot_dag(minimal_dag)

    redirected_minimal_dag = multiplication_reductor(redirect_dag_to_new_sink(dag, 10))
    plot_dag(redirected_minimal_dag)

