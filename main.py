# initialize pygamejk
import pygame
pygame.mixer.pre_init(44100, -16, 1, 1)
pygame.mixer.init(44100, -16, 1, 512)
print(pygame.mixer.get_init())
pygame.init()

import hashlib
import os
# User modules
import input
import ui.box as box
import ui.button as button
import ui.mapcard as mapcard
import transition

resolution = (1280, 720)
button.init(resolution)
box.init(resolution)
mapcard.init(resolution)

from scenes.title import Title

pygame.mixer.music.load("resources/audio/Chika_White_Calabash.mp3")
pygame.mixer.music.set_endevent(1)
pygame.mixer.music.play()

icon = pygame.image.load("resources/images/icon.png")

def run_game(size, fps, starting_scene):
# initialize pygame window
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption("PyRhythm")
    pygame.display.set_icon(icon)

    active_scene = starting_scene

    while active_scene != None:
        ticks = pygame.time.get_ticks()
        
        pressed_keys = pygame.key.get_pressed()
        # Event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit = False
            if event.type == pygame.QUIT:
                quit = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_F4 and alt_pressed:
                    quit = True
                if event.key == pygame.K_ESCAPE:
                    if active_scene.prev and active_scene.canEscape:
                        active_scene.Terminate()
                        transition.begin(ticks, active_scene.prev)
            elif event.type == 1: # Menu theme end event
                pygame.mixer.music.play()
            elif event.type == 2:
                pygame.mixer.music.unload()
                pygame.mixer.music.load("resources/audio/Chika_White_Calabash.mp3")
                pygame.mixer.music.play()
                
            if quit:
                active_scene = None
            else:
                filtered_events.append(event)
        
        input.update()

        # Trigger scene transition phase
        if transition.active and (transition.getT(pygame.time.get_ticks()) > transition.DURATION):
            active_scene.Terminate()
            active_scene = transition.getTransitionScene()
            
            transition.active = False
        
        if active_scene:
            active_scene.ProcessInput(filtered_events, pressed_keys)
            active_scene.Update()
            active_scene.Render(screen)
        
        transition.draw(screen, ticks)
        
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()

run_game(resolution, 120, Title())