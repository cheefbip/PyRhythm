import os
import json
import pygame
pygame.init()

# Default settings
default_settings =  {
                        'FPS': 120,
                        'FOV': 70,
                        'WINDOW_HEIGHT': 720,
                        'WINDOWS_WIDTH': 1280,
                        'VOLUME_MUSIC': 1,
                        'VOLUME_EFFECT': 1,
                        'LANE_KEYBINDS': [
                            ['SPACE'],
                            ['f', 'j'],
                            ['f','SPACE','j'],
                            ['d','f','j','k'],
                            ['d','f','SPACE','j','k'],
                            ['s','d','f','j','k','l'],
                            ['s','d','f','SPACE','j','k','l'],
                            ['a','s','d','f','h','j','k','l'],
                            ['a','s','d','f','SPACE','h','j','k','l'],
                            ['a','s','d','f','SPACE','RIGHT','KP4','KP5','KP6','KP_ENTER']
                        ],
                        'LANE_COLORS': [
                            ['#fcba03'],
                            ['#03a9fc', '#03a9fc'],
                            ['#03a9fc','#fcba03','#03a9fc'],
                            ['#03a9fc','#ededed','#ededed','#03a9fc'],
                            ['#03a9fc','#ededed','#fcba03','#ededed','#03a9fc'],
                            ['#ededed','#03a9fc','#ededed','#ededed','#03a9fc','#ededed'],
                            ['#ededed','#03a9fc','#ededed','#fcba03','#ededed','#03a9fc','#ededed'],
                            ['#27e84e','#ededed','#03a9fc','#ededed','#ededed','#03a9fc','#ededed','L'],
                            ['#27e84e','#ededed','#03a9fc','#ededed','#fcba03','#ededed','#03a9fc','#ededed','#27e84e'],
                            ['#27e84e','#ededed','#03a9fc','#ededed','#fcba03','#fcba03','#ededed','#03a9fc','#ededed','#27e84e']
                        ]
                    }
settings = None

def save_settings(s):
    with open('config.json', 'w') as settings_file:
        json.dump(s, settings_file, indent=4)  # write to file

# Load settings from file, otherwise, create a new one and save it.
if os.path.exists(os.path.join(os.getcwd(), 'config.json')):
    with open('config.json', 'r') as settings_file:
        settings = {**default_settings, **json.load(settings_file)} # Merge settings
else:
    save_settings(default_settings)