import json
import hashlib
import os


def hash_plan(plan_dict):

    ignored_keys = {
        "filename",
        "priority",
    }

    cleaned = {
        k: v
        for k, v in plan_dict.items()
        if k not in ignored_keys
    }

    json_string = json.dumps(
        cleaned,
        sort_keys=True,
        default=str,
    )

    return hashlib.md5(json_string.encode()).hexdigest()


#Cette partie etait pour tester la fonction de hachage, elle n'est plus nécessaire pour le projet final


# Charger deux json
with open("json_file1.json", "r", encoding="utf-8") as f:
    plan1 = json.load(f)

with open("json_file2.json", "r", encoding="utf-8") as f:
    plan2 = json.load(f)

hash1 = hash_plan(plan1)
hash2 = hash_plan(plan2)

print("HASH 1 :", hash1)
print("HASH 2 :", hash2)

print()

if hash1 == hash2:
    print("✅ Plans identiques")
else:
    print("❌ Plans différents")

    keys = set(plan1.keys()) | set(plan2.keys())

    print("\n=== DIFFERENCES ===")

    for k in sorted(keys):

        v1 = plan1.get(k)
        v2 = plan2.get(k)

        if v1 != v2:
            print(f"\nKEY : {k}")
            print("PLAN 1 :", v1)
            print("PLAN 2 :", v2)