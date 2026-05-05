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
                raw = match.group(1).strip()
                defaults[param] = self.simplify_default(param, raw)

        return defaults

    def simplify_default(self, param_name, raw_value):
        """Convertit une valeur brute du fichier template en format simplifié pour l'affichage."""
        param_type = self.param_type.get(param_name, "text")

        if param_type == "list":
            try:
                values = ast.literal_eval(raw_value)
                if isinstance(values, list):
                    return ", ".join(str(v).strip('"').strip("'") for v in values)
            except (ValueError, SyntaxError):
                pass

        if param_type == "range":
            try:
                values = ast.literal_eval(raw_value)
                if isinstance(values, tuple) and len(values) == 2:
                    return f"{values[0]}, {values[1]}"
            except (ValueError, SyntaxError):
                pass

        if param_type == "text":
            return raw_value.strip('"').strip("'")

        return raw_value

    def create_header(self):
        self.header_frame = tk.Frame(self, bg="black", height=150)
        self.header_frame.pack(fill="x", padx=20, pady=20)

        self.create_label(self.header_frame, "SOLPOC UI", ("Arial", 20, "bold")).pack(
            pady=(15, 10)
        )

        nav_frame = tk.Frame(self.header_frame, bg="black")
        nav_frame.pack()

        tk.Button(
            nav_frame, text="Template", width=20, command=self.show_template_view
        ).grid(row=0, column=0, padx=5)

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
        self.clear_content()

        left_frame = tk.Frame(self.content_frame, bg="black", width=300)
        left_frame.pack(side="left", fill="y", padx=(0, 10))

        right_frame = tk.Frame(self.content_frame, bg="black")
        right_frame.pack(side="right", fill="both", expand=True)

        self.create_label(left_frame, "Templates", ("Arial", 14, "bold")).pack(pady=10)

        self.template_listbox = tk.Listbox(left_frame, font=("Arial", 12), height=15)
        self.template_listbox.pack(padx=20, pady=10, fill="both", expand=True)

        for template_name in self.templates_config:
            self.template_listbox.insert(tk.END, template_name)

        self.template_listbox.bind("<<ListboxSelect>>", self.on_template_selected)

        tk.Button(
            left_frame,
            text="Choose the template",
            command=self.confirm_template_selection,
        ).pack(pady=10)

        self.create_label(
            right_frame, "Summary of experiances plans", ("Arial", 14, "bold")
        ).pack(pady=10)

        self.summary_text = tk.Text(right_frame, font=("Arial", 11), wrap="word")
        self.summary_text.pack(fill="both", expand=True, padx=20, pady=10)

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
        if not self.selected_template:
            messagebox.showwarning(
                "Wait",
                "First, select a template from the Template tab.",
            )
            return

        self.clear_content()
        defaults = self.load_defaults(self.selected_template)

        container = tk.Frame(self.content_frame, bg="black")
        container.pack(fill="both", expand=True)

        self.create_label(
            container, f"Parameters - {self.selected_template}", ("Arial", 16, "bold")
        ).pack(pady=20)

        scroll_container = tk.Frame(container, bg="black")
        scroll_container.pack(fill="both", expand=True)

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

        bottom_frame = tk.Frame(container, bg="black")
        bottom_frame.pack(fill="x", pady=20)

        tk.Button(
            bottom_frame, text="Confirm", width=20, command=self.validate_parameters
        ).pack(anchor="center")

    def validate_parameters(self):
        parameter_values = {}

        for param_name, entry in self.parameter_entries.items():
            value = entry.get().strip()

            if not value:
                messagebox.showwarning(
                    "Wait", f"Please fill in the field : {param_name}"
                )
                return

            if not self.validate_type(param_name, value):
                messagebox.showwarning(
                    "Incorrect type",
                    f"The '{param_name}' field is of the wrong type",
                )
                return

            param_type = self.param_type.get(param_name, "text")
            if param_type == "range":
                value = self.normalize_range(value)
            elif param_type == "list":
                value = self.normalize_list(value)

            parameter_values[param_name] = value

        experiment = {
            "template": self.selected_template,
            "parameters": parameter_values,
        }
        self.experiments.append(experiment)
        self.save_to_json()
        messagebox.showinfo("Success", "The design of experiments has been saved.")
        self.show_template_view()

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
            normalized = self.normalize_range(value)
            if normalized is None:
                return False
            try:
                values = ast.literal_eval(normalized)
                if not isinstance(values, tuple) or len(values) != 2:
                    return False
                min_v, max_v = values
                return (
                    isinstance(min_v, (int, float))
                    and isinstance(max_v, (int, float))
                    and min_v <= max_v
                )
            except (ValueError, SyntaxError):
                return False

        if param_type == "list":
            normalized = self.normalize_list(value)
            if normalized is None:
                return False
            try:
                values = ast.literal_eval(normalized)
                return isinstance(values, list)
            except (ValueError, SyntaxError):
                return False

        if param_type == "wavelength":
            return (
                value.startswith("np.arange(")
                or value.startswith("sol.Wl_selectif(")
                or self.value_list(value)
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

    def normalize_range(self, value):
        """Convertit '0, 200' ou '0 200' en '(0, 200)' si nécessaire."""
        value = value.strip()
        if value.startswith("(") and value.endswith(")"):
            return value
        parts = [p.strip() for p in value.replace(" ", ",").split(",") if p.strip()]
        if len(parts) == 2:
            return f"({parts[0]}, {parts[1]})"
        return None

    def normalize_list(self, value):
        """Convertit 'BK7, SiO2, TiO2' en '["BK7", "SiO2", "TiO2"]' si nécessaire."""
        value = value.strip()
        if value.startswith("["):
            return value
        parts = [p.strip().strip('"').strip("'") for p in value.split(",") if p.strip()]
        if parts:
            items = ", ".join(f'"{p}"' for p in parts)
            return f"[{items}]"
        return None

    def save_to_json(self):
        with open(self.json_file, "w", encoding="utf-8") as f:
            json.dump(self.experiments, f, indent=4, ensure_ascii=False)

    def refresh_summary(self):
        self.summary_text.delete("1.0", tk.END)

        if not self.experiments:
            self.summary_text.insert(
                tk.END, "No experimental designs have been saved yet."
            )
            return

        for i, exp in enumerate(self.experiments, start=1):
            lignes = [f"Plan {i}", f"Template : {exp['template']}"]
            lignes += [
                f"  - {key} : {value}" for key, value in exp["parameters"].items()
            ]
            lignes.append("")
            self.summary_text.insert(tk.END, "\n".join(lignes) + "\n")


if __name__ == "__main__":
    app = SolpocInterface()
    app.mainloop()
