import hashlib
import os


def hash_fichiers(chemin):
    """Retourne un dict {chemin_relatif: hash} pour chaque fichier"""
    resultats = {}
    for root, dirs, files in os.walk(chemin):
        dirs.sort()
        for fichier in sorted(files):
            chemin_fichier = os.path.join(root, fichier)
            chemin_relatif = os.path.relpath(chemin_fichier, chemin)

            hasher = hashlib.md5()
            with open(chemin_fichier, "rb") as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
            resultats[chemin_relatif] = hasher.hexdigest()
    return resultats


# Comparaison détaillée
h1 = hash_fichiers("2026-05-13-10h41")
h2 = hash_fichiers("AR_10h41m11s_3")
# h2 = hash_fichiers("/chemin/dossier_B")

tous_les_fichiers = set(h1) | set(h2)
for f in sorted(tous_les_fichiers):
    if h1[f] == h2[f]:
        print(f"✅ Identique : {f}")
    if f not in h1:
        print(f"➕ Seulement dans B : {f}")
    elif f not in h2:
        print(f"➖ Seulement dans A : {f}")
    elif h1[f] != h2[f]:
        print(f"✏️  Modifié : {f}")
