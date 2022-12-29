'''
Handle loading of individual charts before transitioning to gameplay
'''

import os
import pygame

import config
from scenes.scene import Scene
from scenes.playfield import Playfield
import transition

font48 = pygame.font.Font(None, 48)
font30 = pygame.font.Font(None, 30)
font24 = pygame.font.Font(None, 24)

# Intermission scene
class Intermission(Scene):
    def __init__(self, difficulty):
        Scene.__init__(self)
        self.difficulty = difficulty
        self.canEscape = False
        self.chart = Chart(difficulty)
        self.chart.parsediff()
        self.transitioning = False

        size = 400
        try:
            img = pygame.image.load(difficulty.folder + '\\' + difficulty.coverfile)
        except:
            img = pygame.image.load(os.getcwd() + '\\resources\\images\\coverdefault.png')
        self.cover = pygame.transform.scale(img, (size, size))
        self.cover_rect = pygame.Rect(640-size/2, 360-size/2-50, size, size)

        self.difftext = pygame.font.Font.render(font24, difficulty.diffname, True, "#FFFFFF")
        self.difftextrect = self.difftext.get_rect(center = (640, 625))

        self.songtext = pygame.font.Font.render(font48, difficulty.title, True, "#FFFFFF")
        self.songtextrect = self.songtext.get_rect(center = (640,550))

        self.artisttext = pygame.font.Font.render(font30, difficulty.artist, True, "#FFFFFF")
        self.artisttextrect = self.artisttext.get_rect(center = (640,580))

    # No input
    def ProcessInput(self, events, pressed_keys):
        pass
        
    def Update(self):
        ticks = pygame.time.get_ticks()
        if (self.chart.loaded) and (ticks - self.creation_time > 2000) and (not self.transitioning):
            transition.begin(ticks, Playfield(self.difficulty, self.chart), self.prev)
            self.transitioning = True
    
    def Render(self, screen):
        screen.fill((150, 160, 180))
        screen.blit(self.cover, self.cover_rect)
        screen.blit(self.songtext, self.songtextrect)
        screen.blit(self.artisttext, self.artisttextrect)
        screen.blit(self.difftext, self.difftextrect)




pyr_sections = {
    "[Metadata]"     : 0,
    "[Events]"      : 1,
    "[Timing]"    : 2,
    "[Velocity]"  : 3,
    "[Objects]"      : 4
}

class Track():
    def __init__(self, idx):
        self.index = idx
        self.state = 0
            # 3 = key has been pressed
            # 2 = key is being held down
            # 1 = key has been released
            # 0 = key is idle
        self.keybind = None     # Keybind for track

        self.held = 0           # Whether or not the track is actively holding a long note
        self.heldresult = 0     # Judge result of hitting a long note, stored until its release
        self.notes = []         # Note array
        self.currentnote = 0    # First note
        self.color = (255, 255, 255)       # Note colors
    
    def applysettings(self, keymode):
        self.color = hextorgb(config.settings.get('LANE_COLORS')[keymode-1][self.index])
        #self.keybind = config.settings.get('LANE_KEYBINDS')[keymode-1][self.index]

class CameraEvent():
    def __init__(self, time, eventtype, easetype, pos, rot):
        self.time = time
        self.easetype = easetype
        self.pos = pos
        self.rot = rot

class Note():
    def __init__(self, time, release = None):
        self.time = time
        self.release = release
        self.pos = time
        self.releasepos = release
    
    def setpos(self,hitpos,relpos): # Planned for scrolling velocity
        pass

class Timing():
    def __init__(self, time, beatlength):
        self.time = time
        self.beatlength = beatlength
        
class Velocity():
    def __init__(self, time, vel):
        self.time = time
        self.vel = vel

class Chart():
    def __init__(self, diff):
        self.diff = diff
        self.keymode = None 
        self.tracks = [] # Tracks containing notes
        self.timing = [] # BPM Changes
        self.cameraevents = [] # BPM Changes
        self.velocity = [] # Velocity Changes
        self.endtime = 0
        self.loaded = False
    
    def parsediff(self):
        if self.loaded: return False
        difficulty = self.diff
        pyrpath = difficulty.folder + "\\" + difficulty.pyrfile
        pyrtxt = open(pyrpath, "r", encoding='utf-8-sig')
        section = None
        successful = True
        try:
            i = 0
            for line in pyrtxt:
                i+=1
                try:
                    if line.endswith("\n"):
                        line = line[:-1]
                    if line == "": continue
                    if pyr_sections.get(line) != None:
                        section = pyr_sections.get(line)
                        continue
                    if section == 0:    # .pyr Metadata
                        items = line.split(":",1)
                        md = items[0].strip()
                        if md == "Mode":
                            mode = items[1].strip()
                            if mode[:4].lower() == "keys":
                                self.keymode = int(mode[5:]) # Parse keymode
                                for i in range(self.keymode):
                                    track = Track(i)
                                    track.applysettings(self.keymode)
                                    self.tracks.append(track) # Populate track list
                    elif section == 1:                  # .pyr Events
                        e = line.split(":")
                        time = int(e[0])
                        eventtype = int(e[1])
                        if eventtype == 0:
                            easetype = int(e[2])
                            pos = tuple(map(float, e[3].split(',')))
                            rot = tuple(map(float, e[4].split(',')))
                            self.cameraevents.append(CameraEvent(time,eventtype,easetype,pos,rot))
                        # items = line.split(",",1)
                        # TODO: Implement later
                    elif section == 2:                  # .pyr Timing
                        tp = line.split(",")
                        self.timing.append(Timing(int(tp[0]), float(tp[1])))
                    elif section == 3:                  # .pyr Velocity
                        tp = line.split(",")
                        self.velocity.append(Velocity(int(tp[0]), float(tp[1])))
                    elif section == 4:                  # .pyr Objects
                        obj = line.split(",")
                        time = int(obj[0])
                        lane = int(obj[1])
                        lane = min(max(lane, 0), self.keymode-1)
                        if len(obj) == 3: # long note
                            self.tracks[lane].notes.append(Note(time, int(obj[2])))
                        else: # normal note (default)
                            self.tracks[lane].notes.append(Note(time))
                except:
                    print(f'Error parsing line {i} of file {self.diff.folder}\\{self.diff.pyrfile}: "{line}"')
        except UnicodeDecodeError:
            print("Error parsing file as UTF-8")
            successful = False
        self.loaded = successful
        self.endtime = max(map(lambda x : 0 if (len(x.notes)==0)else (x.notes[-1].release or x.notes[-1].time) ,self.tracks))
        if len(self.cameraevents) == 0:
            self.cameraevents.append(CameraEvent(0,0,0,(0,6,-2), (-0.942477,0,0)))
            self.cameraevents.append(CameraEvent(1000,0,0,(0,6,-2), (-0.942477,0,0)))
        return successful

    def reset(self):
        for track in self.tracks:
            track.state = 0
            track.currentnote = 0
            track.held = 0
            track.heldresult = 0
        
# color related functions
def hextorgb(hex):
    h = hex[1:]
    rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    
    return rgb