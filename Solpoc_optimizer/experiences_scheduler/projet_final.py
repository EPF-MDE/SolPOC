import numpy as np
import matplotlib

matplotlib.use("Agg")  # Backend non-interactif (pas d'affichage)
import matplotlib.pyplot as plt
import time
import os
from pathlib import Path
import solpoc as sol


from datetime import datetime
from multiprocessing import Pool
import json
import ast
import sys
# import importlib


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.hachage_test import (
    hash_plan,
    load_hashes_db,
    register_executed_plan,
    is_already_executed,
)


try:
    import function_R_s_weighted as test
except ImportError:
    print(
        "WARNING: function_R_s_weighted module not found. Falling back to sol module."
    )
    test = sol


def get_from_modules(name):
    try:
        return getattr(test, name)
    except (AttributeError, Exception):
        return getattr(sol, name)


def build_params(row):
    allowed_fields = {
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
        "f2",
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
        "nb_run",
        "seed",
        "nb_layer",
    }

    params = {}
    for key, value in row.items():
        if key not in allowed_fields:
            continue
        # Ignore None
        if value is None:
            continue
        # Ignore NaN
        if isinstance(value, (float, np.floating)) and np.isnan(value):
            continue
        params[key] = value

    # Casts spéciaux
    int_fields = ["nb_run", "seed", "nb_layer"]
    for field in int_fields:
        if field in params:
            params[field] = int(params[field])

    return params


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
        return get_from_modules(Wl)()
    elif isinstance(Wl, list) and len(Wl) == 3:
        start, stop, step = Wl
        return np.arange(start, stop, step)
    return Wl


