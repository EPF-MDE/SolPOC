import tkinter as tk
from tkinter import messagebox
import json


class SolpocInterface(tk.Tk):
    def __init__(self):
        super().__init__()

        # === FENETRE PRINCIPALE ===
        self.title("SOLPOC UI")  # titre de la fenêtre
        self.geometry("1000x700")  # taille de la fenêtre
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
        # Vérifie qu'un template est sélectionné
        if not self.selected_template:
            messagebox.showwarning(
                "Attention",
                "Veuillez d'abord sélectionner un template dans l'onglet Template.",
            )
            return

        # Supprime le contenu actuel
        self.clear_content()

        # Conteneur principal
        container = tk.Frame(self.content_frame, bg="black")
        container.pack(fill="both", expand=True)

        # Titre de la page
        self.create_label(
            container, f"Paramètres - {self.selected_template}", ("Arial", 16, "bold")
        ).pack(pady=20)

        # === Zone scrollable pour le formulaire ===
        canvas = tk.Canvas(container, bg="black", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="black")

        # Met à jour la zone scrollable quand le formulaire change
        scroll_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Affiche le formulaire avec scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Crée les champs de saisie pour chaque paramètre
        self.parameter_entries = {}
        parameters = self.templates_config[self.selected_template]

        for i, param_name in enumerate(parameters):
            # Affiche le nom du paramètre
            self.create_label(scroll_frame, param_name).grid(
                row=i, column=0, padx=10, pady=5, sticky="w"
            )
            # Crée le champ de saisie
            entry = tk.Entry(scroll_frame, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.parameter_entries[param_name] = entry

        # Bouton pour valider les paramètres
        tk.Button(
            container, text="Valider", width=20, command=self.validate_parameters
        ).pack(pady=20)

    def validate_parameters(self):
        # === RECUPERE LES VALEURS ENTREES ===
        parameter_values = {}

        for param_name, entry in self.parameter_entries.items():
            value = entry.get().strip()

            # vérifie si le champ est rempli
            if not value:
                messagebox.showwarning(
                    "Attention", f"Veuillez remplir le champ : {param_name}"
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
