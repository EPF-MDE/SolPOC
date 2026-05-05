import tkinter as tk
from tkinter import messagebox
import json
import re
import os
import ast


class SolpocInterface(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SOLPOC UI")
        self.geometry("1100x600")
        self.configure(bg="grey")

        self.selected_template = None
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

        # Pour les autres types, on retourne la valeur telle quelle
        return raw_value
    

    def create_header(self):
        # crée la barre du haut
        self.header_frame = tk.Frame(self, bg="black", height=150)
        self.header_frame.pack(fill="x", padx=20, pady=20)

        # affiche le titre
        self.create_label(self.header_frame, "SOLPOC UI", ("Arial", 20, "bold")).pack(pady=(15, 10))

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
            self.selected_template = self.template_listbox.get(selection[0])


    def confirm_template_selection(self):
        if not self.selected_template:
            messagebox.showwarning("Wait", "Please select a template.")
            return
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

        # frame pour le bouton en bas
        bottom_frame = tk.Frame(container, bg="black")
        bottom_frame.pack(fill="x", pady=20)

        # bouton de validation
        tk.Button(
            bottom_frame, text="Confirm", width=20, command=self.validate_parameters
        ).pack(anchor="center")


    def validate_parameters(self):
        # dictionnaire qui stocke les valeurs saisies
        parameter_values = {}

        # parcourt tous les champs de paramètres
        for param_name, entry in self.parameter_entries.items():
            # récupère la valeur saisie
            value = entry.get().strip()

            # vérifie que le champ n'est pas vide
            if not value:
                messagebox.showwarning(
                    "Wait", f"Please fill in the field : {param_name}"
                )
                return

            # vérifie que la valeur a le bon type
            if not self.validate_type(param_name, value):
                messagebox.showwarning(
                    "Incorrect type",
                    f"The '{param_name}' field is of the wrong type",
                )
                return

            # récupère le type attendu du paramètre
            param_type = self.param_type.get(param_name, "text")

            # normalise les intervalles
            if param_type == "range":
                value = self.normalize_range(value)

            # normalise les listes
            elif param_type == "list":
                value = self.normalize_list(value)

            # ajoute la valeur au dictionnaire
            parameter_values[param_name] = value

        # crée le plan d'expérience
        experiment = {
            "template": self.selected_template,
            "parameters": parameter_values,
        }

        # ajoute le plan à la liste
        self.experiments.append(experiment)

        # sauvegarde dans le fichier JSON
        self.save_to_json()

        # affiche un message de succès
        messagebox.showinfo("Success", "The design of experiments has been saved.")

        # retourne à la page des templates
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


    def save_to_json(self):
        with open(self.json_file, "w", encoding="utf-8") as f:
            json.dump(self.experiments, f, indent=4, ensure_ascii=False)


    def refresh_summary(self):
        # vide la zone de texte
        self.summary_text.delete("1.0", tk.END)

        # si aucun plan enregistré, affiche un message
        if not self.experiments:
            self.summary_text.insert(
                tk.END, "No experimental designs have been saved yet."
            )
            return

        # parcourt tous les plans enregistrés
        for i, exp in enumerate(self.experiments, start=1):
            # crée les lignes à afficher
            lignes = [f"Plan {i}", f"Template : {exp['template']}"]

            # ajoute chaque paramètre du plan
            lignes += [
                f"  - {key} : {value}" for key, value in exp["parameters"].items()
            ]

            # ajoute une ligne vide pour séparer
            lignes.append("")

            # affiche le tout dans la zone texte
            self.summary_text.insert(tk.END, "\n".join(lignes) + "\n")


if __name__ == "__main__":
    app = SolpocInterface()
    app.mainloop()
