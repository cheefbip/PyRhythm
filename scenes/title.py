import pygame

from scenes.scene import Scene
from scenes.levelselect import LevelSelect
from scenes.help import Help
from scenes.credits import Credits
from scenes.settings import Settings

import ui.button as btn
import input
import pygame.gfxdraw
import background
import transition

btn_play =      btn.Button("Play", (200,40), (100, 350), color="#1768C4")
btn_settings =  btn.Button("Settings", (200,40), (100, 400))
btn_help =      btn.Button("Help", (200,40), (100, 450))
btn_credits =      btn.Button("Credits", (200,40), (100, 500))

buttons = (btn_play, btn_settings, btn_help, btn_credits)

sound_click = pygame.mixer.Sound("resources/audio/click.wav")

font96 = pygame.font.Font(None, 96)
icon = pygame.image.load("resources/images/icon.png")
iconrect = icon.get_rect(center = (480,160))

# Title class
class Title(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.titletext = font96.render("PyRhythm", True, "#FFFFFF")
        self.titletextrect = self.titletext.get_rect(center = (720,160))

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
            if btn_play.clicked:
                transition.begin(ticks, LevelSelect(), self)
            elif btn_credits.clicked:
                transition.begin(ticks, Credits(), self)
            elif btn_settings.clicked:
                transition.begin(ticks, Settings(), self)
            elif btn_help.clicked:
                transition.begin(ticks, Help(), self)
    
    def Render(self, screen):
        t = pygame.time.get_ticks()/1000
        
        # render background
        background.draw(screen, t)

        screen.blit(self.titletext, self.titletextrect)
        screen.blit(icon, iconrect)

        # render buttons
        for btn in buttons:
            btn.draw(screen)

        
"""

    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            # Move to the next scene when the user pressed Enter
            self.SwitchToScene(GameScene())
                
"""