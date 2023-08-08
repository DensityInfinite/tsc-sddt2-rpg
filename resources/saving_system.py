import json
import os


def save_inventory(inventory, file_name, overwrite=True):
    if not overwrite and os.path.exists(file_name):
        raise FileExistsError(f"File '{file_name}' already exists.")

    inventory_data = [
        {"name": item.name, "category": item.category} for item in inventory.items
    ]
    with open(file_name, "w") as file:
        json.dump(inventory_data, file)


def load_inventory(file_name, Inventory, Item):
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"File '{file_name}' not found.")

    with open(file_name, "r") as file:
        inventory_data = json.load(file)

    inventory = Inventory()
    for item_data in inventory_data:
        if "name" not in item_data or "category" not in item_data:
            raise ValueError("Invalid item data in JSON file.")
        item = Item(item_data["name"], item_data["category"])
        inventory.add_item(item)

    return inventory
