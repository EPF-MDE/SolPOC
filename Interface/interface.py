from curses import raw
import tkinter as tk
from tkinter import messagebox, ttk
import json
import re
import os
import ast
from datetime import datetime


class SolpocInterface(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SOLPOC UI")
        self.geometry("1100x600")
        self.configure(bg="grey")

        # template confirmé par le bouton
        self.selected_template = None

        # template cliqué dans la liste mais pas encore confirmé
        self.selected_template_f = None

        self.experiments = []
        self.parameter_entries = {}
        self.json_file = "plans_experiences.json"

        self.templates_config = {
            "AR": [
                "Comment",
                "Mat_Stack",
                "Wl (start, stop, step)",
                "Th_Substrate (nm)",
                "Th_range (min, max)",
                "n_range (min, max)",
                "nb_layer",
                "Ang (°)",
                "pop_size",
                "crossover_rate",
                "f1",
                "mutation_DE",
                "budget",
                "nb_run",
                "cpu_used",
                "seed",
            ],
            "Bragg Mirror": [
                "Comment",
                "Mat_Stack",
                "Wl (start, stop, step)",
                "Th_Substrate (nm)",
                "Th_range (min, max)",
                "Ang (°)",
                "pop_size",
                "crossover_rate",
                "f1",
                "f2",
                "mutation_DE",
                "budget",
                "nb_run",
                "seed",
            ],
            "Low-e": [
                "Comment",
                "Mat_Stack",
                "Wl (start, stop, step)",
                "Th_Substrate (nm)",
                "Th_range (min, max)",
                "Ang (°)",
                "d_Stack_Opt",
                "Lambda_cut_1 (nm)",
                "pop_size",
                "crossover_rate",
                "f1",
                "f2",
                "mutation_DE",
                "budget",
                "nb_run",
                "cpu_used",
                "seed",
            ],
            "Optimization with Materials": [
                "Mat_Stack",
                "Mat_Option",
                "Th_range (min, max)",
                "Th_Substrate (nm)",
                "Wl (start, stop, step)",
                "Ang (°)",
                "pop_size",
                "crossover_rate",
                "f1",
                "mutation_DE",
                "budget",
                "Mode_choose_material",
                "seed",
            ],
            "PV Cells": [
                "Comment",
                "Mat_Stack",
                "Wl (start, stop, step)",
                "Th_Substrate (nm)",
                "Th_range (min, max)",
                "vf_range (min, max)",
                "Ang (°)",
                "pop_size",
                "crossover_rate",
                "f1",
                "mutation_DE",
                "budget",
                "nb_run",
                "cpu_used",
                "seed",
            ],
            "Selective Coating": [
                "Comment",
                "Mat_Stack",
                "Th_Substrate (nm)",
                "Th_range (min, max)",
                "vf_range (min, max)",
                "Ang (°)",
                "C",
                "T_air (K)",
                "T_abs (K)",
                "pop_size",
                "crossover_rate",
                "f1",
                "f2",
                "mutation_DE",
                "budget",
                "nb_run",
                "cpu_used",
                "seed",
            ],
            "Spectral Splitting": [
                "Comment",
                "Mat_Stack",
                "Wl (start, stop, step)",
                "Th_Substrate (nm)",
                "Th_range (min, max)",
                "vf_range (min, max)",
                "Ang (°)",
                "lambda_cut_1 (nm)",
                "lambda_cut_2 (nm)",
                "pop_size",
                "crossover_rate",
                "f1",
                "f2",
                "mutation_DE",
                "budget",
                "nb_run",
                "cpu_used",
                "seed",
            ],
        }

        self.file_map = {
            "AR": "template_AR.py",
            "Bragg Mirror": "template_Bragg_mirror.py",
            "Low-e": "template_low_e.py",
            "Optimization with Materials": "template_optimization_with_materials.py",
            "PV Cells": "template_PVcells.py",
            "Selective Coating": "template_selective_coating.py",
            "Spectral Splitting": "template_spectral_splitting.py",
        }

        self.param_to_var = {
            "Comment": "Comment",
            "Mat_Stack": "Mat_Stack",
            "Wl (start, stop, step)": "Wl",
            "Th_Substrate (nm)": "Th_Substrate",
            "Th_range (min, max)": "Th_range",
            "n_range (min, max)": "n_range",
            "nb_layer": "nb_layer",
            "Ang (°)": "Ang",
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
            "Lambda_cut_1 (nm)": "Lambda_cut_1",
            "Mat_Option": "Mat_Option",
            "Mode_choose_material": "Mode_choose_material",
            "vf_range (min, max)": "vf_range",
            "C": "C",
            "T_air (K)": "T_air",
            "T_abs (K)": "T_abs",
            "lambda_cut_1 (nm)": "lambda_cut_1",
            "lambda_cut_2 (nm)": "lambda_cut_2",
        }

        self.param_type = {
            "Comment": "text",
            "Mat_Stack": "list",
            "Mat_Option": "list",
            "Wl (start, stop, step)": "wavelength",
            "Th_Substrate (nm)": "number",
            "Th_range (min, max)": "range",
            "n_range (min, max)": "range",
            "vf_range (min, max)": "range",
            "nb_layer": "int",
            "Ang (°)": "number",
            "d_Stack_Opt": "list",
            "Lambda_cut_1 (nm)": "number",
            "lambda_cut_1 (nm)": "number",
            "lambda_cut_2 (nm)": "number",
            "C": "number",
            "T_air (K)": "number",
            "T_abs (K)": "number",
            "pop_size": "int",
            "budget": "int",
            "nb_run": "int",
            "cpu_used": "int",
            "seed": "optional_int",
            "crossover_rate": "rate",
            "f1": "number",
            "f2": "number",
            "mutation_DE": "text",
            "Mode_choose_material": "text",
        }

        self.create_header()
        self.create_content_area()
        self.show_template_view()

    def load_defaults(self, template_name):
        # Recupere le nom du fichier associé au template
        filename = self.file_map.get(template_name)
        if not filename:
            return {}

        # Chemin vers le fichier template
        filepath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "Examples", filename
        )

        # Verifie que le fichier existe
        if not os.path.exists(filepath):
            return {}

        # Ouvre le fichier et lit le contenu
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Dictionnaire qui va contenir les valeurs par default
        defaults = {}

        # Gestion des affectations multiples (ex: f1, f2 = 0.9, 0.8)

        # Toutes les lignes avec plusieurs variables à gauche
        lines = re.findall(r"([\w\s,]+)=\s*([^\n#]+)", content)

        # Parcours chaque ligne trouvé
        for vars, values in lines:
            # Sépare les variables
            vars_list = [v.strip() for v in vars.split(",")]

            # Sépare les valeurs
            values_list = [v.strip() for v in values.split(",")]

            # Verifie s'il y a autant de variables que de valeurs
            if len(vars_list) == len(values_list):
                # Associe chaque variable à sa valeur
                for var_name, value in zip(vars_list, values_list):
                    # Parcourt les paramètres attendus par l’interface
                    for param, var in self.param_to_var.items():
                        # Si la variable correspond on stocke la valeur
                        if var == var_name:
                            defaults[param] = value

        # Gestion classique

        # Parcourt tous les paramètres attendus
        for param, var in self.param_to_var.items():
            if param in defaults:
                continue

            # Cherche une affectation simple
            match = re.search(rf"{var}\s*=\s*([^#\n]+)", content)

            if match:
                raw = match.group(1).strip()
                defaults[param] = self.simplify_default(param, raw)

        return defaults

    # Convertit une valeur brute du fichier template en format simplifié pour l'affichage.
    def simplify_default(self, param_name, raw_value):

        param_type = self.param_type.get(param_name, "text")

        # Cas d'une liste Python
        if param_type == "list":
            try:
                values = ast.literal_eval(raw_value)

                # Si la valeur est bien une liste, on enlève les crochets
                if isinstance(values, list):
                    return ", ".join(str(v).strip('"').strip("'") for v in values)

            except (ValueError, SyntaxError):
                pass

        # Cas d'un intervalle
        if param_type == "range":
            try:
                values = ast.literal_eval(raw_value)

                # Si la valeur est un tuple de deux éléments, on enlève les parenthèses
                if isinstance(values, tuple) and len(values) == 2:
                    return f"{values[0]}, {values[1]}"

            except (ValueError, SyntaxError):
                pass

        # Cas d'un texte : on enlève simplement les guillemets
        if param_type == "text":
            return raw_value.strip('"').strip("'")

        # Cas d'une longueur d'onde : on enlève np.arange( ) et les parenthèses
        if param_type == "wavelength":
            value = raw_value.strip()
            if value.startswith("np.arange(") and value.endswith(")"):
                return value[len("np.arange(") : -1]
            if value.startswith("sol.Wl_selectif(") and value.endswith(")"):
                return value[len("sol.Wl_selectif(") : -1]

        # Pour les autres types, on retourne la valeur telle quelle
        return raw_value

    def create_header(self):
        # crée la barre du haut
        self.header_frame = tk.Frame(self, bg="black", height=150)
        self.header_frame.pack(fill="x", padx=20, pady=20)

        # affiche le titre
        self.create_label(self.header_frame, "SOLPOC UI", ("Arial", 20, "bold")).pack(
            pady=(15, 10)
        )

        # frame pour les boutons
        nav_frame = tk.Frame(self.header_frame, bg="black")
        nav_frame.pack()

        # bouton pour aller sur la page templates
        tk.Button(
            nav_frame, text="Template", width=20, command=self.show_template_view
        ).grid(row=0, column=0, padx=5)

        # bouton pour aller sur la page paramètres
        tk.Button(
            nav_frame, text="Parameters", width=20, command=self.show_parameters_view
        ).grid(row=0, column=1, padx=5)

    def create_content_area(self):
        self.content_frame = tk.Frame(self, bg="black")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def create_label(self, parent, text, font=("Arial", 12), bg="black", fg="white"):
        return tk.Label(parent, text=text, font=font, bg=bg, fg=fg)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_template_view(self):
        # vide la zone principale
        self.clear_content()

        # frame gauche pour les templates
        left_frame = tk.Frame(self.content_frame, bg="black", width=300)
        left_frame.pack(side="left", fill="y", padx=(0, 10))

        # frame droite pour le résumé
        right_frame = tk.Frame(self.content_frame, bg="black")
        right_frame.pack(side="right", fill="both", expand=True)

        # titre "Templates"
        self.create_label(left_frame, "Templates", ("Arial", 14, "bold")).pack(pady=10)

        # liste des templates
        self.template_listbox = tk.Listbox(left_frame, font=("Arial", 12), height=15)
        self.template_listbox.pack(padx=20, pady=10, fill="both", expand=True)

        # ajoute chaque template dans la liste
        for template_name in self.templates_config:
            self.template_listbox.insert(tk.END, template_name)

        # action quand on sélectionne un template
        self.template_listbox.bind("<<ListboxSelect>>", self.on_template_selected)

        # bouton pour confirmer le choix
        tk.Button(
            left_frame,
            text="Choose the template",
            command=self.confirm_template_selection,
        ).pack(pady=10)

        # titre du résumé
        self.create_label(
            right_frame, "Summary of experiances plans", ("Arial", 14, "bold")
        ).pack(pady=10)

        # zone texte pour afficher les plans sauvegardés
        self.summary_text = tk.Text(right_frame, font=("Arial", 11), wrap="word")
        self.summary_text.pack(fill="both", expand=True, padx=20, pady=10)

        # met à jour le résumé
        self.refresh_summary()

    def on_template_selected(self, event):
        selection = self.template_listbox.curselection()
        if selection:
            self.selected_template_f = self.template_listbox.get(selection[0])

    def confirm_template_selection(self):
        # Verifie qu'un template a ete selectioné
        if not self.selected_template_f:
            messagebox.showwarning("Wait", "Please select a template.")
            return
        # Confirm le template selectioné
        self.selected_template = self.selected_template_f

        # Message de confirmation
        messagebox.showinfo(
            "Selected template", f"Selected template : {self.selected_template}"
        )

    def show_parameters_view(self):
        # vérifie qu'un template est sélectionné
        if not self.selected_template:
            messagebox.showwarning(
                "Wait",
                "First, select a template from the Template tab.",
            )
            return

        # vide la zone principale
        self.clear_content()

        # charge les valeurs par défaut du template
        defaults = self.load_defaults(self.selected_template)

        # conteneur principal
        container = tk.Frame(self.content_frame, bg="black")
        container.pack(fill="both", expand=True)

        # titre de la page
        self.create_label(
            container, f"Parameters - {self.selected_template}", ("Arial", 16, "bold")
        ).pack(pady=20)

        # conteneur pour le scroll
        scroll_container = tk.Frame(container, bg="black")
        scroll_container.pack(fill="both", expand=True)

        # création canvas + scrollbar
        canvas = tk.Canvas(scroll_container, bg="black", highlightthickness=0)
        scrollbar = tk.Scrollbar(
            scroll_container, orient="vertical", command=canvas.yview
        )
        scroll_frame = tk.Frame(canvas, bg="black")

        # ajuste la zone scrollable
        scroll_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # ajoute le frame dans le canvas
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # affichage canvas + scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # reset des champs
        self.parameter_entries = {}

        # récupère les paramètres du template
        parameters = self.templates_config[self.selected_template]

        # nombre de colonnes par ligne
        cols_per_row = 3

        # champs d'informations générales
        self.meta_entries = {}

        meta_frame = tk.Frame(container, bg="black")
        meta_frame.pack(fill="x", padx=20, pady=10)

        # meta_fields = ["Priority", "First name", "Last name", "Date"]
        meta_fields = ["Priority", "First name", "Last name"]

        for i, field in enumerate(meta_fields):
            self.create_label(meta_frame, field).grid(
                row=0, column=i * 2, padx=10, pady=5
            )

            if field == "Priority":
                entry = ttk.Combobox(
                    meta_frame, value=[1, 2, 3], width=18, state="readonly"
                )
                entry.current(0)  # valeur par défaut = 1
            else:
                entry = tk.Entry(meta_frame, width=20)

            entry.grid(row=0, column=i * 2 + 1, padx=10, pady=5)

            self.meta_entries[field] = entry

        # crée les champs dynamiquement
        for i, param_name in enumerate(parameters):
            row = i // cols_per_row
            col = (i % cols_per_row) * 2

            # label du paramètre
            self.create_label(scroll_frame, param_name).grid(
                row=row, column=col, padx=10, pady=8, sticky="w"
            )

            # champ de saisie
            entry = tk.Entry(scroll_frame, width=25)
            entry.grid(row=row, column=col + 1, padx=10, pady=8)

            # insère la valeur par défaut si dispo
            if param_name in defaults:
                entry.insert(0, defaults[param_name])

            # stocke le champ
            self.parameter_entries[param_name] = entry

            # Rentre la date automatiquement
            # if field == "Date":
            # entry.insert(0, datetime.now().strftime("%d/%m/%Y"))

        # frame pour le bouton en bas
        bottom_frame = tk.Frame(container, bg="black")
        bottom_frame.pack(fill="x", pady=20)

        # bouton de validation
        tk.Button(
            bottom_frame, text="Confirm", width=20, command=self.validate_parameters
        ).pack(anchor="center")

    def validate_parameters(self):

        # vérification que tous les champs template sont remplis
        for param_name, entry in self.parameter_entries.items():
            if param_name.startswith("__"):
                continue
            if not entry.get().strip():
                messagebox.showwarning("Attention", f"Veuillez remplir : {param_name}")
                return

        # récupère la priorité
        try:
            priority = int(self.meta_entries["Priority"].get())
        except (ValueError, KeyError):
            messagebox.showwarning("Attention", "La priorité doit être un entier.")
            return

        # récupère prénom et nom
        firstname = self.meta_entries.get("First name")
        firstname = firstname.get().strip() if firstname else "inconnu"

        lastname = self.meta_entries.get("Last name")
        lastname = lastname.get().strip() if lastname else "inconnu"

        # génère et sauvegarde le JSON
        filepath = self.build_and_save_json(
            self.parameter_entries, priority, firstname, lastname
        )

        messagebox.showinfo("Succès", f"Plan enregistré :\n{filepath}")

        # retour à la page principale
        self.show_template_view()

    def validate_type(self, param_name, value):
        # récupère le type attendu du paramètre
        param_type = self.param_type.get(param_name, "text")

        # enlève les espaces au début et à la fin
        value = value.strip()

        # vérifie un champ texte
        if param_type == "text":
            return value != ""

        # vérifie un entier positif
        if param_type == "int":
            return value.isdigit() and int(value) > 0

        # vérifie un entier optionnel ou None
        if param_type == "optional_int":
            return value == "None" or (value.isdigit() and int(value) > 0)

        # vérifie un nombre
        if param_type == "number":
            try:
                float(value)
                return True
            except ValueError:
                return False

        # vérifie un taux entre 0 et 1
        if param_type == "rate":
            try:
                number = float(value)
                return 0 <= number <= 1
            except ValueError:
                return False

        # vérifie un intervalle
        if param_type == "range":
            normalized = self.normalize_range(value)

            # si la conversion échoue, la valeur est invalide
            if normalized is None:
                return False

            try:
                # convertit le texte en tuple Python
                values = ast.literal_eval(normalized)

                # vérifie que c'est bien un tuple de 2 valeurs
                if not isinstance(values, tuple) or len(values) != 2:
                    return False

                # récupère les bornes min et max
                min_v, max_v = values

                # vérifie que les bornes sont numériques et cohérentes
                return (
                    isinstance(min_v, (int, float))
                    and isinstance(max_v, (int, float))
                    and min_v <= max_v
                )
            except (ValueError, SyntaxError):
                return False

        # vérifie une liste
        if param_type == "list":
            normalized = self.normalize_list(value)

            # si la conversion échoue, la valeur est invalide
            if normalized is None:
                return False

            try:
                # convertit le texte en liste Python
                values = ast.literal_eval(normalized)

                # vérifie que c'est bien une liste
                return isinstance(values, list)
            except (ValueError, SyntaxError):
                return False

        # vérifie une longueur d'onde
        if param_type == "wavelength":
            return (
                value.startswith("np.arange(")
                or value.startswith("sol.Wl_selectif(")
                or self.value_list(value)
            )

        # accepte par défaut si aucun cas spécifique
        return True

    def value_list(self, value):
        try:
            values = ast.literal_eval(value)
            if not isinstance(values, list):
                return False
            for item in values:
                if not isinstance(item, (int, float)):
                    return False
            return True
        except (ValueError, SyntaxError):
            return False

    def normalize_range(self, value):
        # enlève les espaces inutiles
        value = value.strip()

        # si déjà au bon format (tuple), on retourne tel quel
        if value.startswith("(") and value.endswith(")"):
            return value

        # remplace les espaces par des virgules puis découpe
        parts = [p.strip() for p in value.replace(" ", ",").split(",") if p.strip()]

        # si on a exactement 2 valeurs, on crée un tuple
        if len(parts) == 2:
            return f"({parts[0]}, {parts[1]})"

        # sinon la valeur est invalide
        return None

    def normalize_list(self, value):
        # enlève les espaces inutiles
        value = value.strip()

        # si déjà au bon format (liste), on retourne tel quel
        if value.startswith("["):
            return value

        # découpe la chaîne en éléments séparés par des virgules
        parts = [p.strip().strip('"').strip("'") for p in value.split(",") if p.strip()]

        # si des éléments existent, on reconstruit une liste Python valide
        if parts:
            items = ", ".join(f'"{p}"' for p in parts)
            return f"[{items}]"

        # sinon la valeur est invalide
        return None

    def parse_value(self, raw: str, json_key: str):
        raw = raw.strip()

        # null si vide ou None
        if raw == "" or raw.lower() in ("none", "null"):
            return None

        # booléens
        if raw.lower() == "true":
            return True
        if raw.lower() == "false":
            return False

        # listes de nombres : "280, 2505, 5" → [280, 2505, 5]
        list_keys = {"Wl", "Th_range", "n_range", "vf_range"}
        if json_key in list_keys:
            cleaned = raw.strip("[]() ")
            parts = [p.strip() for p in cleaned.split(",") if p.strip()]
            result = []
            for p in parts:
                try:
                    result.append(int(p))
                except ValueError:
                    result.append(float(p))
            return result

        # entiers
        if json_key in {"pop_size", "budget", "nb_run", "cpu_used", "nb_layer"}:
            try:
                return int(float(raw))
            except ValueError:
                return raw

        # floats
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
            try:
                return float(raw)
            except ValueError:
                return raw

        # seed : None ou entier
        if json_key == "seed":
            if raw.lower() in ("none", "null", ""):
                return None
            try:
                return int(raw)
            except ValueError:
                return None

        # strings propres sans guillemets
        if json_key in {"mutation_DE", "Comment", "Mode_choose_material"}:
            return raw.strip("\"'")

        # Mat_Stack : liste de strings
        if json_key in {"Mat_Stack", "Mat_Option"}:
            if raw.startswith("["):
                try:
                    import ast

                    parsed = ast.literal_eval(raw)
                    if isinstance(parsed, list):
                        return parsed
                except Exception:
                    pass
            # "BK7, TiO2" → ["BK7", "TiO2"]
            return [p.strip().strip("\"'") for p in raw.split(",") if p.strip()]

        # d_Stack_Opt : liste mixte "no, no, 10" → ["no", "no", 10]
        if json_key == "d_Stack_Opt":
            if raw.startswith("["):
                try:
                    import ast

                    return ast.literal_eval(raw)
                except Exception:
                    pass
            parts = [p.strip().strip("\"'") for p in raw.split(",") if p.strip()]
            result = []
            for p in parts:
                try:
                    result.append(float(p) if "." in p else int(p))
                except ValueError:
                    result.append(p)
            return result

        # fallback générique
        try:
            import ast

            parsed = ast.literal_eval(raw)
            if isinstance(parsed, tuple):
                return list(parsed)
            return parsed
        except Exception:
            pass

        return raw.strip("\"'")

    def build_and_save_json(
        self, parameter_entries: dict, priority: int, firstname: str, lastname: str
    ) -> str:

        # schéma de base avec tous les champs à null
        experiment = {
            "template": self.selected_template,
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
            "priority": priority,
            "not_use": False,
        }

        # correspondance label UI : clé JSON
        ui_label_to_json_key = {
            "Comment": "Comment",
            "Mat_Stack": "Mat_Stack",
            "Wl (start, stop, step)": "Wl",
            "Th_Substrate (nm)": "Th_Substrate",
            "Th_range (min, max)": "Th_range",
            "n_range (min, max)": "n_range",
            "nb_layer": "nb_layer",
            "Ang (°)": "Ang",
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
            "Lambda_cut_1 (nm)": "Lambda_cut_1",
            "lambda_cut_1 (nm)": "lambda_cut_1",
            "lambda_cut_2 (nm)": "lambda_cut_2",
            "Mat_Option": "Mat_Option",
            "Mode_choose_material": "Mode_choose_material",
            "vf_range (min, max)": "vf_range",
            "C": "C",
            "T_air (K)": "T_air",
            "T_abs (K)": "T_abs",
        }

        # remplissage avec les valeurs saisies par l'utilisateur
        for ui_label, entry_widget in parameter_entries.items():
            # on ignore les champs internes (__priority__, __firstname__...)
            if ui_label.startswith("__"):
                continue

            json_key = ui_label_to_json_key.get(ui_label, ui_label)
            raw_value = entry_widget.get().strip()
            experiment[json_key] = self.parse_value(raw_value, json_key)

        # nom de fichier : Template_Prenom_Nom_date_heure.json
        folder = "plans_experiences"
        os.makedirs(folder, exist_ok=True)

        template_slug = self.selected_template.replace(" ", "_")
        firstname_slug = firstname.strip().replace(" ", "_")
        lastname_slug = lastname.strip().replace(" ", "_")
        timestamp = datetime.now().strftime("%Y-%m-%d_%Hh%M")
        filename = f"{template_slug}_{firstname_slug}_{lastname_slug}_{timestamp}.json"
        filepath = os.path.join(folder, filename)

        # sauvegarde
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(experiment, f, indent=4, ensure_ascii=False)

        return filepath

    def refresh_summary(self):
        # vide la zone de texte
        self.summary_text.delete("1.0", tk.END)

        folder = "plans_experiences"

        # dossier inexistant ou vide
        if not os.path.exists(folder):
            self.summary_text.insert(
                tk.END, "No experimental designs have been saved yet."
            )
            return

        # liste les fichiers json triés par date
        files = sorted(f for f in os.listdir(folder) if f.endswith(".json"))

        if not files:
            self.summary_text.insert(
                tk.END, "No experimental designs have been saved yet."
            )
            return

        # clés internes à ne pas afficher
        meta_keys = {
            "template",
            "Comment",
            "priority",
            "not_use",
            "open_SolSpec",
            "open_Spec_Signal",
            "Sol_Spec",
            "name_Sol_Spec",
            "algo",
            "cost_function",
            "selection",
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
            "coherency_limit",
            "n_Stack",
            "k_Stack",
            "vf",
            "d_Stack",
        }

        # affiche chaque plan
        for i, filename in enumerate(files, start=1):
            filepath = os.path.join(folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                exp = json.load(f)

            status = "pending" if not exp.get("not_use") else "done"

            # séparateur entre plans
            separator = "─" * 60
            self.summary_text.insert(tk.END, f"{separator}\n")

            # en-tête du plan
            self.summary_text.insert(
                tk.END, f"  Plan {i} : {exp.get('template', '?')}\n"
            )
            self.summary_text.insert(tk.END, f"  File: {filename}\n")
            self.summary_text.insert(tk.END, f"  Comment: {exp.get('Comment', '')}\n")
            self.summary_text.insert(
                tk.END, f"  Priority : {exp.get('priority', '?')}   Status : {status}\n"
            )
            self.summary_text.insert(tk.END, f"\n")

            # paramètres
            for key, value in exp.items():
                if key in meta_keys or value is None:
                    continue
                self.summary_text.insert(tk.END, f"    • {key} : {value}\n")

            self.summary_text.insert(tk.END, f"\n")

        # séparateur final
        self.summary_text.insert(tk.END, "─" * 60 + "\n")


if __name__ == "__main__":
    app = SolpocInterface()
    app.mainloop()
