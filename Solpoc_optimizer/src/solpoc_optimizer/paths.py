from __future__ import annotations

import os
from pathlib import Path


# ---------------------------------------------------------
# DOSSIERS DU PACKAGE INSTALLÉ
# ---------------------------------------------------------

# Dossier src/solpoc_optimizer/
PACKAGE_DIR = Path(__file__).resolve().parent

# Ressources faisant partie du package
INTERFACE_DIR = PACKAGE_DIR / "interface"
MANUAL_PLANS_DIR = INTERFACE_DIR / "manual_interface"
NEW_FUNCTIONS_DIR = PACKAGE_DIR / "new_functions"


# ---------------------------------------------------------
# DOSSIER DE TRAVAIL DE L'UTILISATEUR
# ---------------------------------------------------------


def get_workspace_dir() -> Path:
    """
    Retourne le dossier de travail de SolPOC Optimizer.

    L'utilisateur peut choisir un emplacement personnalisé avec
    la variable d'environnement SOLPOC_OPTIMIZER_HOME.
    """

    custom_workspace = os.getenv("SOLPOC_OPTIMIZER_HOME")

    if custom_workspace:
        return Path(custom_workspace).expanduser().resolve()

    # Emplacement utilisé par défaut après installation
    return Path.home() / "SolPOC_Optimizer"


WORKSPACE_DIR = get_workspace_dir()


# ---------------------------------------------------------
# DOSSIERS D'EXÉCUTION
# ---------------------------------------------------------

# Plans en attente
PLAN_EXPERIENCE_DIR = WORKSPACE_DIR / "plan_experience"

# Plans exécutés
PLAN_EXECUTED_DIR = WORKSPACE_DIR / "plan_executer"

# Plans échoués
PLAN_FAILED_DIR = WORKSPACE_DIR / "plan_failed"

# Résultats générés
RUNS_DIR = WORKSPACE_DIR / "runs"

# Base des hashes
HASHES_FILE = PLAN_EXECUTED_DIR / "hashes.json"


# ---------------------------------------------------------
# CRÉATION DES DOSSIERS
# ---------------------------------------------------------


def create_project_directories() -> None:
    """Crée les dossiers de travail s'ils n'existent pas."""

    directories = [
        PLAN_EXPERIENCE_DIR,
        PLAN_EXECUTED_DIR,
        PLAN_FAILED_DIR,
        RUNS_DIR,
    ]

    for directory in directories:
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )
