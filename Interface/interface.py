import tkinter as tk
from tkinter import messagebox
import json
import re
import os
from sympy import content
import ast


class SolpocInterface(tk.Tk):
    def __init__(self):
        super().__init__()

        # === FENETRE PRINCIPALE ===
        self.title("SOLPOC UI")  # titre de la fenêtre
        self.geometry("1100x600")  # taille de la fenêtre
        self.configure(bg="grey")  # couleur de fond

        # Variables
        self.selected_template = None  # template choisi (initialiser a 0)
        self.experiments = []  # liste des expériences enregistrées
        self.parameter_entries = {}  # stocke les champs de saisie
        self.json_file = "plans_experiences.json"  # fichier de sauvegarde

        # Config des templates
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

        # Interface
        self.create_header()  # crée le haut de l'interface
        self.create_content_area()  # crée la zone principale
        self.show_template_view()  # affiche la première vue

        # Ajout de la fonctionalité de remplissage automatique des paramètres
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
            "Comment" : "text",
            "Mat_Stack" : "list",
            "Mat_Option" : "list",
            "Wl (start, stop, step)" : "wavelength",
            "Th_Substrate (nm)" : "number",
            "Th_range (min, max)" : "range",
            "n_range (min, max)" : "range",
            "vf_range (min, max)" : "range",
            "nb_layer" : "int",
            "Ang (°)" : "number",
            "d_Stack_Opt" : "list",
            "Lambda_cut_1 (nm)" : "number",
            "lambda_cut_1 (nm)" : "number",
            "lambda_cut_2 (nm)" : "number",
            "C" : "number",
            "T_air (K)" : "number",
            "T_abs (K)" : "number",
            "pop_size" : "int",
            "budget" : "int",
            "nb_run" : "int",
            "cpu_used" : "int",
            "seed" : "optional_int",
            "crossover_rate" : "rate",
            "f1" : "number",
            "f2" : "number",
            "mutation_DE" : "text",
            "Mode_choose_material" : "text",
        }

    def load_defaults(self, template_name):
        filename = self.file_map.get(template_name)
        if not filename:
            return {}

        filepath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "Examples", filename
        )

        if not os.path.exists(filepath):
            return {}

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        defaults = {}
        for param, var in self.param_to_var.items():
            match = re.search(rf"{var}\s*=\s*([^#\n]+)", content)
            if match:
                defaults[param] = match.group(1).strip()

        return defaults

    def create_header(self):
        # Barre du haut
        self.header_frame = tk.Frame(self, bg="black", height=150)  # zone du haut
        self.header_frame.pack(fill="x", padx=20, pady=20)

        # Titre headers
        self.create_label(self.header_frame, "SOLPOC UI", ("Arial", 20, "bold")).pack(
            pady=(15, 10)
        )

        # Zones boutons
        nav_frame = tk.Frame(self.header_frame, bg="black")  # sous-zone pour boutons
        nav_frame.pack()

        # Boutons template
        tk.Button(
            nav_frame, text="Template", width=20, command=self.show_template_view
        ).grid(row=0, column=0, padx=5)

        # Boutons parametre
        tk.Button(
            nav_frame, text="Paramètres", width=20, command=self.show_parameters_view
        ).grid(row=0, column=1, padx=5)

    def create_content_area(self):
        # Zone pp
        self.content_frame = tk.Frame(self, bg="black")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def create_label(self, parent, text, font=("Arial", 12), bg="black", fg="white"):
        # Creer un label
        return tk.Label(parent, text=text, font=font, bg=bg, fg=fg)

    def clear_content(self):
        # Supprime le contenu
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_template_view(self):
        # Affiche la page
        self.clear_content()

        # Partie à gauche (templates)
        left_frame = tk.Frame(self.content_frame, bg="black", width=300)
        left_frame.pack(side="left", fill="y", padx=(0, 10))

        # Partie à droite (résumé)
        right_frame = tk.Frame(self.content_frame, bg="black")
        right_frame.pack(side="right", fill="both", expand=True)

        # Titre
        self.create_label(left_frame, "Templates", ("Arial", 14, "bold")).pack(pady=10)

        # Liste template
        self.template_listbox = tk.Listbox(left_frame, font=("Arial", 12), height=15)
        self.template_listbox.pack(padx=20, pady=10, fill="both", expand=True)

        # Ajout des templates
        for template_name in self.templates_config:
            self.template_listbox.insert(tk.END, template_name)

        # Clique
        self.template_listbox.bind("<<ListboxSelect>>", self.on_template_selected)

        # Bouton de confirmation
        tk.Button(
            left_frame,
            text="Choisir ce template",
            command=self.confirm_template_selection,
        ).pack(pady=10)

        # Titre du résumé
        self.create_label(
            right_frame, "Résumé des plans d'expériences", ("Arial", 14, "bold")
        ).pack(pady=10)

        # Zone de texe
        self.summary_text = tk.Text(right_frame, font=("Arial", 11), wrap="word")
        self.summary_text.pack(fill="both", expand=True, padx=20, pady=10)

        self.refresh_summary()  # met à jour le résumé

    def on_template_selected(self, event):

        # Recupere le template selectioné
        selection = self.template_listbox.curselection()
        if selection:
            self.selected_template = self.template_listbox.get(selection[0])

    def confirm_template_selection(self):
        # Verification si le template est selectioné
        if not self.selected_template:
            messagebox.showwarning("Attention", "Veuillez sélectionner un template.")
            return

        # Affiche le message
        messagebox.showinfo(
            "Template sélectionné", f"Template choisi : {self.selected_template}"
        )

    def show_parameters_view(self):
        if not self.selected_template:
            messagebox.showwarning(
                "Attention",
                "Veuillez d'abord sélectionner un template dans l'onglet Template.",
            )
            return

        self.clear_content()
        defaults = self.load_defaults(self.selected_template)

        # Conteneur principal
        container = tk.Frame(self.content_frame, bg="black")
        container.pack(fill="both", expand=True)

        # Titre
        self.create_label(
            container, f"Paramètres - {self.selected_template}", ("Arial", 16, "bold")
        ).pack(pady=20)

        # Frame pour la zone scrollable
        scroll_container = tk.Frame(container, bg="black")
        scroll_container.pack(fill="both", expand=True)

        # Zone scrollable
        canvas = tk.Canvas(scroll_container, bg="black", highlightthickness=0)
        scrollbar = tk.Scrollbar(
            scroll_container, orient="vertical", command=canvas.yview
        )
        scroll_frame = tk.Frame(canvas, bg="black")

        scroll_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Grille avec 3 paramètres par ligne
        self.parameter_entries = {}
        parameters = self.templates_config[self.selected_template]
        cols_per_row = 3

        for i, param_name in enumerate(parameters):
            row = i // cols_per_row
            col = (i % cols_per_row) * 2

            self.create_label(scroll_frame, param_name).grid(
                row=row, column=col, padx=10, pady=8, sticky="w"
            )
            entry = tk.Entry(scroll_frame, width=25)
            entry.grid(row=row, column=col + 1, padx=10, pady=8)
            if param_name in defaults:
                entry.insert(0, defaults[param_name])
            self.parameter_entries[param_name] = entry

        # Frame séparé pour le bouton en bas centré
        bottom_frame = tk.Frame(container, bg="black")
        bottom_frame.pack(fill="x", pady=20)

        tk.Button(
            bottom_frame, text="Valider", width=20, command=self.validate_parameters
        ).pack(anchor="center")

    def validate_parameters(self):
        # recupere les valeurs entrées
        parameter_values = {}

        for param_name, entry in self.parameter_entries.items():
            value = entry.get().strip()

            # vérifie si le champ est rempli
            if not value:
                messagebox.showwarning(
                    "Attention", f"Veuillez remplir le champ : {param_name}"
                )
                return
            
            # Verification du type
            if not self.validate_type(self, param_name, value):
                messagebox.showwarning(
                    "Type incorrect", 
                    f"Le champ '{param_name}' n'a pas le bon type"
                )
                return 
            
            parameter_values[param_name] = value

        # création du plan d'expériences
        experiment = {
            "template": self.selected_template,
            "parameters": parameter_values,
        }

        # ajout à la liste
        self.experiments.append(experiment)
        self.save_to_json()

        messagebox.showinfo("Succès", "Le plan d'expériences a été enregistré.")

        self.show_template_view()  # retour à la page principale

    # Fonction qui verifie le type
    def validate_type(self, param_name, value):
        param_type = self.param_type.get(param_name, "text")
        value = value.strip()

        if param_type == "text":
            return value != ""
        
        if param_type == "int":
            return value.isdigit() and int(value) > 0
        
        if param_type == "optional_int":
            return value == "None" or (value.isdigit() and int(value) > 0)

        if param_type == "number":
            try:
                float(value)
                return True
            except ValueError:
                return False
        
        if param_type == "rate":
            try:
                number = float(value)
                return 0 <= number <= 1
            except ValueError:
                return False
        
        if param_type == "range":
            try:
                values = ast.literal_eval(value)
                if not isinstance(values, tuple):
                    return False
                if len(values) != 2:
                    return False
                min_value, max_value = values
                return isinstance(min_value, (int, float)) and isinstance(max_value, (int, float)) and min_value <= max_value
            except (ValueError, SyntaxError):
                return False
            
        if param_type == "list":
            try:
                values = ast.literal_eval(value)
                return isinstance(values, list)
            except (ValueError, SyntaxError):
                return False

        if param_type == "wavelength":
            return (
                value.startswith("np.arange(")
                or value.startswith("sol.Wl_selectif(")
                or self.is_valid_number_list(value)
            )
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

    def save_to_json(self):
        # sauvegardee dans le json
        with open(self.json_file, "w", encoding="utf-8") as f:
            json.dump(self.experiments, f, indent=4, ensure_ascii=False)

    def refresh_summary(self):
        # mise a jour du texte du résumé
        self.summary_text.delete("1.0", tk.END)

        if not self.experiments:
            self.summary_text.insert(
                tk.END, "Aucun plan d'expériences enregistré pour le moment."
            )
            return

        # affiche tous les plans enregistrés
        for i, exp in enumerate(self.experiments, start=1):
            lignes = [f"Plan {i}", f"Template : {exp['template']}"]
            lignes += [
                f"  - {key} : {value}" for key, value in exp["parameters"].items()
            ]
            lignes.append("")
            self.summary_text.insert(tk.END, "\n".join(lignes) + "\n")


# lancer l'app
if __name__ == "__main__":
    app = SolpocInterface()
    app.mainloop()
