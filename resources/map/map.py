import pygame, os.path as path
import resources.game_settings as game_settings, resources.utils as utils


class _TileTrigger(pygame.sprite.Sprite):
    def __init__(self, type: str, link=None) -> None:
        # Initialise
        pygame.sprite.Sprite.__init__(self)
        settings = game_settings.Map()

        self.type = type  # neutral, obstruction, damage, link
        self.link = link

        self.rect = pygame.Rect(0, 0, settings.tile_size, settings.tile_size)

    def get_type(self) -> str:
        return self.type


class Grid:
    def __init__(self) -> None:
        self.screen_settings = game_settings.Screen()
        self.map_settings = game_settings.Map()
        self.json_utils = utils.JsonUtils()

    def init_grid(self, grid_id: int) -> tuple[pygame.Surface, list]:
        grid_image = pygame.Surface(self.screen_settings.screen_size)
        triggers = []
        grid_master: dict = self.json_utils.load_from_json(
            self.map_settings.grids_master_path
        )
        grid_path = grid_master[grid_id]["file"]
        grid_file: dict = self.json_utils.load_from_json(grid_path)
        tiles: list = grid_file["tiles"]
        links: dict = grid_file["links"]
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
        for row in tiles:
            cursor = (0, 0)
            for tile in row:
                if tile is not int:
                    grid_image.blit(textures[tile], cursor)
                    triggers.append(_TileTrigger(self._get_type(tile)))
                else:
                    triggers.append(_TileTrigger("link", link=tile))
                cursor = (cursor[0] + self.map_settings.tile_size, cursor[1])
            cursor = (0, cursor[1 + self.map_settings.tile_size])

        return grid_image, triggers

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
