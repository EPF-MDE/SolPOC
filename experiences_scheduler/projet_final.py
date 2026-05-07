import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")  # Backend non-interactif (pas d'affichage)
import matplotlib.pyplot as plt
import time
import os
import solpoc as sol
from datetime import datetime
from multiprocessing import Pool, cpu_count
import json
import function_R_s_weighted as test

file_json = "plan_test.json"  # Fichier JSON contenant les plans d'expérience
# file_json = "test_unitaire.json"  # Fichier JSON de test unitaire


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()  # Convertit le tableau en liste Python
        if isinstance(obj, (np.integer,)):
            return int(obj)  # Convertit les entiers NumPy
        if isinstance(obj, (np.floating,)):
            return float(obj)  # Convertit les flottants NumPy
        return super().default(obj)


def main_for_parameters(
    parameters,
    nb_run,
    launch_time,
    Comment,
    name_Sol_Spec,
    cpu_used,
    algo,
    cost_function,
    selection,
):
    directory = parameters["directory"]
    sol.run_main(parameters)

    mp_pool = Pool(cpu_used)
    tasks = [(i, parameters, algo, cost_function, selection) for i in range(nb_run)]
    results = mp_pool.map(run_problem_solution, tasks)
    mp_pool.close()
    mp_pool.join()

    tab_best_solution, tab_dev, tab_perf, tab_n_iter, tab_temps, tab_seed = (
        [],
        [],
        [],
        [],
        [],
        [],
    )

    for best_solution, perf, dev, n_iter, temps, seed in results:
        tab_best_solution.append(best_solution)
        tab_dev.append(dev)
        tab_perf.append(perf)
        tab_n_iter.append(n_iter)
        tab_temps.append(temps)
        tab_seed.append(seed)

    Experience_results = {
        "tab_perf": tab_perf,
        "tab_dev": tab_dev,
        "tab_best_solution": tab_best_solution,
        "tab_n_iter": tab_n_iter,
        "tab_temps": tab_temps,
        "tab_seed": tab_seed,
        "Comment": Comment,
        "language": "en",
        "name_Sol_Spec": name_Sol_Spec,
        "launch_time": launch_time,
        "cpu_used": cpu_used,
        "nb_run": nb_run,
    }

    end_of_time = time.time()
    time_real = end_of_time - parameters["dawn_of_time"]
    parameters.update({"time_real": time_real})

    print("Total real time: {:.2f}s".format(time_real))
    print("Processor calculation time: {:.2f}s".format(sum(tab_temps)))

    sol.Explain_results(parameters, Experience_results)
    sol.Convergences_txt(parameters, Experience_results, directory)
    sol.Generate_txt(parameters, Experience_results, directory)
    sol.Optimization_txt(parameters, Experience_results, directory)
    sol.Generate_materials_txt(parameters, Experience_results, directory)

    sol.Reflectivity_plot(parameters, Experience_results, directory)
    print("Graphique de réflectivité sauvegardé.")

    sol.Transmissivity_plot(parameters, Experience_results, directory)
    print("Graphique de transmissivité sauvegardé.")

    sol.OpticalStackResponse_plot(parameters, Experience_results, directory)
    print("Graphique de réponse de la pile optique sauvegardé.")

    sol.Convergence_plots(parameters, Experience_results, directory)
    print("Graphiques de convergence sauvegardés.")

    sol.Convergence_plots_2(parameters, Experience_results, directory)
    print("Graphiques de convergence 2 sauvegardés.")

    sol.Consistency_curve_plot(parameters, Experience_results, directory)
    print("Graphique de courbe de cohérence sauvegardé.")

    sol.Optimum_thickness_plot(parameters, Experience_results, directory)
    print("Graphique d'épaisseur optimale sauvegardé.")

    sol.Optimum_refractive_index_plot(parameters, Experience_results, directory)
    print("Graphique d'indice de réfraction optimale sauvegardé.")

    sol.Volumetric_parts_plot(parameters, Experience_results, directory)
    print("Graphique des parties volumétriques sauvegardé.")

    sol.Stack_plot(parameters, Experience_results, directory)
    print("Graphique de la pile sauvegardé.")


def build_wl(Wl):
    if isinstance(Wl, str):
        try:
            return getattr(test, Wl)()
        except (AttributeError, Exception):
            return getattr(sol, Wl)()
    elif isinstance(Wl, list) and len(Wl) == 3:
        start, stop, step = Wl
        return np.arange(start, stop, step)
    return Wl


def nan_to_none(x):
    if isinstance(x, (list, np.ndarray)):
        return x  # laisser tel quel
    if pd.isna(x):
        return None
    return x


