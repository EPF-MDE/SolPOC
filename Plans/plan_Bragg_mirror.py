import numpy as np
import solpoc as sol
from plan_utils import generate_json

# ----------------------------------------------------------------------------#
#                   SCRIPT PARAMETERS - START                                #
# ----------------------------------------------------------------------------#

priority = 1

Comment = "A 4 periodic layers of Bragg mirror, deposited on 1mm BK7 glass"
Mat_Stack = ["BK7", "SiO2", "TiO2", "SiO2", "TiO2", "SiO2", "TiO2", "SiO2", "TiO2"]
# ou : Mat_Stack = sol.write_stack_period(["BK7"], ["SiO2", "TiO2"], 4)

algo = sol.DEvol
selection = sol.selection_max
cost_function = sol.evaluate_R_Brg

Wl = np.arange(400, 800, 5)
Th_Substrate = 1e6
Th_range = (0, 200)
Ang = 0

pop_size = 30
crossover_rate = 0.5
f1, f2 = 0.9, 0.8
mutation_DE = "current_to_best"

budget = 2000
nb_run = 8
seed = 2905804230

# ----------------------------------------------------------------------------#
#                   SCRIPT PARAMETERS - END                                  #
# ----------------------------------------------------------------------------#

if __name__ == "__main__":
    generate_json(locals(), template_name="Bragg Mirror", priority=priority)
