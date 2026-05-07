import tkinter as tk
from tkinter import messagebox, ttk
import json
import re
import os
import ast
from datetime import datetime

from sympy import content


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

        self.parameter_entries = {}

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

            content = content.split("# %% You should stop modifying")[0]

            content = "\n".join(
                line
                for line in content.splitlines()
                if not line.strip().startswith("#")
            )

        start_marker = "SCRIPT PARAMETERS - START"
        end_marker = "SCRIPT PARAMETERS - END"

        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker)

        if start_idx != -1 and end_idx != -1:
            content = content[start_idx:end_idx]

        defaults = {}

        lines = re.findall(r"([\w\s,]+)=\s*([^\n#]+)", content)

        for vars, values in lines:
            vars_list = [v.strip() for v in vars.split(",")]
            values_list = [v.strip() for v in values.split(",")]

            if len(vars_list) == len(values_list):
                for var_name, value in zip(vars_list, values_list):
                    for param, var in self.param_to_var.items():
                        if var == var_name:
                            defaults[param] = self.simplify_default(param, value)

        for param, var in self.param_to_var.items():
            if param in defaults:
                continue

            match = re.search(rf"{var}\s*=\s*([^#\n]+)", content)

            if match:
                raw = match.group(1).strip()
                defaults[param] = self.simplify_default(param, raw)

        if (
            "seed" in self.templates_config[self.selected_template]
            and "seed" not in defaults
        ):
            defaults["seed"] = "None"

        return defaults

    def simplify_default(self, param_name, raw_value):

        param_type = self.param_type.get(param_name, "text")

        if param_type == "list":
            if "write_stack_period" in raw_value or "write_stack" in raw_value:
                materials = re.findall(r'["\']([^"\']+)["\']', raw_value)
                if materials:
                    return ", ".join(materials)

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

        if param_type == "number":
            try:
                return str(eval(raw_value))
            except Exception:
                return raw_value

        if param_type == "wavelength":
            value = raw_value.strip()
            if value.startswith("np.arange(") and value.endswith(")"):
                return value[len("np.arange(") : -1]
            if value.startswith("sol.Wl_selectif(") and value.endswith(")"):
                return value[len("sol.Wl_selectif(") : -1]

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

        # Double-clic pour sélectionner et ouvrir directement les paramètres
        self.template_listbox.bind("<Double-Button-1>", self.on_template_double_clicked)

        self.create_label(
            right_frame, "Summary of experiances plans", ("Arial", 14, "bold")
        ).pack(pady=10)

        self.summary_text = tk.Text(right_frame, font=("Arial", 11), wrap="word")
        self.summary_text.pack(fill="both", expand=True, padx=20, pady=10)

        self.refresh_summary()

    def on_template_double_clicked(self, event):
        selection = self.template_listbox.curselection()
        if selection:
            self.selected_template = self.template_listbox.get(selection[0])
            self.show_parameters_view()

    def show_parameters_view(self):
        if not self.selected_template:
            messagebox.showwarning(
                "Wait",
                "First, double-click a template from the Template tab.",
            )
            return

        self.clear_content()

        defaults = self.load_defaults(self.selected_template)

        container = tk.Frame(self.content_frame, bg="black")
        container.pack(fill="both", expand=True)

        self.create_label(
            container, f"Parameters - {self.selected_template}", ("Arial", 16, "bold")
        ).pack(pady=20)

        scroll_frame = tk.Frame(container, bg="black")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.parameter_entries = {}

        parameters = self.templates_config[self.selected_template]

        cols_per_row = 3

        self.meta_entries = {}

        meta_frame = tk.Frame(container, bg="black")
        meta_frame.pack(fill="x", padx=20, pady=10)

        meta_fields = ["Priority", "First name", "Last name"]

        for i, field in enumerate(meta_fields):
            self.create_label(meta_frame, field).grid(
                row=0, column=i * 2, padx=10, pady=5
            )

            if field == "Priority":
                entry = ttk.Combobox(
                    meta_frame, value=[1, 2, 3], width=18, state="readonly"
                )
                entry.current(0)
            else:
                entry = tk.Entry(meta_frame, width=20)

            entry.grid(row=0, column=i * 2 + 1, padx=10, pady=5)

            self.meta_entries[field] = entry

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

        for param_name, entry in self.parameter_entries.items():
            if param_name.startswith("__"):
                continue

            value = entry.get().strip()

            if not value:
                messagebox.showwarning("Warning", f"Please fill out : {param_name}")
                return

            if not self.validate_type(param_name, value):
                messagebox.showwarning(
                    "Incorrect type",
                    f"The '{param_name}' field is of the wrong type",
                )
                return

        priority = int(self.meta_entries["Priority"].get())

        firstname = self.meta_entries.get("First name")
        firstname = firstname.get().strip() if firstname else "inconnu"

        lastname = self.meta_entries.get("Last name")
        lastname = lastname.get().strip() if lastname else "inconnu"

        filepath = self.build_and_save_json(
            self.parameter_entries, priority, firstname, lastname
        )

        messagebox.showinfo("Succès", f"Plan enregistré :\n{filepath}")

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
            if value.startswith("np.arange(") or value.startswith("sol.Wl_selectif("):
                return True

            cleaned = value.strip("[]() ")
            parts = [p.strip() for p in cleaned.split(",") if p.strip()]
            if len(parts) == 3:
                try:
                    [float(p) for p in parts]
                    return True
                except ValueError:
                    return False

            return False

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
        value = value.strip()

        if value.startswith("(") and value.endswith(")"):
            return value

        parts = [p.strip() for p in value.replace(" ", ",").split(",") if p.strip()]

        if len(parts) == 2:
            return f"({parts[0]}, {parts[1]})"

        return None

    def normalize_list(self, value):
        value = value.strip()

        if value.startswith("["):
            return value

        parts = [p.strip().strip('"').strip("'") for p in value.split(",") if p.strip()]

        if parts:
            items = ", ".join(f'"{p}"' for p in parts)
            return f"[{items}]"

        return None

    def parse_value(self, raw: str, json_key: str):
        raw = raw.strip()

        if raw == "" or raw.lower() in ("none", "null"):
            return None

        if raw.lower() == "true":
            return True
        if raw.lower() == "false":
            return False

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

        if json_key in {"pop_size", "budget", "nb_run", "cpu_used", "nb_layer"}:
            try:
                return int(float(raw))
            except ValueError:
                return raw

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

        if json_key == "seed":
            if raw.lower() in ("none", "null", ""):
                return None
            try:
                return int(raw)
            except ValueError:
                return None

        if json_key in {"mutation_DE", "Comment", "Mode_choose_material"}:
            return raw.strip("\"'")

        if json_key in {"Mat_Stack", "Mat_Option"}:
            if raw.startswith("["):
                try:
                    parsed = ast.literal_eval(raw)
                    if isinstance(parsed, list):
                        return parsed
                except Exception:
                    pass
            return [p.strip().strip("\"'") for p in raw.split(",") if p.strip()]

        if json_key == "d_Stack_Opt":
            if raw.startswith("["):
                try:
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

        try:
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
        }

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

        for ui_label, entry_widget in parameter_entries.items():
            if ui_label.startswith("__"):
                continue

            json_key = ui_label_to_json_key.get(ui_label, ui_label)
            raw_value = entry_widget.get().strip()
            experiment[json_key] = self.parse_value(raw_value, json_key)

        folder = "plans_experiences"
        os.makedirs(folder, exist_ok=True)

        template_slug = self.selected_template.replace(" ", "_")
        firstname_slug = firstname.strip().replace(" ", "_")
        lastname_slug = lastname.strip().replace(" ", "_")
        timestamp = datetime.now().strftime("%Y-%m-%d_%Hh%M")
        filename = f"{template_slug}_{priority}_{firstname_slug}_{lastname_slug}_{timestamp}.json"
        filepath = os.path.join(folder, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(experiment, f, indent=4, ensure_ascii=False)

        return filepath

    def refresh_summary(self):
        self.summary_text.delete("1.0", tk.END)

        folder = "plans_experiences"

        if not os.path.exists(folder):
            self.summary_text.insert(
                tk.END, "No experimental designs have been saved yet."
            )
            return

        files = sorted(f for f in os.listdir(folder) if f.endswith(".json"))

        if not files:
            self.summary_text.insert(
                tk.END, "No experimental designs have been saved yet."
            )
            return

        meta_keys = {
            "template",
            "Comment",
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

        for i, filename in enumerate(files, start=1):
            filepath = os.path.join(folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                exp = json.load(f)

            priority_from_filename = filename.split("_")[0]

            self.summary_text.insert(tk.END, "─" * 60 + "\n")
            self.summary_text.insert(
                tk.END, f"  Plan {i} : {exp.get('template', '?')}\n"
            )
            self.summary_text.insert(tk.END, f"  File: {filename}\n")
            self.summary_text.insert(tk.END, f"  Comment: {exp.get('Comment', '')}\n")
            self.summary_text.insert(tk.END, f"  Priority : {priority_from_filename}\n")
            self.summary_text.insert(tk.END, f"\n")

            for key, value in exp.items():
                if key in meta_keys or value is None:
                    continue
                self.summary_text.insert(tk.END, f"    • {key} : {value}\n")

            self.summary_text.insert(tk.END, f"\n")

        self.summary_text.insert(tk.END, "─" * 60 + "\n")


if __name__ == "__main__":
    app = SolpocInterface()
    app.mainloop()
