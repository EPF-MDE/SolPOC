import numpy as np
import solpoc as sol
from plan_utils import generate_json

# ----------------------------------------------------------------------------#
#                   SCRIPT PARAMETERS - START                                #
# ----------------------------------------------------------------------------#

priority = 1

Comment = "Tutorial : anti-reflective coating for human eye, with research of the best theorical refractiv index"
Mat_Stack = ["BK7"]

algo = sol.DEvol
selection = sol.selection_max
cost_function = sol.evaluate_T_s

Wl = np.arange(280, 2505, 5)
Wl_Sol, Sol_Spec, name_Sol_Spec = sol.open_SolSpec("Materials/SolSpec.txt", "GT")
Th_Substrate = 1e6
Th_range = (0, 300)
n_range = (1.442, 2.42)
nb_layer = 3
Ang = 0

pop_size = 30
crossover_rate = 0.5
f1 = 1.0
mutation_DE = "rand_1"

budget = 500
nb_run = 4
cpu_used = 4
seed = None

# ----------------------------------------------------------------------------#
#                   SCRIPT PARAMETERS - END                                  #
# ----------------------------------------------------------------------------#

if __name__ == "__main__":
    generate_json(locals(), template_name="AR", priority=priority)
