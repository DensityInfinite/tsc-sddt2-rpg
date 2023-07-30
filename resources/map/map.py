import pygame, os.path as path
import resources.game_settings as game_settings, resources.utils as utils

class Map:
    def __init__(self) -> None:
        self.screen_settings = game_settings.Screen()
        self.map_settings = game_settings.Map()
        self.json_utils = utils.JsonUtils()

    def init_grid(self, grid_id: int):
        grid = pygame.Surface(self.screen_settings.screen_size)
        grid_master: dict = self.json_utils.load_from_json(self.map_settings.grids_master_path)
        grid_path = grid_master[grid_id]["file"]
        grid_file: dict = self.json_utils.load_from_json(grid_path)
        tiles: list = grid_file["tiles"]
        links: dict = grid_file["links"]
        textures = {
            "cave stone": pygame.transform.scale(pygame.image.load(path.join(self.map_settings.textures_path, "Cave Rocks.jpg")).convert(), (self.map_settings.tile_size, self.map_settings.tile_size)),
            "civilised rocks": pygame.transform.scale(pygame.image.load(path.join(self.map_settings.textures_path, "Civilised Rock.jpg")).convert(), (self.map_settings.tile_size, self.map_settings.tile_size)),
            "track": pygame.transform.scale(pygame.image.load(path.join(self.map_settings.textures_path, "Paving Stones.jpg")).convert(), (self.map_settings.tile_size, self.map_settings.tile_size)),
        }
        for row in tiles:
            cursor = (0, 0)
            for tile in row:
                grid.blit(textures[tile], cursor)
                cursor = (cursor[0] + self.map_settings.tile_size, cursor[1])
            cursor = (0, cursor[1 + self.map_settings.tile_size])

class _TileTrigger(pygame.sprite.Sprite):
    def __init__(self) -> None:
        # Initialise
        pygame.sprite.Sprite.__init__(self)
        settings = game_settings.Map()

        self.type = "neutral"               # neutral, obstruction, damage

        self.rect = pygame.Rect(0, 0, settings.tile_size, settings.tile_size)

    def get_type(self) -> str:
        return self.type