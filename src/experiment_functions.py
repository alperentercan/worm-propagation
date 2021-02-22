
import simulations as simulations
import numpy as np
def run_simulation_over_graph(graph, p,number_of_runs, initial_infection, spread_type='mi-ms', **kwargs):
    if kwargs.get('add_cure') in [None, False]:
        initial_infection_list = []
        total_infection_list  = []
        roundly_infection_list = []
        for i in range(number_of_runs):                
            init_inf = (initial_infection if type(initial_infection) == list else 
                                 np.random.randint(graph.shape[0], size=initial_infection))
            initial_infection_list.append(init_inf)
            roundly_infection, running_total = simulations.simulation(graph,p,init_inf,
                                                                      spread_type=spread_type, debug=kwargs.get('debug'))
            roundly_infection_list.append(roundly_infection)
            total_infection_list.append(running_total)
            if kwargs.get('debug'):
                print(f"Run {i} took {len(running_total)} steps")
        return initial_infection_list, total_infection_list, roundly_infection_list
    else:
        pc = kwargs['pc']
        initial_cured = kwargs['initial_cured']
        initial_infection_list = []
        total_infection_list  = []
        roundly_infection_list = []
        
        initial_cured_list = []
        total_cured_list  = []
        roundly_cured_list = []
        
        for i in range(number_of_runs):

            init_inf = initial_infection if type(initial_infection) == list else np.random.randint(graph.shape[0], size=initial_infection)
            init_cure = (initial_cured if type(initial_cured) == list else 
                                 np.random.randint(graph.shape[0], size=initial_cured))                               
                                       
            initial_infection_list.append(init_inf)
            initial_cured_list.append(init_cure)
            
            
            (roundly_infection, running_total_infection,
             roundly_cured, running_total_cured) = simulations.cured_simulation(graph,pi=p, initial_infection=init_inf,pc=pc,
                                                                   initial_cure=init_cure,spread_type=spread_type,
                                                                                debug=kwargs.get('debug'))
            roundly_infection_list.append(roundly_infection)
            total_infection_list.append(running_total_infection)        
            roundly_cured_list.append(roundly_cured)
            total_cured_list.append(running_total_cured)
            
            if kwargs.get('debug'):
                print(f"Run {i} took {len(running_total_cured)} steps")
            
        return (initial_infection_list, total_infection_list, roundly_infection_list,
                initial_cured_list, total_cured_list, roundly_cured_list)
