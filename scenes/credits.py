import pygame

from scenes.scene import Scene

import ui.button as btn
import input
import background
import transition

btn_back =      btn.Button("Back", (200,40), ((1280-200)/2, 600), color="#1768C4")
font30 = pygame.font.Font(None, 30)
font24 = pygame.font.Font(None, 24)

buttons = (btn_back,)

sound_click = pygame.mixer.Sound("resources/audio/click.wav")

class Credits(Scene):
    def __init__(self):
        Scene.__init__(self)
        pygame.display.set_mode((1280,720))
        pygame.font.init()
        # ui geometry
        self.ui_size = (800,420)
        self.ui_pos = (240,150)
        self.ui_rect = pygame.Rect(self.ui_pos,self.ui_size)
        # ui shadow
        self.shadow= pygame.Surface(self.ui_size)
        self.shadow = self.shadow.convert_alpha()
        self.shadow.fill((0, 0, 0, 0))
        pygame.draw.rect(self.shadow, (0, 0, 0), pygame.Rect((0,0), self.ui_size), border_radius = 4)
        self.shadow.set_alpha(64)
        # text surface/rect
        text = "PROGRAMMING\nSergio Gutierrez (https://github.com/subfluid)\nDESIGN LEAD\nJennifer Tarax\nMENU THEME\nChika - White Calabash\nSOUND EFFECTS\nEric Matyas (soundimage.org)".split("\n")
        self.text_surfs = list()
        self.text_rects = list()
        for i, t in enumerate(text):
            font = font24 if i%2 else font30 
            self.text_surfs.append(font.render(t, True, "#FFFFFF"))
            y_shift = i*30 + i//2*30 - 150
            self.text_rects.append(self.text_surfs[i].get_rect(center = self.ui_rect.center).move(0, y_shift))
        
    def ProcessInput(self, events, pressed_keys):
        input.set_ui_hover(False)
        for btn in buttons:
            btn.clicked = False
            if btn.mouse_over():
                if input.get_mouse() == 3:
                    input.set_ui_focus(btn)
                    sound_click.play()
                break
        if input.get_mouse() < 2:
            if input.get_mouse() == 1 and input.get_ui_focus() == input.get_ui_hover():
                btn = input.get_ui_hover()
                btn.clicked = True
            input.set_ui_focus(None)
    
    def Update(self):
        ticks = pygame.time.get_ticks()
        if transition.active == False:
            if btn_back.clicked:
                transition.begin(ticks, self.prev)
    
    def Render(self, screen):
        # render background
        t = pygame.time.get_ticks()/1000
        background.draw(screen, t)

        
        screen.blit(self.shadow, self.ui_rect.move(8, 8))
        pygame.draw.rect(screen, "#949AB2", self.ui_rect, border_radius = 4)
        for surf, rect in zip(self.text_surfs, self.text_rects):
            screen.blit(surf, rect)

        # render buttons
        for btn in buttons:
            btn.draw(screen)