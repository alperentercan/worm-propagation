
import simulations as sim
import graph_utils as gutils
import utils as utils
import experiment_functions as expfuncs
import argparse
import tempfile
import os


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Worm Propation in Topology Constrained Networks')
    
    # I/O
    parser.add_argument('--output_folder', default='../results/',
                type=str, help='output folder to create a run dir and store results')
    parser.add_argument('--debug', dest='debug', action='store_true',
                    help='output frequent(roundly) information to stdout')
    
    # Graph
    graph_group = parser.add_mutually_exclusive_group(required=True)
    graph_group.add_argument('--input_file', help='graph file to use')
      
    graph_group.add_argument('--topology', choices=['binomial', 'scale-free', 'small-worlds'], #default='binomial',
                type=str, help='graph topology to use when generating new graph - options: binomial/scale-free/small-worlds')
    
    # Other Optional Graph Generation Arguments
    parser.add_argument('--graph_size', default=(500,1000), nargs="+", type=int, 
                        help='If --topology arg is passed, used for graph generation, two ints n_nodes n_edges')  
    parser.add_argument('--p_rewire', default=0.07, type=float, 
                        help='If --topology arg is passed as smallworlds, used as rewiring prob, float') 
                        
    
    # Infection Arguments
    parser.add_argument('--spread_type', default='ms',choices=['ms', 'ss'],
                    type=str, help='spread mode to use - see the report for explanation - options: ms/ss')
                        
    parser.add_argument('--p_infection', dest='pi', default=0.05, type=float, 
                        help='Infection probability between an infected node and a neighboring susceptible node')
                        
    # Initial Infection Group 
    infection_init_group = parser.add_mutually_exclusive_group(required=False)
    infection_init_group.add_argument('--initially_infected', nargs="+", type=int, help='list of initially infected nodes')
    infection_init_group.add_argument('--n_initial_infected', default=1, type=int, help='number of nodes to initially infect')
                        
    # Cure Arguments                                           
   
    parser.add_argument('--add_cure', dest='add_cure', action='store_true',
                        help='whether add cure to the system')

    parser.add_argument('--p_cure', dest='pc', default=0.05, type=float, 
                        help='Curing probability between a cured node and a neighboring not cured node')
                        
    # Initial Cure Group                            
    cure_init_group = parser.add_mutually_exclusive_group(required=False)
    cure_init_group.add_argument('--initially_cured', nargs="+", type=int, help='list of initially cured nodes')
    cure_init_group.add_argument('--n_initial_cured', default=1, type=int, help='number of nodes to initially cure')
                        
                        
    # Simulation Arguments
    parser.add_argument('--nsims', default=1, type=int, 
                        help='How many times run the experiment')                        
                        
    args = parser.parse_args()

    
    # Get/Generate graph                            
    if not args.input_file is None:
        g = gutils.load_graph(args.input_file)
        n = g.shape[0]
        m = int(sum(sum(g)))
        
        utils.prRed("Graph is read from the file")
    else:
        n,m = args.graph_size
        with tempfile.TemporaryDirectory() as tmpdirname:
            file = os.path.join(tmpdirname, "graph.csv")
            gutils.generate_nx_graph(args.topology, file, n=n, m=m, 
                                     rewire_probability=args.p_rewire)
            g = gutils.load_graph(file)
            utils.prRed(f"A {args.topology} graph with {n} nodes and {m} edges generated")                        
                        
    if args.add_cure:
        utils.prRed(f"Simulating infection with cure {args.nsims} times")
        spread_type = "mi-" + args.spread_type
        utils.prYellow(f"Infection rate: {args.pi}, Cure rate: {args.pc},  Spread Type: {spread_type}")                
        initial_infection = args.initially_infected if args.initially_infected else args.n_initial_infected
        initial_cured = args.initially_cured if args.initially_cured else args.n_initial_cured

        if type(initial_infection) == list:
            utils.prGreen(f"A list of initially infected nodes was provided: {initial_infection}")
        else:
            utils.prGreen(f"Number of initially infected nodes was provided or default value 1 is used: {initial_infection}")

        if type(initial_cured) == list:
            utils.prGreen(f"A list of initially cured nodes was provided: {initial_cured}")
        else:
            utils.prGreen(f"Number of initially cured nodes was provided or default value 1 is used: {initial_cured}")
                        
        key = (f"{args.topology} - "*(not args.topology is None) + f"Spread:{spread_type},Size:{n}-{m},pi:{args.pi},pc:{args.pc}," +
                        f"init_inf:{initial_infection}, init_cure:{initial_cured}, nsims:{args.nsims}")
        output_folder = utils.get_output_folder(args.output_folder,key)
        utils.prPurple(f"Results will be saved to {output_folder}")                        
        result = expfuncs.run_simulation_over_graph(g, args.pi, number_of_runs=args.nsims,
                                                 initial_infection=initial_infection, spread_type=spread_type,
                                                 add_cure=True, initial_cured=initial_cured,pc=args.pc,
                                                debug=args.debug)
        (initial_infection_list, total_infection_list, roundly_infection_list,
                initial_cured_list, total_cured_list, roundly_cured_list)  = result
        utils.save_obj(initial_infection_list,output_folder,"initial_infected_nodes")
        utils.save_obj(total_infection_list,output_folder,"total_infection")
        utils.save_obj(roundly_infection_list,output_folder,"roundly_infection")
        utils.save_obj(initial_cured_list,output_folder,"initial_cured_nodes")
        utils.save_obj(total_cured_list,output_folder,"total_cured")
        utils.save_obj(roundly_cured_list,output_folder,"roundly_cured") 

        utils.plot_cured(output_folder, total_infection_list,roundly_infection_list,total_cured_list,roundly_cured_list)
        
    else:
        utils.prRed(f"Simulating infection w/o cure {args.nsims} times")
        spread_type = "mi-" + args.spread_type
        utils.prYellow(f"Infection rate: {args.pi}, Spread Type: {spread_type}")                
        initial_infection = args.initially_infected if args.initially_infected else args.n_initial_infected
        if type(initial_infection) == list:
            utils.prGreen(f"A list of infected nodes was provided: {initial_infection}")
        else:
            utils.prGreen(f"Number of initially infected nodes was provided or default value 1 is used: {initial_infection}")
        
        key = f"Spread:{spread_type},Size:{n}-{m},pi:{args.pi},init_inf:{initial_infection},sims:{args.nsims}"
        output_folder = utils.get_output_folder(args.output_folder,key)
        utils.prPurple(f"Results will be saved to {output_folder}")
        initial_infection_list, total_infection_list, roundly_infection_list = expfuncs.run_simulation_over_graph(g, args.pi, number_of_runs=args.nsims,
                                                 initial_infection=initial_infection, spread_type=spread_type,
                                                debug=args.debug)
        utils.save_obj(initial_infection_list,output_folder,"initial_infected_nodes")
        utils.save_obj(total_infection_list,output_folder,"total_infection")
        utils.save_obj(roundly_infection_list,output_folder,"roundly_infection")
        utils.plot_wo_cure(output_folder, total_infection_list,roundly_infection_list)                        
                        
    utils.prRed("Experiment is over")
