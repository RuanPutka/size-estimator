from src.directed_acyclic_graph.directed_acyclic_graph import DirectedAcyclicGraph as DAG
import numpy as np

def multiplication_reductor(dag):
    reduced_dag = DAG()    
    vertex_set = dag.get_vertex_set() 
    sink_vertex = dag.get_sink_vertices()[0]
    source_vertices = [v for v in vertex_set if v != sink_vertex]
    for vertex in source_vertices:
        from_vertex = vertex
        factor = 1
        while (from_vertex != sink_vertex):
            connected_vertices = dag.get_vertices_coming_from(from_vertex)
            if len(connected_vertices) > 0:
                connected_vertice = connected_vertices[0]
                factor *= dag[(from_vertex, connected_vertice)]
                from_vertex = connected_vertice
                
        reduced_dag.add_vertices((vertex, sink_vertex), factor)
     
    return reduced_dag

