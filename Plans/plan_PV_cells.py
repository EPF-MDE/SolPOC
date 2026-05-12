import numpy as np
import solpoc as sol
from plan_utils import generate_json

# ----------------------------------------------------------------------------#
#                   SCRIPT PARAMETERS - START                                #
# ----------------------------------------------------------------------------#

priority = 1

Comment = "Tutorial : anti-reflective coating for Si PV-Cell"
Mat_Stack = ["Si", "TiO2", "ZnO", "Al2O3"]

algo = sol.DEvol
selection = sol.selection_max
cost_function = sol.evaluate_A_pv

Wl = np.arange(280, 2505, 5)
Wl_Sol, Sol_Spec, name_Sol_Spec = sol.open_SolSpec("Materials/SolSpec.txt", "GT")
Th_Substrate = 1e6
Th_range = (0, 300)
vf_range = (0, 1.0)
Ang = 0
Wl_PV, Signal_PV, name_PV = sol.open_Spec_Signal("Materials/PV_cells.txt", 1)

pop_size = 30
crossover_rate = 0.5
f1 = 1.0
mutation_DE = "rand_1"

budget = 1500
nb_run = 8
cpu_used = 8
seed = None

# ----------------------------------------------------------------------------#
#                   SCRIPT PARAMETERS - END                                  #
# ----------------------------------------------------------------------------#

if __name__ == "__main__":
    generate_json(locals(), template_name="PV Cells", priority=priority)
