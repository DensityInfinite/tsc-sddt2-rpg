import pygame, json
from os import path


class JsonUtils:
    def load_from_json(self, file_rel_path: str) -> dict:
        """file_rel_path: Need to be relative to magic_variables.py"""
        absolute_path = path.join(path.dirname(__file__), file_rel_path)
        with open(absolute_path, "r") as f:
            loaded_dict = json.load(f)
        return loaded_dict

    def save_to_json(self, file_rel_path: str, dict: dict) -> None:
        """file_rel_path: Need to be relative to magic_variables.py"""
        json_obj = json.dumps(dict, indent=4)
        absolute_path = path.join(path.dirname(__file__), file_rel_path)
        with open(absolute_path, "w") as f:
            f.write(json_obj)
