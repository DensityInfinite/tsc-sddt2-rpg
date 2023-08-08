import pygame
import game_settings
from resources.player import Player
from resources.enemies.enemy import Enemy
from resources.items.item import Inventory


class Combat:
    def __init__(self, player: Player, enemy: Enemy, inventory: Inventory) -> None:
        self.player = player
        self.enemy = enemy

        self.player_settings = game_settings.Player()
        self.player_health, self.player_defence = self.player.get_stats()
        self.player_base_damage = self.player_settings.base_damage
        self.player_dmg_boost = (
            15 if inventory.get_holding_item().get_category() == "weapon" else 0
        )
        self.enemy_health, self.enemy_defence = self.enemy.get_stats()

    def update(self) -> None:
        self.player_health, _ = self.player.get_stats()
        self.enemy_health, _ = self.enemy.get_stats()
