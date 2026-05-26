import numpy as np
import solpoc as sol
from Solpoc_optimizer.Interface.Manual_Interface.plan_utils import generate_json

# ----------------------------------------------------------------------------#
#                   SCRIPT PARAMETERS - START                                #
# ----------------------------------------------------------------------------#

priority = 1

Comment = "A low emissivity coating for building"
Mat_Stack = ["BK7", "Si3N4", "ZnO", "Ag", "ZnO", "Si3N4"]

algo = sol.DEvol
selection = sol.selection_max
cost_function = sol.evaluate_low_e

Wl = np.arange(280, 1505, 5)
Wl_Sol, Sol_Spec, name_Sol_Spec = sol.open_SolSpec("Materials/SolSpec.txt", "GT")
Th_Substrate = 1e6
Th_range = (0, 200)
Ang = 0
d_Stack_Opt = ["no", "no", 10, "no", "no"]
Lambda_cut_1 = 800

pop_size = 30
crossover_rate = 0.5
f1, f2 = 0.9, 0.8
mutation_DE = "current_to_best"

budget = 3000
nb_run = 8
cpu_used = 8
seed = None

# ----------------------------------------------------------------------------#
#                   SCRIPT PARAMETERS - END                                  #
# ----------------------------------------------------------------------------#

if __name__ == "__main__":
    generate_json(locals(), template_name="Low-e", priority=priority)
