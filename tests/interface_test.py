import pytest
import json
import os
from unittest.mock import Mock
from Interface.interface import SolpocInterface


class TestJsonValidation:
    # Parametrize (execute le test une fois pour chaque template)
    @pytest.mark.parametrize("template", list(SolpocInterface().templates_config.keys()))
    def test_json_generation(self, template):
        
        # Crée une instance de l'interface
        interface = Mock(spec=SolpocInterface)
        
        # Definit le template courant 
        interface.selected_template = template 

        # Données de test
        test = {"Comment":"Test", 
                "Mat_Stack":"BK7, TiO2",
                "Mat_Option":"SiO2, TiO2",
                "Wl (start, stop, step)": "280, 2505, 5",
                "Th_Substrate (nm)": "1000000",
                "Th_range (min, max)": "0, 200",
                "n_range (min, max)": "1.4, 2.4",
                "vf_range (min, max)": "0.1, 0.9",
                "nb_layer": "3",
                "Ang (°)": "0",
                "pop_size": "30",
                "crossover_rate": "0.5",
                "f1": "0.9",
                "f2": "0.8",
                "mutation_DE": "current_to_best",
                "budget": "1000",
                "nb_run": "8",
                "cpu_used": "4",
                "seed": "None",
                "d_Stack_Opt": "no, no, 10",
                "Lambda_cut_1 (nm)": "800",
                "lambda_cut_1 (nm)": "800",
                "lambda_cut_2 (nm)": "1200",
                "Mode_choose_material": "sigmoid",
                "C": "100",
                "T_air (K)": "300",
                "T_abs (K)": "350"}
        
        # Parametres envoyé au json
        parameter_entries = {}

        # Ajoute uniquement les parametres du template courant
        for param in interface.templates_config[template]:
            parameter_entries[param] = test[param]
        
        # Appel de la methode a tester (build_and_save_json)
        filepath = interface.build_and_save_json(parameter_entries, 1, "John", "Doe")

        # Verifie que le fichier existe
        assert os.path.exists(filepath)

        # Ouvre le fichier json
        with open(filepath, "r") as f:
            data = json.load(f)

        # Vérifie que le bon template est enregistré
        assert data["template"] == template

        # Correspondance entre les labels de l'interface et les clés JSON
        ui_label_to_json_key = {
            "Wl (start, stop, step)": "Wl",
            "Th_Substrate (nm)": "Th_Substrate",
            "Th_range (min, max)": "Th_range",
            "n_range (min, max)": "n_range",
            "vf_range (min, max)": "vf_range",
            "Ang (°)": "Ang",
            "Lambda_cut_1 (nm)": "Lambda_cut_1",
            "T_air (K)": "T_air",
            "T_abs (K)": "T_abs",
        }

        # Vérifie que toutes les clés du template existent dans le JSON
        for param in interface.templates_config[template]:
            json_key = ui_label_to_json_key.get(param, param)
            assert json_key in data
        
        # Différentes clés 
        int_keys = [
            "pop_size",
            "budget",
            "nb_run",
            "cpu_used",
            "nb_layer",
        ]
        
        float_key = [
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
        ]

        list_keys = [
        "Wl",
        "Th_range",
        "n_range",
        "vf_range",
        "Mat_Stack",
        "Mat_Option",
        "d_Stack_Opt",
        ]

        string_keys = [
        "Comment",
        "mutation_DE",
        "Mode_choose_material",
        ]

        optional_keys = [
        "seed",
        ]

        # Vérifie que les entiers
        for key in int_keys:
            if key in data and data[key] is not None:
                assert isinstance(data[key], int)
        
         # Vérifie les floats
        for key in float_key:
            if key in data and data[key] is not None:
                assert isinstance(data[key], float)

        # Vérifie les listes
        for key in list_keys:
            if key in data and data[key] is not None:
                assert isinstance(data[key], list)

        # Vérifie les strings
        for key in string_keys:
            if key in data and data[key] is not None:
                assert isinstance(data[key], str)

        # Vérifie seed
        if optional_keys in data and data[key] is not None:
            assert data["seed"] is None or isinstance(data["seed"], int)
        
        # Supprime le fichier apres execution 
        os.remove(filepath)

        # Supprime le dossier s'il est vide
        folder = os.path.dirname(filepath)
        if os.path.isdir(folder) and not os.listdir(folder):
            os.rmdir(folder)

# Pour résumé, ici le test verifie 3 choses : 







        
    