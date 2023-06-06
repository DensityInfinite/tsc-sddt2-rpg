import pygame, resources.game_settings as game_settings


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        colour: pygame.Color,
        clickable: bool = True,
    ) -> None:
        # Initialise
        pygame.sprite.Sprite.__init__(self)
        self.screen_settings = game_settings.Screen()
        self.colours = game_settings.Colours()
        self.fonts = game_settings.Fonts()
        self.gui_consts = game_settings.GUI()
        self.dev_tools = game_settings.Dev()

        self.dimensions = rect
        self.colour = colour

        self.clickable = clickable
        self.state = "idle"
        self.last_state = "idle"
        self.event = pygame.event.Event(
            self.dev_tools.button_pressed_event, {"index": self}
        )
        self.event_posted = False

        # Image
        self.text_image = self.fonts.button_font.render(
            text, True, self.colours.button_text_colour
        )
        self.coloured_text_image = self.fonts.button_font.render(
            text, True, self.colour
        )
        self.white_text_image = self.fonts.button_font.render(
            text, True, self.colours.white
        )
        self.text_rect = self.text_image.get_rect()
        self.text_rect.center = (
            self.dimensions.width // 2,
            self.dimensions.height // 2,
        )
        self.image: pygame.Surface = pygame.Surface(
            (self.dimensions.width, self.dimensions.height), pygame.SRCALPHA
        )
        pygame.draw.rect(
            self.image,
            self.colour,
            pygame.Rect(0, 0, self.dimensions.width, self.dimensions.height),
            width=2,
            border_radius=self.gui_consts.rounded_corner_radius,
        )
        pygame.draw.rect(
            self.image,
            self.colour,
            pygame.Rect(2, 2, self.dimensions.width - 4, self.dimensions.height - 4),
            border_radius=self.gui_consts.rounded_corner_radius
            - self.gui_consts.inner_corner_decrement,
        )
        self.image.blit(self.text_image, self.text_rect)
        self.image.set_colorkey(self.colours.background_colour)
        self.rect = self.image.get_rect()
        self.rect.center = self.dimensions.topleft

    def update(self, cursor: pygame.sprite.GroupSingle) -> None:
        if self.state == "pressed":
            pygame.draw.rect(
                self.image,
                self.colour,
                pygame.Rect(0, 0, self.dimensions.width, self.dimensions.height),
                width=2,
                border_radius=self.gui_consts.rounded_corner_radius,
            )
            pygame.draw.rect(
                self.image,
                self.colours.background_colour,
                pygame.Rect(
                    2, 2, self.dimensions.width - 4, self.dimensions.height - 4
                ),
                border_radius=self.gui_consts.rounded_corner_radius
                - self.gui_consts.inner_corner_decrement,
            )
            self.image.blit(self.coloured_text_image, self.text_rect)
        elif self.state == "hovered":
            pygame.draw.rect(
                self.image,
                self.colours.white,
                pygame.Rect(0, 0, self.dimensions.width, self.dimensions.height),
                width=2,
                border_radius=self.gui_consts.rounded_corner_radius,
            )
            pygame.draw.rect(
                self.image,
                self.colour,
                pygame.Rect(
                    2, 2, self.dimensions.width - 4, self.dimensions.height - 4
                ),
                border_radius=self.gui_consts.rounded_corner_radius
                - self.gui_consts.inner_corner_decrement,
            )
            self.image.blit(self.text_image, self.text_rect)
        else:
            pygame.draw.rect(
                self.image,
                self.colour,
                pygame.Rect(0, 0, self.dimensions.width, self.dimensions.height),
                width=2,
                border_radius=self.gui_consts.rounded_corner_radius,
            )
            pygame.draw.rect(
                self.image,
                self.colour,
                pygame.Rect(
                    2, 2, self.dimensions.width - 4, self.dimensions.height - 4
                ),
                border_radius=self.gui_consts.rounded_corner_radius
                - self.gui_consts.inner_corner_decrement,
            )
            self.image.blit(self.text_image, self.text_rect)

        self.last_state = self.state
        if pygame.sprite.spritecollide(self, cursor, False) and self.clickable:
            if cursor.sprite.get_button_state():  # type: ignore
                self.state = "pressed"
                self.event_posted = False
            else:
                self.state = "hovered"
                if not self.event_posted and self.last_state == "pressed":
                    pygame.event.post(self.event)
                    self.event_posted = True
        else:
            self.state = "idle"
            self.event_posted = False

    def get_state(self) -> str:
        return self.state


class Text(pygame.sprite.Sprite):
    def __init__(
        self,
        font_name: str,
        text: str,
        pos: tuple[int, int],
        colour: pygame.Color,
        size: int = 25,
        font: pygame.font.Font | None = None,
    ) -> None:
        # Initialise
        pygame.sprite.Sprite.__init__(self)
        self.screen_settings = game_settings.Screen()
        self.colours = game_settings.Colours()
        self.fonts = game_settings.Fonts()

        # Image
        if font is None:
            font = pygame.font.Font(pygame.font.match_font(font_name), size)
        self.image = font.render(text, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = pos


class Cursor(pygame.sprite.Sprite):
    def __init__(self) -> None:
        # Initialise
        pygame.sprite.Sprite.__init__(self)
        self.colours = game_settings.Colours()
        self.dev_tools = game_settings.Dev()

        # Button
        self.button_state: bool = False

        # Position
        self.x = 0
        self.y = 0
        self.image = pygame.Surface(
            (self.dev_tools.cursor_sprite_size, self.dev_tools.cursor_sprite_size),
            pygame.SRCALPHA,
        )
        pygame.draw.ellipse(
            self.image,
            self.colours.white,
            pygame.Rect(0, 0, self.image.get_width(), self.image.get_height()),
        )
        self.image.set_colorkey(self.colours.black)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self, mouse_pos: tuple[int, int]) -> None:
        self.x = mouse_pos[0]
        self.y = mouse_pos[1]
        self.rect.center = (self.x, self.y)

    def register_click(self, pressed: bool) -> None:
        self.button_state = pressed

    def get_button_state(self) -> bool:
        return self.button_state


class Overlay(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect, rounded_corner_radius: int) -> None:
        # Initialise
        pygame.sprite.Sprite.__init__(self)
        self.colours = game_settings.Colours()

        # Image
        self.image: pygame.Surface = pygame.Surface(
            (rect.width, rect.height), pygame.SRCALPHA
        )
        pygame.draw.rect(
            self.image,
            self.colours.grey,
            (0, 0, rect.width, rect.height),
            border_radius=rounded_corner_radius,
        )
        self.rect = self.image.get_rect()
        self.rect.center = rect.topleft
