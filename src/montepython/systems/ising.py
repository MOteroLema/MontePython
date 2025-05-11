from .base_systems import UndirectedComplexNetwork
from functools import lru_cache
import numpy as np
from itertools import product


class IsingModel(UndirectedComplexNetwork):

    def __init__(self, size, dimension=2, state_initialization="random", external_field=0):

        self.SIZE = size
        self.DIMENSION = dimension
        self.FIELD = external_field

        elements, adjacency = self.get_initialization(size, dimension, state_initialization)
        super().__init__(elements, adjacency)

        @lru_cache
        def hamiltonian(central_state, neighbor_states):
            return 0.5*np.sum(central_state * np.array(neighbor_states)) + central_state*external_field
        
        self.hamiltonian = hamiltonian

        def flip_state(state):
            return state*-1
        
        self.transform_state = flip_state


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

        for i, ri in enumerate(position_matrix):
            for j, rj in enumerate(position_matrix[i+1:, :]):

                rij = rj - ri
                nonzero = np.argwhere(rij!=0)

                if len(nonzero)==1:
                    value = abs(rij[nonzero])
                    if value==1 or value==n_nodes-1:
                        adjancency_matrix[i][i+j+1]=1

    
        return states, adjancency_matrix


class TwoDimensionalIsingModel(IsingModel):

    def __init__(self, size, state_initialization, external_field=0):

        super().__init__(siz=size, dimension=2, state_initialization=state_initialization, external_field=external_field)

        positions = np.zeros((size**2, 2))
        arr = np.arange(size)
        for i, p in enumerate(product(arr, arr)):
            positions[i] = p

        self.positions = positions


    def represent_state(self):

        return None

            
        


