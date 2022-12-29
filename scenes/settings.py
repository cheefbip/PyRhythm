import pygame
from scenes.scene import Scene
import background

global time

class Settings(Scene):
    def __init__(self):
        Scene.__init__(self)
    
    def ProcessInput(self, events, pressed_keys):
        pass
        
    def Update(self):
        global time
        time = pygame.time.get_ticks()
    
    def Render(self, screen):
        # render background
        t = time/1000
        background.draw(screen, t)