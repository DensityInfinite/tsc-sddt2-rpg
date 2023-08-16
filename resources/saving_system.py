from resources.utils import JsonUtils
import os


def save_game_state(inventory, player_location, grid, file_name, overwrite=True):
    if not overwrite and os.path.exists(file_name):
        raise FileExistsError(f"File '{file_name}' already exists.")

    game_state = {
        "inventory": [
            {"name": item.name, "category": item.category} for item in inventory.items
        ],
        "player_location": player_location,
        "grid": grid,
    }

    json_utils = JsonUtils()  # Create an instance of JsonUtils
    json_utils.save_to_json(file_name, game_state)  # Call the save_to_json method


def load_game_state(file_name, Inventory, Item):
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"File '{file_name}' not found.")

    json_utils = JsonUtils()  # Create an instance of JsonUtils
    game_state = json_utils.load_from_json(file_name)  # Call the load_from_json method

    inventory_data = game_state.get("inventory", [])
    inventory = Inventory()
    for item_data in inventory_data:
        if "name" not in item_data or "category" not in item_data:
            raise ValueError("Invalid item data in JSON file.")
        item = Item(item_data["name"], item_data["category"])
        inventory.add_item(item)

    player_location = game_state.get("player_location", None)
    grid = game_state.get("grid", None)

    return inventory, player_location, grid
