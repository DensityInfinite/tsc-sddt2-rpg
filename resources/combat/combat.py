import pygame, random
import resources.game_settings as game_settings
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

    def update(self, action: int = -1) -> None:
        # Get updated stats
        self.player_health, _ = self.player.get_stats()
        self.enemy_health, _ = self.enemy.get_stats()

        # Emit event if combat has ended
        if self.player_health <= 0 or self.enemy_health <= 0:
            dead = "player" if self.player_health <= 0 else "enemy"
            pygame.event.post(pygame.event.Event(self.events.combat, dead=dead))

        if self.state == "player turn":
            match action:  # 1: attack, 2: item (not yet implemented), 3: escape
                case 1:
                    result = random.random()
                    if result <= self.player_settings.attack_consistency:
                        self.enemy.damage(
                            (self.player_base_damage + self.player_dmg_boost)
                            * (1 - self.enemy_defence)
                        )
                        pygame.event.post(
                            pygame.event.Event(
                                self.events.combat, turn=self.state, attack_success=True
                            )
                        )
                    else:
                        pygame.event.post(
                            pygame.event.Event(
                                self.events.combat,
                                turn=self.state,
                                attack_success=False,
                            )
                        )
                case 3:
                    result = random.random()
                    if result <= self.player_settings.escape_chance:
                        pygame.event.post(
                            pygame.event.Event(
                                self.events.combat, turn=self.state, escape_success=True
                            )
                        )
                    else:
                        pygame.event.post(
                            pygame.event.Event(
                                self.events.combat,
                                turn=self.state,
                                escape_success=False,
                            )
                        )
            if action != -1:
                self.state = "player turn finished"
        elif self.state == "enemy turn":
            if random.random() > self.enemy_settings.escape_probability:
                result = random.random()
                if result <= self.enemy_settings.attack_consistency:
                    self.enemy.damage(
                        self.enemy_settings.base_damage * (1 - self.player_defence)
                    )
                    pygame.event.post(
                        pygame.event.Event(
                            self.events.combat, turn=self.state, attack_success=True
                        )
                    )
                else:
                    pygame.event.post(
                        pygame.event.Event(
                            self.events.combat,
                            turn=self.state,
                            attack_success=False,
                        )
                    )
            else:
                result = random.random()
                if result <= self.enemy_settings.escape_chance:
                    # Emit an event indicating the enemy's escape fail
                    pygame.event.post(
                        pygame.event.Event(
                            self.events.combat, turn=self.state, escape_success=True
                        )
                    )
                else:
                    # Emit an event indicating the enemy's escape fail
                    pygame.event.post(
                        pygame.event.Event(
                            self.events.combat, turn=self.state, escape_success=False
                        )
                    )
            # Mark the end of the enemy's turn
            self.state = "enemy turn finished"

        # End turn
        match self.state:
            case "player turn finished":
                self.state = "enemy turn"
            case "enemy turn finished":
                self.state = "player turn"
        self.last_state = self.state

    def get_state(self) -> str:
        return self.state
