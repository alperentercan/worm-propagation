A repository for simulating and analysing worm propagation under topological constraints.

**Repository Structure:**

* src/: Contains source files
* example_graphs/: Contains some example graphs .csv files
* notebooks/: Some Jupyter notebooks as reference for further development - they are not intended for casual users. Unorganized and broken paths.


**Imported Source Files:**

* src/main.py: Main file to run an experiment
* src/experiment_functions.py: Contains functions to run multiple simulations over a graph
* src/simulations.py: Simulation functions
* src/graph_utils.py: Functions to generate, save, and load graphs.



**Running Example Experiments:**

**Do not forget to use `--debug` flag to see roundly information during the simulation, it is disabled by default.**

Running Program 1 on the graph in binomial-0.csv 6 times and nodes 6,7,249 will be infected initially. Infection rate is 0.03:

`python src/main.py --input_file example_graphs/binomial-0.csv --p_infection 0.03 --initially_infected 6 7 249 --nsims 6`

Running Program 2 on a new Scale-free graph with 1000 nodes and 3000 edges nodes 2,45 will be cured initially and 3 randomly chosen nodes will be infected initially. Infection rate is 0.03 and Cure rate is 0.01. Experiment is run 2 times. Output roundly information to console:

`python src/main.py --topology scale-free --graph_size 1000 3000 --p_infection 0.03 --n_initial_infected 3 --add_cure --p_cure 0.01 --initially_cured 2 45  --nsims 2 --debug`


**Important Arguments:** 

* Graph Input/Generation: You can either give a pre-generated .csv file via --input_file or generate a new random graph by specificying --topology. If `--topology` is used, `networkx` package is needed to generate graphs. `--graph_size` should be followed by two integers, the first one is number of nodes and the second one is number of edges.(eg. `--graph_size 500 1000`) `--p_rewire` can be used to change the rewiring probability in small-worlds graph generation, default is 0.07.

* Spread Type: The simulations have two modes: multi-susceptible(ms) and single-susceptible(ss). These modes decide how many susceptible neighbors an infected node can infect in a round. SS is closer to the process is defined on Canvas and corresponds to limited bandwidth/resource case. MS is closer to CodeRed worm, which uses 100 threads to infect nodes in parallel. See the report for more information. Note that same spread type is used for both infection and cure.

* Adding Cure(Program 1 vs Program 2): If `--add_cure` flag is absent, Program 1 is run. If it is used, Program 2 is run.

* Infection/Cure Rate Arguments: `--p_infection` and `s--p_cure` accept floats.

* Initial Infection/Cure Arguments: You can either determine specific nodes to infect or apply cure initially, by using `--initially_infected` and `--initially_cured` flags. (sntx: "`--initially_infected 3 15 29`" infects nodes [3,15,29]) Or you can just decide how many nodes will be infected/cured by using `--n_initial_infected` and `--n_initial_cured`. (These accept a single integer.)

* I/O: `--debug` flag prints total number of infected/cured nodes roundly. `--output_folder` decides where the results will be saved, default is ../results/

* Experimenting: `--nsims` flag can be used to run simulation several times over the same graph. Note that if `--initially_infected/cured` flags used, the same initial nodes will be used every run. If --n_initial_infected/cured used, nodes will be chosen randomly every run.




