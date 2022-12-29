import pygame

_t_marker = 0
_t_scene = None
_fade_transition_surf = pygame.Surface((1280,720))

active = False
DURATION = 250

def getTransitionScene():
    return _t_scene

def getT(ticks):
    return ticks - _t_marker
 
def begin(ticks, scene, previous_scene = None):
    global active, _t_marker, _t_scene
    active = True
    _t_marker = ticks
    _t_scene = scene
    if previous_scene:
        _t_scene.prev = previous_scene

def draw(screen, ticks):

    alpha = 1-abs(ticks - _t_marker - DURATION)/DURATION
    alpha = min(1,max(0, alpha))
    _fade_transition_surf.set_alpha(alpha * 255)
    screen.blit(_fade_transition_surf, (0,0))

