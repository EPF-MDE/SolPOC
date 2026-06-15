import numpy as np
import solpoc as sol
from Solpoc_optimizer.Interface.Manual_Interface.plan_utils import generate_json

# ----------------------------------------------------------------------------#
#                   SCRIPT PARAMETERS - START                                #
# ----------------------------------------------------------------------------#

priority = 1

Comment = "Exemple of spectral-splitting coating (dichroic mirror) for PV-CST, 20 layers of SiO2/TiO2"
Mat_Stack = sol.write_stack_period(["BK7"], ["TiO2", "SiO2"], 10)

algo = sol.DEvol
selection = sol.selection_max
cost_function = sol.evaluate_TRT

Wl = np.arange(280, 2505, 5)
Wl_Sol, Sol_Spec, name_Sol_Spec = sol.open_SolSpec("Materials/SolSpec.txt", "GT")
Th_Substrate = 1e6
Th_range = (0, 250)
vf_range = (0, 1.0)
Ang = 0
lambda_cut_1 = 500
lambda_cut_2 = 1000

pop_size = 30
crossover_rate = 0.5
f1, f2 = 1.0, 1.0
mutation_DE = "rand_1"

budget = 30000
nb_run = 4
cpu_used = 4
seed = None

# ----------------------------------------------------------------------------#
#                   SCRIPT PARAMETERS - END                                  #
# ----------------------------------------------------------------------------#

if __name__ == "__main__":
    generate_json(locals(), template_name="Spectral Splitting", priority=priority)