def convert_nan(obj):
    if isinstance(obj, float) and pd.isna(obj):
        return None
    if isinstance(obj, dict):
        return {k: convert_nan(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_nan(v) for v in obj]
    return obj


# creation of a function for multiprocessing
def run_problem_solution(args):
    i, parameters, algo, cost_function, selection = args
    t1 = time.time()  # Time before the optimisation process
    # Line below to be uncommented to slightly desynchronize the cores, if the seed is generated by reading the clock.
    # time.sleep(np.random.random())
    # Create a dictionary for this particular run so we can update the seed with the specific seed for this run
    this_run_params = {}
    this_run_params.update(parameters)
    this_run_params["seed"] = parameters["seed_list"][i]
    # Run the optimisation process (algo), with an evaluate method, a selection method and the parameters dictionary.
    best_solution, dev, n_iter, seed = algo(cost_function, selection, this_run_params)
    # calculate the time used
    t2 = time.time()
    temps = t2 - t1
    # best solution is a stack. Evaluation of this stack
    if type(best_solution) != list:
        best_solution = best_solution.tolist()
    best_solution = np.array(best_solution)
    dev = np.array(dev)
    perf = cost_function(best_solution, parameters)

    print(
        "I finished case #",
        str(i + 1),
        " in ",
        "{:.1f}".format(temps),
        " seconds.",
        " Best: ",
        "{:.4f}".format(perf),
        flush=True,
    )

    return best_solution, perf, dev, n_iter, temps, seed


# paramètre hors de get_parameters

cpu_used = 4  # Number of CPU used. /!\ be "raisonable", regarding the real number of CPU your computer

# ordre exact des colonnes
columns = [
    "template",
    "Comment",
    "Wl",
    "open_SolSpec",
    "open_Spec_Signal",
    "Ang",
    "Sol_Spec",
    "name_Sol_Spec",
    "d_Stack",
    "Mat_Stack",
    "n_Stack",
    "k_Stack",
    "vf",
    "Th_range",
    "Th_Substrate",
    "vf_range",
    "Lambda_cut_1",
    "Lambda_cut_2",
    "pop_size",
    "crossover_rate",
    "f1",
    "f2",
    "mutation_DE",
    "budget",
    "nb_run",
    "seed",
    "algo",
    "cost_function",
    "selection",
    "nb_layer",
    "n_range",
    "d_Stack_Opt",
    "C",
    "T_air",
    "T_abs",
    "Signal_H_eye",
    "poids_PV",
    "Signal_PV",
    "Signal_Th",
    "Signal_fit",
    "Signal_fit_2",
    "precision_AlgoG",
    "mutation_rate",
    "mutation_delta",
    "evaluate_rate",
    "Mat_Option",
    "coherency_limit",
    "Mode_choose_material",
    "priority",
    "not_use",
]
Comment = ""


if __name__ == "__main__":
    running = True
    launch_time_global = datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")

    # Créer les répertoires pour les plans
    os.makedirs("plan_experience", exist_ok=True)
    os.makedirs("plan_failed", exist_ok=True)
    os.makedirs("plan_executer", exist_ok=True)

    # Charger tous les plans depuis plan_experience
    plan_files = [f for f in os.listdir("plan_experience") if f.endswith(".json")]
    plans = []
    for f in plan_files:
        with open(os.path.join("plan_experience", f), "r", encoding="utf-8") as file:
            plan = json.load(file)
            plan["filename"] = f  # Garder le nom du fichier
            # Extraire la priorité du nom du fichier (format: template_priority.json)
            priority_str = f.rsplit("_", 1)[0]  # Prend tout sauf le dernier _
            priority_str = (
                priority_str.rsplit("_", 1)[-1] if "_" in priority_str else priority_str
            )
            # Obtenir le dernier nombre du nom (la priorité)
            import re

            match = re.search(r"_(\d+)\.json$", f)
            if match:
                plan["priority"] = int(match.group(1))
            else:
                plan["priority"] = 999  # Priorité par défaut si format incorrect
            plans.append(plan)

    # Trier par priorité croissante (du plus bas au plus haut)
    plans.sort(key=lambda x: x.get("priority", 999))

    while running:
        # All Parameters who need to be initialize to None each ru
        Wl_Sol = None
        Wl_PV = None
        name_Sol_Spec = None
        name_PV = None

        if not plans:
            running = False
            print("Aucune ligne restante à traiter. Fin de la boucle.")
            break

        first_min_row = plans.pop(0)
        template_name = first_min_row.get("template", "unknown")

        # Sauvegarder la ligne originale
        original_row = first_min_row.copy()

        # Initialisation of parameter Comment
        Comment = first_min_row["Comment"]

        # changement des variable a modifier
        first_min_row["Wl"] = build_wl(first_min_row["Wl"])

        # utilise la fonction de Mat_Stack si Mat_Stack est un str
        if isinstance(first_min_row["Mat_Stack"], str):
            func_name = first_min_row["Mat_Stack"].split("(")[0]
            args_str = first_min_row["Mat_Stack"].split("(")[1].rstrip(")")
            args = eval(f"[{args_str}]")
            try:
                first_min_row["Mat_Stack"] = getattr(test, func_name)(*args)
            except (AttributeError, Exception):
                first_min_row["Mat_Stack"] = getattr(sol, func_name)(*args)

        # Pour selection
        if first_min_row.get("selection") is not None:
            try:
                selection = getattr(test, first_min_row["selection"])
            except (AttributeError, Exception):
                selection = getattr(sol, first_min_row["selection"])
            try:
                first_min_row["selection"] = getattr(test, first_min_row["selection"])
            except (AttributeError, Exception):
                first_min_row["selection"] = getattr(sol, first_min_row["selection"])

        # Pour algo
        if first_min_row.get("algo") is not None:
            try:
                algo = getattr(test, first_min_row["algo"])
            except (AttributeError, Exception):
                algo = getattr(sol, first_min_row["algo"])
            try:
                first_min_row["algo"] = getattr(test, first_min_row["algo"])
            except (AttributeError, Exception):
                first_min_row["algo"] = getattr(sol, first_min_row["algo"])

        # Pour cost_function
        if first_min_row.get("cost_function") is not None:
            try:
                cost_function = getattr(test, first_min_row["cost_function"])
            except (AttributeError, Exception):
                cost_function = getattr(sol, first_min_row["cost_function"])
            try:
                first_min_row["cost_function"] = getattr(
                    test, first_min_row["cost_function"]
                )
            except (AttributeError, Exception):
                first_min_row["cost_function"] = getattr(
                    sol, first_min_row["cost_function"]
                )

        # print(f"\nPremière ligne avec priorité minimale apres transformation : \n{first_min_row}")

        # Open the solar spectrum
        if isinstance(first_min_row["open_SolSpec"], str):
            args = [
                a.strip().strip("'\"") for a in first_min_row["open_SolSpec"].split(",")
            ]
            try:
                Wl_Sol, first_min_row["Sol_Spec"], first_min_row["name_Sol_Spec"] = (
                    getattr(test, "open_SolSpec")(*args)
                )
            except (AttributeError, Exception):
                Wl_Sol, first_min_row["Sol_Spec"], first_min_row["name_Sol_Spec"] = (
                    getattr(sol, "open_SolSpec")(*args)
                )
            name_Sol_Spec = first_min_row["name_Sol_Spec"]

        if isinstance(first_min_row["open_Spec_Signal"], str):
            args = [
                a.strip().strip("'\"")
                for a in first_min_row["open_Spec_Signal"].split(",")
            ]
            # convertir en int les arguments qui sont des nombres
            args = [int(a) if a.isdigit() else a for a in args]
            try:
                Wl_PV, first_min_row["Signal_PV"], name_PV = getattr(
                    test, "open_Spec_Signal"
                )(*args)
            except (AttributeError, Exception):
                Wl_PV, first_min_row["Signal_PV"], name_PV = getattr(
                    sol, "open_Spec_Signal"
                )(*args)

        if first_min_row["Mat_Stack"] is not None and first_min_row["Wl"] is not None:
            first_min_row["n_Stack"], first_min_row["k_Stack"] = sol.Made_Stack(
                first_min_row["Mat_Stack"], first_min_row["Wl"]
            )

        # ajouter les paramètres manquant
        if first_min_row["Wl"] is not None and Wl_Sol is not None:
            first_min_row["Sol_Spec"] = np.interp(
                first_min_row["Wl"], Wl_Sol, first_min_row["Sol_Spec"]
            )

        # ajouter les paramètres manquant
        if first_min_row["Wl"] is not None and Wl_PV is not None:
            first_min_row["Signal_PV"] = np.interp(
                first_min_row["Wl"], Wl_PV, first_min_row["Signal_PV"]
            )

        # mettre a jour les parametres
        params = {}

        params = {}

        # Champs simples (pas de vérification NaN supplémentaire)
        simple_fields = [
            "Wl",
            "Ang",
            "Sol_Spec",
            "name_Sol_Spec",
            "d_Stack",
            "Mat_Stack",
            "n_Stack",
            "k_Stack",
            "vf",
            "Th_range",
            "Th_Substrate",
            "vf_range",
            "Lambda_cut_1",
            "Lambda_cut_2",
            "pop_size",
            "crossover_rate",
            "f1",
            "mutation_DE",
            "budget",
            "algo",
            "cost_function",
            "selection",
            "n_range",
            "d_Stack_Opt",
            "C",
            "T_air",
            "T_abs",
            "Signal_H_eye",
            "poids_PV",
            "Signal_PV",
            "Signal_Th",
            "Signal_fit",
            "Signal_fit_2",
            "precision_AlgoG",
            "mutation_rate",
            "mutation_delta",
            "evaluate_rate",
            "Mat_Option",
            "coherency_limit",
            "Mode_choose_material",
        ]

        # Champs avec vérification NaN + cast int
        int_fields = ["nb_run", "seed", "nb_layer"]

        # Champs avec vérification NaN sans cast
        nan_fields = ["f2"]

        for field in simple_fields:
            if first_min_row.get(field) is not None:
                params[field] = first_min_row[field]

        for field in int_fields:
            if first_min_row.get(field) is not None and not pd.isna(
                first_min_row.get(field)
            ):
                params[field] = int(first_min_row[field])

        for field in nan_fields:
            if first_min_row.get(field) is not None and not pd.isna(
                first_min_row.get(field)
            ):
                params[field] = first_min_row[field]

        # print(f"nb de layer : {params['nb_layer']}")
        # print(f"n_range : {params['n_range']}")
        # print(params)
        parameters = sol.get_parameters(**params)

        algo = first_min_row["algo"]

        if first_min_row["nb_run"] is not None and not pd.isna(
            first_min_row.get("nb_run")
        ):
            nb_run = int(first_min_row["nb_run"])
        else:
            nb_run = 1

        # Créer un dossier unique pour cette ligne a modifier pour faire en sorte que ensuite les resultat soit mis dedans!
        # dossier global pour tous les resultats
        global_run_dir = os.path.join("runs", launch_time_global)
        os.makedirs(global_run_dir, exist_ok=True)

        # Dossier spécifique à cette expérience
        priority = first_min_row.get("priority", "unknown")
        directory = os.path.join(global_run_dir, f"{template_name}_priority{priority}")
        os.makedirs(directory, exist_ok=True)

        parameters["directory"] = directory
        parameters["dawn_of_time"] = time.time()

        # Exécuter le main pour cette ligne
        try:
            main_for_parameters(
                parameters,
                nb_run,
                launch_time_global,
                Comment,
                name_Sol_Spec,
                cpu_used,
                algo=algo,
                cost_function=cost_function,
                selection=selection,
            )
            # Si réussi, déplacer vers plan_executer
            os.rename(
                os.path.join("plan_experience", first_min_row["filename"]),
                os.path.join("plan_executer", first_min_row["filename"]),
            )
        except Exception as e:
            print(
                f"An error occurred while processing {first_min_row['filename']}: {e}"
            )
            # Déplacer le plan échoué vers plan_failed avec préfixe
            os.rename(
                os.path.join("plan_experience", first_min_row["filename"]),
                os.path.join("plan_failed", f"failed_{first_min_row['filename']}"),
            )
            continue  # Passer au suivant

    # Fermer toutes les figures matplotlib pour éviter la fuite mémoire
    plt.close("all")

    # Supprimer les dossiers vides créés en dehors de runs
    for item in os.listdir("."):
        if (
            os.path.isdir(item)
            and not item.startswith("runs")
            and item.startswith("2026-")
            and item not in ["plan_experience", "plan_executer", "plan_failed"]
        ):
            try:
                os.rmdir(item)  # Supprime seulement si vide
                print(f"Dossier vide supprimé : {item}")
            except OSError:
                pass  # Pas vide, on passe

    # Supprimer les dossiers vides à l'intérieur de runs
    if os.path.isdir("runs"):
        for root, dirs, files in os.walk("runs", topdown=False):
            if not dirs and not files:
                try:
                    os.rmdir(root)
                    print(f"Dossier vide supprimé dans runs : {root}")
                except OSError:
                    pass  # Pas vide ou impossible à supprimer


# IMPORTANT
# Tout les paramètres ne sont pas dans la fonctions get_parameters comme Wl_Sol, Sol_Spec, name_Sol_Spec
# Donc a ajouter sinon crash
# Penser a sortir les paramètres en trop de la fonctions get_parameters par la suite

# Beginning of the main loop. The code must be in this loop to work in multiprocessing


# modifier les valeur first_min_row[] qui sont des numpy.float en variable direct (int)

# faire en sorte que l'utilisateur puisse modifier son spectre solaire directemment dans le fichier json
# Regarder pour PV pour fair ela meme chose

# hacher les plans d'expérience

# plan d'expérience 2 = PVcells
# plan d'expérience 3 = template_low_e
# plan d'expérience 1 = AR
# plan d'expérience 4 = spectral splitting
# plan d'expérience 5 = selective coating
# potentiellement rajouter le code de optimization et de bragg_mirror pour faire en sorte que ca fonctionne pour ces 2 cas

# rajouter les comment pour chaque plan d'expérience dans le json
