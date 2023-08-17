from resources.utils import JsonUtils
import os


class SavingSystem:
    def __init__(self):
        self.json_utils = JsonUtils()

    def save_game_state(
        self, inventory, player_location, grid, file_name, overwrite=True
    ):
        if not overwrite and os.path.exists(file_name):
            raise FileExistsError(f"File '{file_name}' already exists.")

        game_state = {
            "inventory": [
                {"name": item.name, "category": item.category}
                for item in inventory.items
            ],
            "player_location": player_location,  # Save player's current location
            "grid": grid,  # Save the grid information
        }

        self.json_utils.save_to_json(file_name, game_state)

    def load_game_state(self, file_name, Inventory, Item):
        if not os.path.exists(file_name):
            raise FileNotFoundError(f"File '{file_name}' not found.")

        game_state = self.json_utils.load_from_json(file_name)

        inventory_data = game_state.get("inventory", [])
        inventory = Inventory()
        for item_data in inventory_data:
            if "name" not in item_data or "category" not in item_data:
                raise ValueError("Invalid item data in JSON file.")
            item = Item(item_data["name"], item_data["category"])
            inventory.add_item(item)

        player_location = game_state["player_location"]
        grid = game_state.get("grid", None)

        return inventory, player_location, grid
