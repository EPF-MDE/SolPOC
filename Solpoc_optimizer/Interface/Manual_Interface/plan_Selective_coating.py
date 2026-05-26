import numpy as np
import solpoc as sol
from Solpoc_optimizer.Interface.Manual_Interface.plan_utils import generate_json

# ----------------------------------------------------------------------------#
#                   SCRIPT PARAMETERS - START                                #
# ----------------------------------------------------------------------------#

priority = 1

Comment = "Tutorial : selective coating for solar thermal systems, like CSP"
Mat_Stack = ["Fe", "W", "W-Al2O3", "Al2O3"]

algo = sol.DEvol
selection = sol.selection_max
cost_function = sol.evaluate_rh

Wl = sol.Wl_selectif()
Wl_Sol, Sol_Spec, name_Sol_Spec = sol.open_SolSpec("Materials/SolSpec.txt", "DC")
Th_Substrate = 1e6
Th_range = (0, 300)
vf_range = (0, 1.0)
Ang = 0

C = 80
T_air = 20 + 273
T_abs = 300 + 273

pop_size = 30
crossover_rate = 0.5
f1, f2 = 0.9, 0.8
mutation_DE = "current_to_best"

budget = 500
nb_run = 4
cpu_used = 4
seed = None

# ----------------------------------------------------------------------------#
#                   SCRIPT PARAMETERS - END                                  #
# ----------------------------------------------------------------------------#

if __name__ == "__main__":
    generate_json(locals(), template_name="Selective Coating", priority=priority)
