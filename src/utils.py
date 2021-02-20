import numpy as np
import pickle
import matplotlib.pyplot as plt
import os

def padded_stack(list_to_stack):
    max_size = max([len(a) for a in list_to_stack])
    padded_list = [np.pad(np.array(a),pad_width=(0,max_size-len(a)), mode='edge') for a in list_to_stack]
    return np.stack(padded_list)

def save_obj(obj, parent_dir, name):
    with open(os.path.join(parent_dir,name + '.pkl'), 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(parent_dir,name):
    with open(os.path.join(parent_dir,name + '.pkl'), 'rb') as f:
        return pickle.load(f)
    
def prRed(prt): print("\033[91m {}\033[00m" .format(prt))
def prGreen(prt): print("\033[92m {}\033[00m" .format(prt))
def prYellow(prt): print("\033[93m {}\033[00m" .format(prt))
def prPurple(prt): print("\033[95m {}\033[00m" .format(prt))

def get_output_folder(parent_dir, info):
    """Return save folder.

    Assumes folders in the parent_dir have suffix -run{run
    number}. Finds the highest run number and sets the output folder
    to that number + 1. This is just convenient so that if you run the
    same script multiple times tensorboard can plot all of the results
    on the same plots with different names.

    Parameters
    ----------
    parent_dir: str
      Path of the directory containing all experiment runs.

    Returns
    -------
    parent_dir/run_dir
      Path to this run's save directory.
    """
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.join(script_dir, parent_dir)
    os.makedirs(parent_dir, exist_ok=True)
    experiment_id = 0
    for folder_name in os.listdir(parent_dir):
        if not os.path.isdir(os.path.join(parent_dir, folder_name)):
            continue
        try:
            folder_name = int(folder_name.split('-run')[-1])
            if folder_name > experiment_id:
                experiment_id = folder_name
        except:
            pass
    experiment_id += 1

    parent_dir = os.path.join(parent_dir, info)
    parent_dir = parent_dir +  '%-' + os.uname()[1] + '%-run{}'.format(experiment_id)
    os.makedirs(parent_dir, exist_ok=True)
    return parent_dir

def plot_cured(output_folder, ti,ri,tc,rc):
    data = [ti,ri,tc,rc]
    labels = ["Total Infected", "Roundly Infected", "Total Cured", "Roundly Cured"]
    fig, axs = plt.subplots(2,2, sharex=True, figsize=(16,10))
    
    for k in range(4):
        res_arr = padded_stack(data[k])
        mean = np.mean(res_arr, axis=0)
        std = np.std(res_arr, axis=0)
        axs[k//2][k%2].plot(mean)      
        axs[k//2][k%2].fill_between(range(mean.shape[0]), mean-std, mean+std, alpha=0.4)  
        axs[k//2][k%2].set_title(labels[k])

    axs[0][0].set_ylabel("Number of Nodes", size=12)
    axs[1][0].set_ylabel("Number of Nodes", size=12)
    axs[1][0].set_xlabel("Simulation Step", size=12)
    axs[1][1].set_xlabel("Simulation Step", size=12)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder,"results.png"))

def plot_wo_cure(output_folder, ti,ri):
    data = [ti,ri]
    labels = ["Total Infected", "Roundly Infected"]
    fig, axs = plt.subplots(1,2, squeeze=False, figsize=(12,5))
    
    for k in range(2):
        res_arr = padded_stack(data[k])
        mean = np.mean(res_arr, axis=0)
        std = np.std(res_arr, axis=0)
        axs[k//2][k%2].plot(mean)    
        axs[k//2][k%2].fill_between(range(mean.shape[0]), mean-std, mean+std, alpha=0.4)  
        axs[k//2][k%2].set_title(labels[k])

    axs[0][0].set_ylabel("Number of Nodes", size=12)
    axs[0][0].set_xlabel("Simulation Step", size=12)
    axs[0][1].set_xlabel("Simulation Step", size=12)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder,"results.png"))
              
