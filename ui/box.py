import pygame

# initialize font module
font = None
def init(size):
    global font
    pygame.font.init()
    pygame.display.set_mode(size)
    font = pygame.font.Font(None, 30)

# UI Box with shadow
class Box:
    def __init__(self, size, pos, color = '#909090', shadow = True):
        # button rectangle
        self.body_rect = pygame.Rect(pos, size)
        self.body_col = color

        # button shadow
        self.has_shadow = shadow
        self.shadow = pygame.Surface(size)
        self.shadow = self.shadow.convert_alpha()
        self.shadow.fill((0, 0, 0, 0))
        pygame.draw.rect(self.shadow, (0, 0, 0), pygame.Rect((0,0), size), border_radius = 4)
        self.shadow.set_alpha(64)
        self.shadow_rect = self.body_rect.move(8, 8)

    def draw(self, surface):
        if self.has_shadow == True:
            surface.blit(self.shadow, self.shadow_rect)
        pygame.draw.rect(surface, self.body_col, self.body_rect, border_radius = 4)
        surface.blit(self.text_surf, self.text_rect)
    
