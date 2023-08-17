import pygame, os.path as path, ast
import resources.game_settings as game_settings, resources.utils as utils

from resources.enemies.enemy import Enemy


class _TileTrigger(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], type: str, link=None) -> None:
        # Initialise
        pygame.sprite.Sprite.__init__(self)
        settings = game_settings.Map()

        self.type = type  # neutral, obstruction, damage, link
        self.link = link

        self.rect = pygame.Rect(pos[0], pos[1], settings.tile_size, settings.tile_size)

    def get_type(self) -> str:
        return self.type


class Grid(pygame.sprite.Sprite):
    def __init__(self, grid_id: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.screen_settings = game_settings.Screen()
        self.map_settings = game_settings.Map()
        self.json_utils = utils.JsonUtils()

        self.image, self.triggers, self.enemies = self._init_grid(grid_id)

    def _init_grid(self, grid_id: int) -> tuple[pygame.Surface, list, list]:
        grid_image = pygame.Surface(self.screen_settings.screen_size)
        triggers = []
        enemies = []
        grid_master: dict = self.json_utils.load_from_json(
            self.map_settings.grids_master_path
        )
        grid_file_name = grid_master[str(grid_id)]["file"]
        grid_file: dict = self.json_utils.load_from_json(
            path.join(self.map_settings.grids_path, grid_file_name)
        )
        tiles: list = grid_file["tiles"]
        links: dict = grid_file["links"]
        enemies_map: list = grid_file["enemies"]
        enemies_data: list = grid_file["enemies_data"]
        textures = {
            " ": pygame.transform.scale(
                pygame.image.load(
                    path.join(self.map_settings.textures_path, "Cave Rocks.jpg")
                ).convert(),
                (self.map_settings.tile_size, self.map_settings.tile_size),
            ),
            "#": pygame.transform.scale(
                pygame.image.load(
                    path.join(self.map_settings.textures_path, "Civilised Rock.jpg")
                ).convert(),
                (self.map_settings.tile_size, self.map_settings.tile_size),
            ),
            "-": pygame.transform.scale(
                pygame.image.load(
                    path.join(self.map_settings.textures_path, "Paving Stones.jpg")
                ).convert(),
                (self.map_settings.tile_size, self.map_settings.tile_size),
            ),
            "~": pygame.transform.scale(
                pygame.image.load(
                    path.join(self.map_settings.textures_path, "Lava.jpg")
                ).convert(),
                (self.map_settings.tile_size, self.map_settings.tile_size),
            ),
        }
        cursor = (0, 0)
        for row in tiles:
            for tile in row:
                if not isinstance(tile, int):
                    grid_image.blit(textures[tile], cursor)
                    triggers.append(_TileTrigger(cursor, self._get_type(tile)))
                else:
                    triggers.append(_TileTrigger(cursor, "link", link=links[str(tile)]))
                cursor = (cursor[0] + self.map_settings.tile_size, cursor[1])
            cursor = (0, cursor[1] + self.map_settings.tile_size)
        cursor = (1, 1)
        for row in enemies_map:
            for tile in row:
                if isinstance(tile, int):
                    enemies.append(
                        Enemy(
                            cursor,
                            ast.literal_eval(enemies_data[str(tile)]["movement"]), # type: ignore
                            enemies_data[str(tile)]["speed"], # type: ignore
                        )
                    )
                cursor = (cursor[0] + 1, cursor[1])
            cursor = (1, cursor[1] + 1)

        return grid_image, triggers, enemies

    def _get_type(self, tile_texture_name: str) -> str:
        match tile_texture_name:
            case " ":  # cave stone
                return "neutral"
            case "-":  # paving stone
                return "neutral"
            case "#":  # civilised rock
                return "obstruction"
            case "~":  # lava
                return "damage"
            case _:
                return "obstruction"
