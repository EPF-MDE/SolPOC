import numpy as np
import solpoc as sol
from Solpoc_optimizer.Interface.Manual_Interface.plan_utils import generate_json

# ----------------------------------------------------------------------------#
#                   SCRIPT PARAMETERS - START                                #
# ----------------------------------------------------------------------------#

priority = 1

Mat_Stack = ["BK7", "SiO2", "TiO2", "UM", "TiO2", "UM", "UM"]
Mat_Option = ["SiO2", "ZnO", "TiO2"]

algo = sol.DEvol
selection = sol.selection_max
cost_function = sol.evaluate_R_s

Th_range = (50, 250)
Th_Substrate = 1e6
Wl = np.arange(280, 2505, 20)
Ang = 0
Wl_Sol, Sol_Spec, name_Sol_Spec = sol.open_SolSpec("Materials/SolSpec.txt", "GT")

pop_size = 30
crossover_rate = 0.5
f1 = 1.0
mutation_DE = "rand_1"
budget = 1000
Mode_choose_material = "sigmoid"
seed = None

# ----------------------------------------------------------------------------#
#                   SCRIPT PARAMETERS - END                                  #
# ----------------------------------------------------------------------------#

if __name__ == "__main__":
    generate_json(
        locals(), template_name="Optimization with Materials", priority=priority
    )
