import numpy as np
import networkx as nx
from itertools import product
from functools import lru_cache

class UndirectedComplexNetwork():

    def __init__(self, elements, adjacency_matrix):

        self.graph = nx.from_numpy_array(adjacency_matrix)
        nx.set_node_attributes(self.graph, {i:attr for i, attr in enumerate(elements)}, name="state")

        self.N_NODES = len(elements)
        self._hamiltonian = None


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


    def get_energy(self):

        total_energy = 0

        for node, state in self.graph.nodes(data="state"):

            neighbors = self.graph.neighbors(node)
            neighbors_states = np.array((self.graph.nodes(n)["state"] for n in neighbors))

            total_energy += self.hamiltonian(state, neighbors_states)

        return total_energy / 2
    

    def delta_E(self, node_to_change, new_state):

        current_state = self.graph.nodes[node_to_change]["state"]
        neighbors_states = np.array((self.graph.nodes(n)["state"] for n in self.graph.neighbors(node_to_change)))

        return 2 * (self.hamiltonian(new_state, neighbors_states) - self.hamiltonian(current_state, neighbors_states))

        


class IsingModel(UndirectedComplexNetwork):

    def __init__(self, size, dimension=2, state_initialization="random", external_field=0):

        self.SIZE = size
        self.DIMENSION = dimension
        self.FIELD = external_field

        elements, adjacency = self.get_initialization(size, dimension, state_initialization)
        super().__init__(elements, adjacency)

        @lru_cache
        def hamiltonian(central_state, neighbor_states):
            return np.sum(central_state * neighbor_states)
        
        self.hamiltonian = hamiltonian


    @staticmethod
    def get_initialization(size, dimension, state_initialization):

        n_nodes = size**dimension

        ## Get the initial values of the spins

        if state_initialization=="random":
            states = np.random.choice((1, -1), size=n_nodes, replace=True)
        elif state_initialization=="plus":
            states = np.ones(n_nodes)
        elif state_initialization=="minus":
            states = -np.ones(n_nodes)
        else:
            raise ValueError("Invalid value for the initialization. Supported values are 'random', 'plus' and 'minus'")
        
        ## Generate the adjacency matrix assuming a simple cubic lattice structure

        ## We consider interactions to first neighbours only
        ## Start by assigning positions to the nodes

        position_matrix = np.zeros((n_nodes, dimension))
        arr = np.arange(size)

        for i, p in enumerate(product(*[arr for _ in range(dimension)])):
            position_matrix[i] = p

        ## Create the adjacency matrix

        adjancency_matrix = np.zeros((n_nodes, n_nodes))

        ## Calculate distances
        #! This does not work and idw why


        for i, ri in enumerate(position_matrix):
            for j, rj in enumerate(position_matrix[i:, :]):

                rij = (ri - rj)%size ## This will be of the form (0, 0, ..., 1, 0, ..., 0) for nearest neighbours
                nonzero = np.argwhere(rij!=0)

                if len(nonzero)==1:
                    if rij[nonzero]==1:
                        adjancency_matrix[i, j]=1

        
        np.fill_diagonal(adjancency_matrix, 0)

        return states, adjancency_matrix



            
        


