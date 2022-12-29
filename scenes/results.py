import pygame

from scenes.scene import Scene

import ui.button as btn
import input
import background
import transition

btn_back =      btn.Button("Back", (200,40), ((1280-200)/2, 600), color="#1768C4")
font48 = pygame.font.Font(None, 48)
font36 = pygame.font.Font(None, 36)
font30 = pygame.font.Font(None, 30)
font24 = pygame.font.Font(None, 24)

buttons = (btn_back,)

sound_click = pygame.mixer.Sound("resources/audio/click.wav")

judge_name = [
    "GREAT",
    "GOOD",
    "OKAY",
    "MISS"
]
judge_color = [
    '#64C8C8', # Great (Cyan)
    '#64C864', # Good (Green)
    '#C8C864', # Okay (Orange)
    '#C86464', # Miss (Red)
]
class Results(Scene):
    def __init__(self, combo, score, accuracy, judgehit):
        Scene.__init__(self)
        self.playmenuthemeflag = False
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
        self.textsurfs = []
        self.textrects = []
        for i in range(len(judge_name)):
            # Judge name
            surf = font36.render(str(judge_name[i]), True, judge_color[i])
            rect = surf.get_rect(midleft = (300,380+i*40))
            self.textsurfs.append(surf)
            self.textrects.append(rect)
            # Judge Value
            surf = font36.render(str(judgehit[i]), True, '#FFFFFF')
            rect = surf.get_rect(midleft = (400,380+i*40))
            self.textsurfs.append(surf)
            self.textrects.append(rect)

        surf = font48.render('Score:', True, '#FFFFFF')
        rect = surf.get_rect(midleft = (300,230))
        self.textsurfs.append(surf)
        self.textrects.append(rect)
        surf = font48.render(str(score), True, '#FFFFFF')
        rect = surf.get_rect(midleft = (500,230))
        self.textsurfs.append(surf)
        self.textrects.append(rect)

        surf = font48.render('Accuracy:', True, '#FFFFFF')
        rect = surf.get_rect(midleft = (300,280))
        self.textsurfs.append(surf)
        self.textrects.append(rect)
        surf = font48.render(f'{format(100*accuracy,".2f")}%', True, '#FFFFFF')
        rect = surf.get_rect(midleft = (500,280))
        self.textsurfs.append(surf)
        self.textrects.append(rect)

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
        if not self.playmenuthemeflag and ticks - self.creation_time > 1000:
            pygame.mixer.music.unload()
            pygame.mixer.music.load("resources/audio/Chika_White_Calabash.mp3")
            pygame.mixer.music.set_endevent(1)
            self.playmenuthemeflag = True

        if transition.active == False:
            if btn_back.clicked:
                transition.begin(ticks, self.prev)
    
    def Render(self, screen):
        # render background
        t = pygame.time.get_ticks()/1000
        background.draw(screen, t)


        
        screen.blit(self.shadow, self.ui_rect.move(8, 8))
        pygame.draw.rect(screen, "#949AB2", self.ui_rect, border_radius = 4)


        for i in range(len(self.textsurfs)):
            screen.blit(self.textsurfs[i], self.textrects[i])

        # render buttons
        for btn in buttons:
            btn.draw(screen)