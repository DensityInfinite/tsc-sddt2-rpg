class Item:
    def __init__(self, name, category):
        self.name = name
        self.category = category


class Inventory:
    def __init__(self):
        self.items = []
        self.selected_item = ""

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item_name):
        for item in self.items:
            if item.name == item_name:
                self.items.remove(item)
                break

    def select_item(self, item_name):
        pass

    def get_items(self) -> list:
        return self.items

    def get_holding_item(self) -> str:
        return self.selected_item

    def display_items(self):
        print("Inventory:")
        for item in self.items:
            print(f"{item.name} ({item.category})")


# Items
sword = Item("Sword", "Weapon")
apple = Item("Apple", "Food")
torch = Item("Torch", "Tool")

# Inventory
player_inventory = Inventory()

# Picking up items
player_inventory.add_item(sword)
player_inventory.add_item(apple)
player_inventory.add_item(torch)

# Displaying items
player_inventory.display_items()

# Removing an item
player_inventory.remove_item("Apple")

# Displaying items after removing an item
player_inventory.display_items()
