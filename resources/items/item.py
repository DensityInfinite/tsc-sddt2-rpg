import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, name, category):
        # Initialise
        pygame.sprite.Sprite.__init__(self)

        self.name = name
        self.category = category

        self.image = None
        self.rect = None

    def get_name(self) -> str:
        return self.name

    def get_category(self) -> str:
        return self.category


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
        for item in self.items:
            if item.name == item_name:
                self.selected_item = item_name
                break

    def get_items(self) -> list:
        return self.items

    def get_holding_item(self) -> Item | None:
        for item in self.items:
            if item.name == self.select_item:
                return item
