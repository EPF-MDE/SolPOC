import json
import hashlib
import os


# Clés ignorées car elles ne font pas partie du contenu scientifique du plan
_IGNORED_KEYS = {"filename", "priority", "cpu_used"}


def hash_plan(plan_dict: dict) -> str:
    """
    Calcule un hash MD5 déterministe d'un plan d'expérience.

    Les clés techniques (filename, priority, cpu_used) sont ignorées :
    deux plans identiques scientifiquement mais avec des priorités différentes
    produiront le même hash.

    Args:
        plan_dict: Le plan d'expérience sous forme de dictionnaire.

    Returns:
        Le hash MD5 du plan sous forme de chaîne hexadécimale.
    """
    cleaned = {k: v for k, v in plan_dict.items() if k not in _IGNORED_KEYS}

    json_string = json.dumps(cleaned, sort_keys=True, default=str)

    return hashlib.md5(json_string.encode()).hexdigest()


# ---------------------------------------------------------------------------
# Gestion du cache hashes.json
# ---------------------------------------------------------------------------

_HASHES_FILE = os.path.join("plan_executer", "hashes.json")


def load_hashes_db() -> dict:
    """
    Charge le cache des hashes depuis plan_executer/hashes.json.

    Returns:
        Dictionnaire { hash: filename } des plans déjà exécutés.
        Renvoie un dict vide si le fichier n'existe pas encore.
    """
    if not os.path.exists(_HASHES_FILE):
        return {}

    with open(_HASHES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_hashes_db(hashes_db: dict) -> None:
    """
    Sauvegarde le cache des hashes dans plan_executer/hashes.json.

    Args:
        hashes_db: Dictionnaire { hash: filename } à persister.
    """
    os.makedirs("plan_executer", exist_ok=True)

    with open(_HASHES_FILE, "w", encoding="utf-8") as f:
        json.dump(hashes_db, f, indent=2, ensure_ascii=False)


def is_already_executed(plan_hash: str, hashes_db: dict) -> bool:
    """
    Vérifie si un plan a déjà été exécuté.

    Args:
        plan_hash: Le hash MD5 du plan à vérifier.
        hashes_db: Le cache chargé via load_hashes_db().

    Returns:
        True si le plan a déjà été exécuté, False sinon.
    """
    return plan_hash in hashes_db


def register_executed_plan(plan_hash: str, filename: str, hashes_db: dict) -> None:
    """
    Enregistre un plan comme exécuté dans le cache (en mémoire + sur disque).

    Args:
        plan_hash: Le hash MD5 du plan.
        filename: Le nom du fichier JSON correspondant.
        hashes_db: Le cache en mémoire (modifié en place).
    """
    hashes_db[plan_hash] = filename
    save_hashes_db(hashes_db)


# import json
# import hashlib
# import os


# def hash_plan(plan_dict):

#     ignored_keys = {
#         "filename",
#         "priority",
#     }

#     cleaned = {
#         k: v
#         for k, v in plan_dict.items()
#         if k not in ignored_keys
#     }

#     json_string = json.dumps(
#         cleaned,
#         sort_keys=True,
#         default=str,
#     )

#     return hashlib.md5(json_string.encode()).hexdigest()


# Cette partie etait pour tester la fonction de hachage, elle n'est plus nécessaire pour le projet final


# # Charger deux json
# with open("json_file1.json", "r", encoding="utf-8") as f:
#     plan1 = json.load(f)

# with open("json_file2.json", "r", encoding="utf-8") as f:
#     plan2 = json.load(f)

# hash1 = hash_plan(plan1)
# hash2 = hash_plan(plan2)

# print("HASH 1 :", hash1)
# print("HASH 2 :", hash2)

# print()

# if hash1 == hash2:
#     print("✅ Plans identiques")
# else:
#     print("❌ Plans différents")

#     keys = set(plan1.keys()) | set(plan2.keys())

#     print("\n=== DIFFERENCES ===")

#     for k in sorted(keys):

#         v1 = plan1.get(k)
#         v2 = plan2.get(k)

#         if v1 != v2:
#             print(f"\nKEY : {k}")
#             print("PLAN 1 :", v1)
#             print("PLAN 2 :", v2)
