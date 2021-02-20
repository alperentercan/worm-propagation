
import numpy as np

def simulate_round_multi_spreader_single_susceptible(infected_nodes, graph, p):    
    directed_graph = graph + graph.T
    uninfected_nodes = 1 - infected_nodes
    infectable_neighbors_for_each_node = directed_graph * uninfected_nodes.T * infected_nodes
    n_infectable_neighbors = np.sum(infectable_neighbors_for_each_node, axis=1)
    infection_probabilities = 1 - (1-p)**n_infectable_neighbors
    infecting_nodes = np.random.uniform(size=(infection_probabilities.shape)) < infection_probabilities
    to_infect = [np.random.choice(np.nonzero(row)[0]) for row in infectable_neighbors_for_each_node[infecting_nodes]]
    infected_nodes[to_infect] = 1
    newly_infected = np.unique(to_infect).shape[0]
    no_more_infection = np.sum(n_infectable_neighbors) == 0
    return infected_nodes, newly_infected, no_more_infection    

def simulate_round_multi_spreader_multi_susceptible(infected_nodes, graph, p):    
    directed_graph = graph + graph.T
    uninfected_nodes = 1 - infected_nodes
    number_of_infected_neighbours = directed_graph.dot(infected_nodes)
    infectable_nodes = np.nonzero((number_of_infected_neighbours >= 1) * uninfected_nodes)[0]
    infection_probabilities = 1 - (1-p)**number_of_infected_neighbours
    infection = (np.random.uniform(size=(infection_probabilities.shape)) < infection_probabilities).astype(np.int)
    newly_infected = sum(uninfected_nodes*infection)
    infected_nodes = (infected_nodes + infection >= 1).astype(np.int)
    no_more_infection = len(infectable_nodes) == 0
    return infected_nodes, newly_infected, no_more_infection    

def simulate_round_single_spreader(infected_nodes, graph, p):    
    directed_graph = graph + graph.T
    uninfected_nodes = 1 - infected_nodes
    an_infected_node = np.random.choice(np.nonzero(infected_nodes)[0])
    adjecent = np.nonzero(directed_graph[an_infected_node,:])[0]
    infection = np.random.uniform(size=len(adjecent)) < p
    newly_infected = sum(uninfected_nodes[adjecent[infection]])
    infected_nodes[adjecent[infection]] += 1
    infected_nodes = (infected_nodes >= 1).astype(np.int)
    infectable_nodes = np.nonzero((directed_graph.dot(infected_nodes) >= 1) * uninfected_nodes)[0]
    no_more_infection = len(infectable_nodes) == 0
    return infected_nodes, newly_infected, no_more_infection

    
def simulation(graph, p, initial_infection, spread_type, debug=False):
    if spread_type == "si":
        sim_func = simulate_round_single_spreader
    elif spread_type == "mi-ss":
        sim_func = simulate_round_multi_spreader_single_susceptible
    elif spread_type == "mi-ms":
        sim_func = simulate_round_multi_spreader_multi_susceptible        
        
    roundly_infection = []
    running_total = []
    total_infected = len(initial_infection)
    roundly_infection.append(total_infected)
        
    n = graph.shape[0]
    infected_nodes = np.zeros((n,1))
    infected_nodes[initial_infection] = 1
    end_of_simulation = False
    k = 0
    while not end_of_simulation:
        k += 1
        running_total.append(total_infected)
        infected_nodes,newly_infected, end_of_simulation = sim_func(infected_nodes,graph,p)
        roundly_infection.append(int(newly_infected))
        total_infected += int(newly_infected)
        if debug:
            print(f"Step {k} : Total Infected: {total_infected}")        
    return roundly_infection, running_total

def simulate_round_all_spreaders_immunized(infected_nodes, graph, p, immunized_nodes):
    '''
    Currently not used.
    '''
    directed_graph = graph + graph.T
    uninfected_nodes = 1 - infected_nodes
    not_immunized_nodes = 1 - immunized_nodes
    number_of_infected_neighbours = directed_graph.dot(infected_nodes)
    infectable_nodes = np.nonzero((number_of_infected_neighbours >= 1) * uninfected_nodes * not_immunized_nodes)[0]
    infection_probabilities = 1 - (1-p)**number_of_infected_neighbours
    infection = (np.random.uniform(size=(infection_probabilities.shape)) < infection_probabilities).astype(np.int)
    newly_infected = sum(uninfected_nodes*infection*not_immunized_nodes)
    infected_nodes = (infected_nodes + infection - immunized_nodes >= 1).astype(np.int)
    no_more_infection = len(infectable_nodes) == 0
    return infected_nodes, newly_infected, no_more_infection

    

def cured_simulation(graph, pi, initial_infection, pc, initial_cure, spread_type, debug=False):
    if spread_type == "si":
        sim_func = simulate_round_single_spreader
    elif spread_type == "mi-ss":
        sim_func = simulate_round_multi_spreader_single_susceptible
    elif spread_type == "mi-ms":
        sim_func = simulate_round_multi_spreader_multi_susceptible      
#         sim_func = simulate_round_all_spreaders_immunized
        
    roundly_infection = []
    roundly_cured = []

    running_total_infection = []
    running_total_cured = []
    
    
    total_infected = len(initial_infection)
    roundly_infection.append(total_infected)
    
    total_cured = len(initial_cure)
    roundly_cured.append(total_cured)
    
    n = graph.shape[0]
    infected_nodes = np.zeros((n,1))
    infected_nodes[initial_infection] = 1
    cured_nodes = np.zeros((n,1))
    cured_nodes[initial_cure] = 1
    
    infected_nodes = (infected_nodes - cured_nodes > 0).astype(np.int)
    end_of_simulation = False
    k = 0
    while not end_of_simulation:
        k += 1
        running_total_infection.append(total_infected)
        running_total_cured.append(total_cured)
        
        # Infection 
        infected_nodes_new, _, _ = sim_func(infected_nodes,graph,pi)
        # Remove false infections - infections of already cured nodes
        # This step is unnecessary as we do not use infected_nodes until new round of cures are also applied.
        # So consider removing for slight performance increase.
        infected_nodes_new = (infected_nodes_new - cured_nodes > 0).astype(np.int)
        
        # Number of newly infected nodes. A node in infected_nodes_new is newly and trulinfected
        newly_infected = np.sum((infected_nodes_new - infected_nodes - cured_nodes > 0))
        infected_nodes = infected_nodes_new
        
        # Cure Spread
        cured_nodes, newly_cured, _ = sim_func(cured_nodes,graph,pc)
        # Apply Cure
        infected_nodes = (infected_nodes - cured_nodes > 0).astype(np.int)
        roundly_infection.append(int(newly_infected))
        total_infected += newly_infected
        roundly_cured.append(int(newly_cured))
        total_cured = np.sum(cured_nodes)
        if debug:
            print(f"Step {k} : Total Infected: {total_infected}, Total Cured: {total_cured}")
        
        end_of_simulation = sum(infected_nodes) == 0
    return roundly_infection, running_total_infection, roundly_cured, running_total_cured
