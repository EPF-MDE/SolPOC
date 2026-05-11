import pytest
import json
import os
import tempfile
from unittest.mock import Mock, patch

from Interface.interface import SolpocInterface


class TestJsonValidation:
    def test_json_generation(self):
        # Crée un object mock qui imite la classe
        self.interface_object = Mock(spec=SolpocInterface)

        # Configuration du mock
        self.interface_object.selected_template = "AR" # Simule le template "AR"
        self.interface_object.parse_value = Mock(side_effect=lambda x, y: x)  # méthode factice qui renvoie le texte reçu

        # Données de test
        parameter_entries = {"Comment":"Test", "Mat_Stack":"BK7, TiO2"}

        # Appel de la methode a tester (build_and_save_json)
        filepath = SolpocInterface.build_and_save_json(self.interface_object, parameter_entries, 1, "John", "Doe")

        # Verifie que le fichier existe
        assert os.path.exists(filepath)

        # Lire le json créé
        with open(filepath, "r") as f:
            # Validité
            data = json.load(f)
        
        # Vérifie les valeurs
        assert data["template"] == "AR"
        assert data["Comment"] == "Test"
        assert data["Mat_Stack"] == "BK7, TiO2"

        # Supprime le fichier apres execution 
        os.remove(filepath)

# Pour résumé, ici le test verifie 3 choses : 

# 1. Que le fichier json est bien créé
# 2. Que le fichier json est valide
# 3. Que le Json contient les bonnes valeurs 







        
    