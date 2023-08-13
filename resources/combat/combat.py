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
        self.enemy_settings = game_settings.Enemy()
        self.events = game_settings.Events()

        self.player_health, self.player_defence = self.player.get_stats()
        self.player_base_damage = self.player_settings.base_damage
        self.player_dmg_boost = (
            15 if inventory.get_holding_item().get_category() == "weapon" else 0
        )
        self.enemy_health, self.enemy_defence = self.enemy.get_stats()

        self.state = "player turn"  # player turn, player turn finished, enemy turn, enemy turn finished
        self.last_state = self.state

    def update(self) -> None:
        # Get updated stats
        self.player_health, _ = self.player.get_stats()
        self.enemy_health, _ = self.enemy.get_stats()

        # Update state
        match self.state:
            case "player turn finished":
                self.state = "enemy turn"
            case "enemy turn finished":
                self.state = "player turn"
        self.last_state = self.state

    def get_state(self) -> str:
        return self.state
