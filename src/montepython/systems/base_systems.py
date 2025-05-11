import networkx as nx

class UndirectedComplexNetwork():

    def __init__(self, elements, adjacency_matrix):

        self.graph = nx.from_numpy_array(adjacency_matrix)
        nx.set_node_attributes(self.graph, {i:attr for i, attr in enumerate(elements)}, name="state")

        self.N_NODES = len(elements)
        self._hamiltonian = None
        self._transform_state = None


    @property
    def hamiltonian(self):
        return self._hamiltonian
    
    @hamiltonian.setter
    def hamiltonian(self, new_hamiltonian):
        assert callable(new_hamiltonian), "The hamiltonian should be a callable function"
        self._hamiltonian = new_hamiltonian

    @hamiltonian.deleter
    def hamiltonian(self):
        del self._hamiltonian

    @property
    def transform_state(self):
        return self._transform_state
    
    @transform_state.setter
    def transform_state(self, new_transform):
        assert callable(new_transform), "The state transformation should be a callable function"
        self._transform_state = new_transform
    
    @transform_state.deleter
    def transform_state(self):
        del self._transform_state


    def get_energy(self):

        total_energy = 0

        for node, state in self.graph.nodes(data="state"):

            neighbors = self.graph.neighbors(node)
            neighbors_states = tuple((self.graph.nodes[n]["state"] for n in neighbors))

            total_energy += self.hamiltonian(state, neighbors_states)

        return total_energy
    

    def delta_E(self, node_to_change, new_state):

        current_state = self.graph.nodes[node_to_change]["state"]
        neighbors_states = tuple((self.graph.nodes[n]["state"] for n in self.graph.neighbors(node_to_change)))

        return (self.hamiltonian(new_state, neighbors_states) - self.hamiltonian(current_state, neighbors_states)) 

        

