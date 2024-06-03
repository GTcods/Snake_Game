import pygame


pygame.init()
pygame.font.init()


class Button:
    def __init__(self, x, y, color, text, font, text_color, text_size,
                 outline_width, outline_color, hover_color):
        self.font = pygame.font.SysFont(font, text_size)
        self.text_surface = self.font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect()

        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.text_color = text_color
        self.outline_width = outline_width
        self.outline_color = outline_color
        self.hover_color = hover_color

    def change_text(self, text):
        self.text_surface = self.font.render(text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect()

    def draw_buttons(*buttons, screen):
        for button in buttons:
            button.draw_button(screen)


class RectButton(Button):
    def __init__(self, x, y, width, height, color, text, font, text_color, text_size,
                 outline_width, outline_color, hover_color):
        super().__init__(x, y, color, text, font, text_color, text_size,
                         outline_width, outline_color, hover_color)
        self.width = width
        self.height = height

        self.rect = pygame.Rect(0, 0, width, height)
        self.outline = pygame.Rect(0, 0, width, height)
        self.surface = pygame.Surface((width, height))

        self.text_rect.center = (width // 2, height // 2)

    def check_if_clicked(self, mouse_pos):
        if self.x <= mouse_pos[0] <= self.x + self.width:
            if self.y <= mouse_pos[1] <= self.y + self.height:
                return True
        else:
            return False

    def draw_button(self, surface):
        pygame.draw.rect(self.surface, self.color, self.rect)
        pygame.draw.rect(self.surface, self.outline_color, self.outline, self.outline_width)
        self.text_rect.center = (self.width // 2, self.height // 2)

        if self.hover_color:
            mouse_pos = pygame.mouse.get_pos()
            if self.x <= mouse_pos[0] <= self.x + self.width:
                if self.y <= mouse_pos[1] <= self.y + self.height:
                    pygame.draw.rect(self.surface, self.hover_color, self.rect)
                    pygame.draw.rect(self.surface, self.outline_color, self.outline, self.outline_width)

        self.surface.blit(self.text_surface, self.text_rect)
        surface.blit(self.surface, (self.x, self.y))


class CircleButton(Button):
    def __init__(self, x, y, radius, color, text, font, text_color, text_size,
                 outline_width, outline_color, hover_color, arc_color="white"):
        super().__init__(x, y, color, text, font, text_color, text_size,
                         outline_width, outline_color, hover_color)

        self.radius = radius

        self.arc_color = arc_color
        self.start_angle = 3.14 / 2
        self.stop_angle = - 3.14 * 3 / 2

        self.text_rect.center = (self.x, self.y)

    def check_if_clicked(self, mouse_pos):
        if ((mouse_pos[0] - self.x) ** 2 + (mouse_pos[1] - self.y) ** 2) ** 0.5 <= self.radius:
            return True
        else:
            return False

    def update_arc(self, button):
        if button == 0 and self.stop_angle < 1.57:
            self.stop_angle += 0.2
        elif button == 2 and self.stop_angle >= - 3.14 * 3 / 2:
            self.stop_angle -= 0.2
        if self.stop_angle >= 1.57:
            return True
        else:
            return False

    def draw_button(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

        if self.hover_color:
            mouse_pos = pygame.mouse.get_pos()
            if ((mouse_pos[0] - self.x) ** 2 + (mouse_pos[1] - self.y) ** 2) ** 0.5 <= self.radius:
                pygame.draw.circle(surface, self.hover_color, (self.x, self.y), self.radius)

        pygame.draw.circle(surface, self.outline_color, (self.x, self.y), self.radius, self.outline_width)
        pygame.draw.arc(surface, self.arc_color, (self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2),
                        self.start_angle, self.stop_angle)
        surface.blit(self.text_surface, self.text_rect)
