
import numpy as np

def generate_erdos_renyi(n, M, filename="erdos_graph.csv"):    

    if M <= 1:
        # This is a probability
        raise Exception("Generating from a probability is not implemented")
                    
    else:
        # This is the number of edges
        arr = (np.tril(np.arange(n*n).reshape(n,n)))
        arr[range(n), range(n)] = 0
        indices = np.nonzero(arr)
        edges = np.random.choice(len(indices[0]), M)
        graph_to_dump = np.array([indices[0][edges],indices[1][edges]], dtype=np.int16).T

    np.savetxt(filename, graph_to_dump, delimiter=",")
    

def load_graph(filename):
    edges = np.loadtxt(filename, delimiter=",", dtype=np.int32)
    n = edges.max() + 1 ## Assume no isolated nodes - Get the number of elements from zero-indexed nodes
    graph = np.zeros((n,n))
    graph[edges[:,0], edges[:,1]] = 1
    return graph


def generate_nx_graph(graph_topology, filename, **kwargs):
    import networkx as nx
    '''
    A function to generate a networkx graph with specified topology and 
    save it to the given file as an edge list.
    '''
    n = kwargs['n']
    m = kwargs['m']
    assert graph_topology in ["erdos-renyi", "binomial",
                              "barabasi-albert","scale-free",
                              "watts_strogatz", "small-worlds"], "Unknown graph type, try 'binomial','scale-free', or 'small-worlds'" 
    
    if graph_topology in ["erdos-renyi", "binomial"]:
        g = nx.dense_gnm_random_graph(n, m)
    elif graph_topology in ["barabasi-albert","scale-free"]:
        g = nx.barabasi_albert_graph(n, m//n)
    elif graph_topology in ["watts_strogatz-albert","small-worlds"]:
        g = nx.watts_strogatz_graph(n, m//n*2, kwargs['rewire_probability'])
    nx.write_edgelist(g, filename, delimiter=',', data=False)
    return g
    
def get_adjacency_matrix(g):
    import networkx as nx
    return np.tril(nx.to_numpy_array(g))
