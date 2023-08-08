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
