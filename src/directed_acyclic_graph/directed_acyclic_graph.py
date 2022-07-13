from src.directed_acyclic_graph.my_ordered_dict import MyOrderedDict
from src.directed_acyclic_graph._exceptions import CycleError

def _remove_from_list(list, blacklist):
    resulting_list = []
    for element in list:
        if element not in blacklist:
            resulting_list.append(element)
            
    return resulting_list
        
class DirectedAcyclicGraph(MyOrderedDict):
    """
    Parameters
    ----------
    keys: (vertice_a, vertice_b).
          The relationship is from A to B.

    values: edges.
    """

    def add_vertices(self, vertices, edge):
        self[vertices] = edge
        if self._has_cycle():
            self.delete_entry(vertices)
            raise CycleError()
            

    def undo(self):
        try:
            self.popitem(last=True)
        except KeyError:
            print("Can't because dictionary is empty.")
            
            
    def get_vertex_set(self):
        vertices = self.keys()
        vertex_set = []
        for vertex in vertices:
            vertex_set.append(vertex[0])
            vertex_set.append(vertex[1])

        return tuple(set(vertex_set))
    
    
    def get_vertices_arriving_at(self, end):
        vertices_arriving_at = []
        vertices = self.keys()
        for vertex_pair in vertices:
            to_vertex = vertex_pair[1]
            from_vertex = vertex_pair[0]
            if to_vertex == end:
                vertices_arriving_at.append(from_vertex)
                
        return vertices_arriving_at
    
    
    def get_vertices_coming_from(self, start):
        vertices_coming_from = []
        vertices = self.keys()
        for vertex_pair in vertices:
            from_vertex = vertex_pair[0]
            to_vertex = vertex_pair[1]
            if from_vertex == start:
                vertices_coming_from.append(to_vertex)
                
        return vertices_coming_from

    
    def get_sink_vertices(self):
        marked_vertices = []
        vertex_set = self.get_vertex_set()
        for vertex in vertex_set:
            source_vertices = self.get_vertices_coming_from(vertex)
            if source_vertices:
                marked_vertices.append(vertex)
            
        sink_vertices = [v for v in vertex_set if v not in marked_vertices]
        return sink_vertices 
    
    
    def _has_cycle(self):
        has_cycle = False
        never_visited = list(self.get_vertex_set())
        visiting = []
        totally_visited = []
        
        current_vertex = never_visited.pop()
        while not has_cycle and never_visited:
            visiting.append(current_vertex)
            vertices_coming_from = self.get_vertices_coming_from(current_vertex)
            possible_next_vertices = _remove_from_list(vertices_coming_from, totally_visited)
            if possible_next_vertices:
                # update next vertex going forward
                current_vertex = possible_next_vertices.pop()
                if current_vertex in visiting:
                    has_cycle = True
            else:
                totally_visited.append(visiting.pop())
                # backtracking
                if visiting:
                    current_vertex = visiting.pop()
                # choosing other vertex
                else:
                    current_vertex = never_visited.pop()
   
            never_visited = _remove_from_list(never_visited, [current_vertex])

        return has_cycle