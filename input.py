import pygame

# mouse button 1 state
#   0 = idle        (up)
#   1 = released    (up)
#   2 = held        (down)
#   3 = clicked     (down)
mouse_states = [0, 0]


def get_mouse():
    return mouse_states[0]
def get_mouse_left():
    return mouse_states[0]
def get_mouse_right():
    return mouse_states[1]

def update():
    # mouse inputs
    for i in range(len(mouse_states)):
        if pygame.mouse.get_pressed()[i]:
            if mouse_states[i] < 2:
                mouse_states[i] = 3 # Mouse has been clicked
            else:
                mouse_states[i] = 2 # Mouse is being held down
        else:
            if mouse_states[i] > 1:
                mouse_states[i] = 1 # Mouse has been released
            else:
                mouse_states[i] = 0 # Mouse is idle

ui_focus = None
def get_ui_focus():
    return ui_focus
def set_ui_focus(obj):
    global ui_focus
    ui_focus = obj

ui_hover = None
def get_ui_hover():
    return ui_hover
def set_ui_hover(obj):
    global ui_hover
    ui_hover = obj