from pathlib import Path


# ---------------------------------------------------------
# RACINES DU PROJET
# ---------------------------------------------------------

# Dossier Solpoc_optimizer/
OPTIMIZER_DIR = Path(__file__).resolve().parent

# Racine générale du dépôt SolPOC/
PROJECT_ROOT = OPTIMIZER_DIR.parent


# ---------------------------------------------------------
# SCHEDULER
# ---------------------------------------------------------

SCHEDULER_DIR = OPTIMIZER_DIR / "experiences_scheduler"

# Plans qui attendent d'être exécutés
PLAN_EXPERIENCE_DIR = SCHEDULER_DIR / "plan_experience"

# Plans correctement exécutés
PLAN_EXECUTED_DIR = SCHEDULER_DIR / "plan_executer"

# Plans ayant échoué
PLAN_FAILED_DIR = SCHEDULER_DIR / "plan_failed"

# Résultats des expériences
RUNS_DIR = SCHEDULER_DIR / "runs"

# Base de données des hashes
HASHES_FILE = PLAN_EXECUTED_DIR / "hashes.json"


# ---------------------------------------------------------
# INTERFACE
# ---------------------------------------------------------

INTERFACE_DIR = OPTIMIZER_DIR / "Interface"

# Fichiers Python utilisés pour préremplir l'interface
MANUAL_PLANS_DIR = INTERFACE_DIR / "Manual_Interface"


# ---------------------------------------------------------
# FONCTIONS PERSONNALISÉES
# ---------------------------------------------------------

NEW_FUNCTIONS_DIR = OPTIMIZER_DIR / "new_functions"


# ---------------------------------------------------------
# CRÉATION DES DOSSIERS NÉCESSAIRES
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
        directory.mkdir(parents=True, exist_ok=True)
