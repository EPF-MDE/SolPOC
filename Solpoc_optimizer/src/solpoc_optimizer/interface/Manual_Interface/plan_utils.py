import os
from solpoc_optimizer.paths import PLAN_EXPERIENCE_DIR
import json
from datetime import datetime

VAR_TO_JSON = {
    "Comment": "Comment",
    "Mat_Stack": "Mat_Stack",
    "Wl": "Wl",
    "Th_Substrate": "Th_Substrate",
    "Th_range": "Th_range",
    "n_range": "n_range",
    "nb_layer": "nb_layer",
    "Ang": "Ang",
    "pop_size": "pop_size",
    "crossover_rate": "crossover_rate",
    "f1": "f1",
    "f2": "f2",
    "mutation_DE": "mutation_DE",
    "budget": "budget",
    "nb_run": "nb_run",
    "cpu_used": "cpu_used",
    "seed": "seed",
    "d_Stack_Opt": "d_Stack_Opt",
    "Lambda_cut_1": "Lambda_cut_1",
    "lambda_cut_1": "lambda_cut_1",
    "lambda_cut_2": "lambda_cut_2",
    "Mat_Option": "Mat_Option",
    "Mode_choose_material": "Mode_choose_material",
    "vf_range": "vf_range",
    "C": "C",
    "T_air": "T_air",
    "T_abs": "T_abs",
}

BASE_SCHEMA = {
    "template": None,
    "Comment": None,
    "Wl": None,
    "open_SolSpec": None,
    "open_Spec_Signal": None,
    "Ang": 0,
    "Sol_Spec": None,
    "name_Sol_Spec": None,
    "d_Stack": None,
    "Mat_Stack": None,
    "n_Stack": None,
    "k_Stack": None,
    "vf": None,
    "Th_range": None,
    "Th_Substrate": None,
    "vf_range": None,
    "Lambda_cut_1": None,
    "Lambda_cut_2": None,
    "pop_size": None,
    "crossover_rate": None,
    "f1": None,
    "f2": None,
    "mutation_DE": None,
    "budget": None,
    "nb_run": None,
    "cpu_used": None,
    "seed": None,
    "algo": None,
    "cost_function": None,
    "selection": None,
    "nb_layer": None,
    "n_range": None,
    "d_Stack_Opt": None,
    "C": None,
    "T_air": None,
    "T_abs": None,
    "Signal_H_eye": None,
    "poids_PV": None,
    "Signal_PV": None,
    "Signal_Th": None,
    "Signal_fit": None,
    "Signal_fit_2": None,
    "precision_AlgoG": None,
    "mutation_rate": None,
    "mutation_delta": None,
    "evaluate_rate": None,
    "Mat_Option": None,
    "coherency_limit": None,
    "Mode_choose_material": None,
}


def parse_value(value, json_key):
    """Convertit une valeur Python brute en type JSON correct."""

    if value is None:
        return None

    # Wl : ndarray ou tuple → liste de nombres
    if json_key == "Wl":
        try:
            return [int(v) if float(v) == int(v) else float(v) for v in value]
        except Exception:
            return list(value)

    # Intervalles : tuple → liste
    if json_key in {"Th_range", "n_range", "vf_range"}:
        if isinstance(value, (tuple, list)):
            return list(value)
        return value

    # Entiers
    if json_key in {"pop_size", "budget", "nb_run", "cpu_used", "nb_layer"}:
        return int(value)

    # Floats
    if json_key in {
        "crossover_rate",
        "f1",
        "f2",
        "Ang",
        "Th_Substrate",
        "Lambda_cut_1",
        "Lambda_cut_2",
        "lambda_cut_1",
        "lambda_cut_2",
        "C",
        "T_air",
        "T_abs",
    }:
        return float(value)

    # seed
    if json_key == "seed":
        return None if value is None else int(value)

    # Listes
    if json_key in {"Mat_Stack", "Mat_Option"}:
        return value if isinstance(value, list) else list(value)

    # d_Stack_Opt : liste mixte ["no", "no", 10]
    if json_key == "d_Stack_Opt":
        return value if isinstance(value, list) else list(value)

    return value


def generate_json(local_vars, template_name, priority):
    """Construit et sauvegarde le JSON à partir des variables locales du plan."""

    experiment = BASE_SCHEMA.copy()
    experiment["template"] = template_name

    for var, json_key in VAR_TO_JSON.items():
        if var in local_vars:
            experiment[json_key] = parse_value(local_vars[var], json_key)

    # dossier plans_experiences/ à la racine de SolPOC
    folder = PLAN_EXPERIENCE_DIR
    folder.mkdir(parents=True, exist_ok=True)

    template_slug = template_name.replace(" ", "_")
    timestamp = datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")
    filename = f"{template_slug}_{timestamp}_{priority}.json"
    filepath = folder / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(experiment, f, indent=4, ensure_ascii=False)

    print(f"Plan sauvegardé : {filepath}")
