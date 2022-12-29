import pygame
import input
from colour import Color

# initialize font module
font = None
def init(size):
    global font
    pygame.font.init()
    pygame.display.set_mode(size)
    font = pygame.font.Font(None, 30)

class Button:
    def __init__(self, text, size, pos, color = '#909090', highlight = None, shadow = True):
        # button rectangle
        self.body_rect = pygame.Rect(pos, size)
        self.body_col = color
        if highlight:
            self.highlight = highlight
        else:
            c = Color(self.body_col)
            c.set_luminance(min(1,c.get_luminance()+0.1))
            self.highlight = c.hex_l

        # button shadow
        self.has_shadow = shadow
        self.shadow = pygame.Surface(size)
        self.shadow = self.shadow.convert_alpha()
        self.shadow.fill((0, 0, 0, 0))
        pygame.draw.rect(self.shadow, (0, 0, 0), pygame.Rect((0,0), size), border_radius = 4)
        self.shadow.set_alpha(64)
        self.shadow_rect = self.body_rect.move(8, 8)

        # text surface/rect
        self.text_surf = font.render(text, True, "#FFFFFF")
        self.text_rect = self.text_surf.get_rect(center = self.body_rect.center)

        # properties
        self.clicked = False

    def draw(self, surface):
        if self == input.get_ui_focus():
            col = self.highlight
        else:
            col = self.body_col
        if self.has_shadow == True:
            surface.blit(self.shadow, self.shadow_rect)
        pygame.draw.rect(surface, col, self.body_rect, border_radius = 4)
        surface.blit(self.text_surf, self.text_rect)

    def mouse_over(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.body_rect.collidepoint(mouse_pos):
            input.set_ui_hover(self)
            return True
        return False
    
    def set_pos(self):
        pass