def run_problem_solution(args):
    i, parameters, algo, cost_function, selection = args
    t1 = time.time()

    this_run_params = {}
    this_run_params.update(parameters)
    this_run_params["seed"] = parameters["seed_list"][i]

    best_solution, dev, n_iter, seed = algo(cost_function, selection, this_run_params)

    t2 = time.time()
    temps = t2 - t1

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


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    running = True
    launch_time_global = datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")

    # ────────────────────────────────────────────────────────────────────────
    # Définir les chemins une fois pour toutes, relatifs à ce script
    # ────────────────────────────────────────────────────────────────────────
    BASE_DIR = Path(__file__).resolve().parent

    PROJECT_ROOT = BASE_DIR.parents[1]

    print(f"PROJECT_ROOT : {PROJECT_ROOT}")

    PLAN_EXPERIENCE_DIR = BASE_DIR / "plan_experience"
    PLAN_EXECUTER_DIR = BASE_DIR / "plan_executer"
    PLAN_FAILED_DIR = BASE_DIR / "plan_failed"
    RUNS_DIR = BASE_DIR / "runs"
    HASH_FILE = PLAN_EXECUTER_DIR / "hashes.json"

    PLAN_EXPERIENCE_DIR.mkdir(exist_ok=True)
    PLAN_FAILED_DIR.mkdir(exist_ok=True)
    PLAN_EXECUTER_DIR.mkdir(exist_ok=True)
    RUNS_DIR.mkdir(exist_ok=True)

    # ── POINT 1 : charger le cache des hashes au démarrage ──────────────────
    hashes_db = load_hashes_db(HASH_FILE) or {}
    """
    if hashes_db:
        print(f"Cache chargé : {len(hashes_db)} experience(s) déjà exécutée(s).")
        print("\n=== Voici les expériences déjà exécutées ===")

        for plan_hash, filename in hashes_db.items():
            print(f"• {filename}")
            print(f"  hash : {plan_hash}")
            """
    # ────────────────────────────────────────────────────────────────────────

    plan_files = [f.name for f in PLAN_EXPERIENCE_DIR.glob("*.json")]
    plans = []
    for f in plan_files:
        with open(PLAN_EXPERIENCE_DIR / f, "r", encoding="utf-8") as file:
            plan = json.load(file)
            plan["filename"] = f
            filename_without_ext = f.replace(".json", "")
            try:
                priority_str = filename_without_ext.rsplit("_", 1)[-1]
                plan["priority"] = int(priority_str)
            except (ValueError, IndexError):
                plan["priority"] = 999
            plans.append(plan)

    plans.sort(key=lambda x: x.get("priority", 999))

    while running:
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

        # ── POINT 2 : vérifier le hash AVANT toute exécution ────────────────
        plan_hash = hash_plan(first_min_row)

        if is_already_executed(plan_hash, hashes_db):
            already_filename = hashes_db[plan_hash]
            print(
                f"[SKIP] {first_min_row['filename']} — experience identique à "
                f"'{already_filename}' déjà exécutée (hash: {plan_hash[:8]}…)."
            )
            # Déplacer quand même vers plan_executer pour ne pas le relancer
            (PLAN_EXPERIENCE_DIR / first_min_row["filename"]).rename(
                PLAN_EXECUTER_DIR / first_min_row["filename"]
            )
            continue
        # ────────────────────────────────────────────────────────────────────

        original_row = first_min_row.copy()

        # Initialisation of parameter Comment
        Comment = first_min_row["Comment"]

        # changement des variable a modifier
        first_min_row["Wl"] = build_wl(first_min_row["Wl"])

        # utilise la fonction de Mat_Stack si Mat_Stack est un str
        if isinstance(first_min_row["Mat_Stack"], str):
            func_name = first_min_row["Mat_Stack"].split("(")[0]
            args_str = first_min_row["Mat_Stack"].split("(")[1].rstrip(")")
            args = ast.literal_eval(f"[{args_str}]")
            first_min_row["Mat_Stack"] = get_from_modules(func_name)(*args)

        # Pour selection
        if first_min_row.get("selection") is not None:
            selection = get_from_modules(first_min_row["selection"])

        # Pour algo
        if first_min_row.get("algo") is not None:
            algo = get_from_modules(first_min_row["algo"])

        # Pour cost_function
        if first_min_row.get("cost_function") is not None:
            cost_function = get_from_modules(first_min_row["cost_function"])

        # print(f"\nPremière ligne avec priorité minimale apres transformation : \n{first_min_row}")

        # Open the solar spectrum
        if isinstance(first_min_row["open_SolSpec"], str):
            args = [
                a.strip().strip("'\"") for a in first_min_row["open_SolSpec"].split(",")
            ]
            open_solspec = get_from_modules("open_SolSpec")
            Wl_Sol, first_min_row["Sol_Spec"], first_min_row["name_Sol_Spec"] = (
                open_solspec(*args)
            )
            name_Sol_Spec = first_min_row["name_Sol_Spec"]

        if isinstance(first_min_row["open_Spec_Signal"], str):
            args = [
                a.strip().strip("'\"")
                for a in first_min_row["open_Spec_Signal"].split(",")
            ]
            # convertir en int les arguments qui sont des nombres
            args = [int(a) if a.isdigit() else a for a in args]
            open_signal = get_from_modules("open_Spec_Signal")
            Wl_PV, first_min_row["Signal_PV"], name_PV = open_signal(*args)

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
        params = build_params(first_min_row)

        # Ajouter les fonctions
        if "algo" in first_min_row and algo is not None:
            params["algo"] = algo
        if "cost_function" in first_min_row and cost_function is not None:
            params["cost_function"] = cost_function
        if "selection" in first_min_row and selection is not None:
            params["selection"] = selection

        # print(f"nb de layer : {params['nb_layer']}")
        # print(f"n_range : {params['n_range']}")
        # print(params)
        parameters = sol.get_parameters(**params)
        nb_run = params.get("nb_run", 1)

        # Lire cpu_used depuis le JSON, par défaut 4 si la clé est absente ou non convertible
        try:
            cpu_used = int(first_min_row["cpu_used"])
        except (KeyError, TypeError, ValueError):
            cpu_used = 4

        # dossier global pour tous les resultats
        global_run_dir = RUNS_DIR / launch_time_global
        global_run_dir.mkdir(exist_ok=True)

        # Capturer l'heure de résultat de ce plan d'expérience spécifique
        result_time = datetime.now().strftime("%Hh%Mm%Ss")

        # Dossier spécifique à cette expérience
        priority = first_min_row.get("priority", "unknown")
        directory = global_run_dir / f"{template_name}_{result_time}_{priority}"
        directory.mkdir(exist_ok=True)

        parameters["directory"] = str(directory)
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
            (PLAN_EXPERIENCE_DIR / first_min_row["filename"]).rename(
                PLAN_EXECUTER_DIR / first_min_row["filename"]
            )

            # ── POINT 3 : enregistrer le hash après succès ───────────────────
            register_executed_plan(
                plan_hash, first_min_row["filename"], hashes_db, HASH_FILE
            )
            print(
                f"[HASH] Plan '{first_min_row['filename']}' enregistré (hash: {plan_hash[:8]}…)."
            )
            # ────────────────────────────────────────────────────────────────

        except Exception as e:
            print(
                f"An error occurred while processing {first_min_row['filename']}: {e}"
            )
            # Déplacer le plan échoué vers plan_failed avec préfixe
            (PLAN_EXPERIENCE_DIR / first_min_row["filename"]).rename(
                PLAN_FAILED_DIR / first_min_row["filename"]
            )
            continue  # Passer au suivant

    # Fermer toutes les figures matplotlib pour éviter la fuite mémoire
    plt.close("all")

    # Supprimer les dossiers vides créés en dehors de runs
    print(f"BASE_DIR : {BASE_DIR}")
    for item in PROJECT_ROOT.iterdir():
        if (
            item.is_dir()
            and not item.name.startswith("runs")
            and item.name.startswith("2026-")
            and item.name
            not in [
                PLAN_EXPERIENCE_DIR.name,
                PLAN_EXECUTER_DIR.name,
                PLAN_FAILED_DIR.name,
            ]
        ):
            try:
                item.rmdir()  # Supprime seulement si vide
                # print(f"Dossier vide supprimé : {item.name}")
            except OSError:
                pass  # Pas vide, on passe

    # Supprimer les dossiers vides à l'intérieur de runs
    if RUNS_DIR.exists():
        for item in sorted(
            RUNS_DIR.rglob("*"), key=lambda x: len(x.parts), reverse=True
        ):
            if item.is_dir() and not any(item.iterdir()):
                try:
                    item.rmdir()
                    print(f"Dossier vide supprimé dans runs : {item}")
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
