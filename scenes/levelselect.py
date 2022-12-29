# Python Modules
import pygame
import os
import time
import math
import random
import shutil
#import hashlib storing replays/scores
from glob import glob1

# User modules
import input
import transition
import background
from scenes.scene import Scene
from scenes.intermission import Intermission
#from scenes.editor import Editor
import ui.button as btn
from ui.mapcard import SongCard
from ui.mapcard import DiffCard
from difficulty import Difficulty

random.seed(time.time_ns())
#dirname = os.path.dirname(__file__)

cwd = os.getcwd()
songfolder = cwd + "\\songs"
song_list = [f.path for f in os.scandir(songfolder) if f.is_dir()]
def creatediffs(folder):
    pyrfiles = glob1(folder, "*.pyr")
    return [Difficulty(folder, chartpath) for chartpath in pyrfiles]
difficulty_list = [creatediffs(path) for path in song_list]

sound_click = pygame.mixer.Sound("resources/audio/click.wav")
sound_songselect = pygame.mixer.Sound("resources/audio/SynthChime3.wav")

font30 = pygame.font.Font(None, 30)
font20 = pygame.font.Font(None, 20)

# Create map folder cards
cards = list()
numcards = 10
for i in range(min(len(song_list), numcards)):
    c = SongCard(difficulty_list[i], 90*(i), i)
    cards.append(c)

btn_back = btn.Button("Back", (200,40), ((1280-200)/2, 600), color="#1768C4")
buttons = (btn_back,)

class LevelSelect(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.songfolder = f"{cwd}\\songs"
        self.scrollY = 0 # Current scroll value in pixels (?)
        #idx = random.randrange(0,len(song_list))
        idx = 0
        self.selectedCard = cards[0]
        self.selectedFolderIdx = idx              # Selected song's index
        self.highlightedFolderIdx = idx           # Highlighted song's index
        self.selectedOffset = 0 # Number of difficulties, scrolling past the selected idx will delay scrolling past highlightedIdx by this amount
        self.scrollEaseFrom = 0
        self.scrollEaseTo = 0+90*idx
        self.transformScroll = 0
        self.scrollEaseMarker = pygame.time.get_ticks()
    def ProcessInput(self, events, pressed_keys):
        ticks = pygame.time.get_ticks()
        amtDiffs = len(difficulty_list[self.selectedFolderIdx])
        dy = pygame.mouse.get_rel()[1]

        # Process relevant events
        for event in events:
            if event.type == pygame.DROPFILE: # Level editor in the future (?)
                filepath = event.file
                filename = os.path.basename(filepath)
                fileextension = os.path.splitext(filename)[1]
                print(fileextension)
                if fileextension == ".mp3":
                    basename = os.path.splitext(filename)[0]
                    chartname = f"chart-{time.time_ns() // 1000000}-{basename}"
                    songpath = f'{self.songfolder}\\{chartname}'
                    os.mkdir(songpath)
                    shutil.copy2(filepath, songpath)
            elif event.type == pygame.MOUSEWHEEL:
                self.scrollEaseMarker = ticks
                self.scrollEaseFrom = self.scrollY
                self.scrollEaseTo -=  event.y*90
                self.scrollEaseTo = clamp(self.scrollEaseTo, 0,90*(len(song_list)+amtDiffs))

        if pygame.mouse.get_pressed()[0]:
            self.scrollEaseFrom = clamp(self.scrollEaseFrom - dy, 0,90*(len(song_list)+amtDiffs))
            self.scrollEaseTo = clamp(self.scrollEaseTo - dy, 0,90*(len(song_list)+amtDiffs))

        # UI Input
        input.set_ui_hover(False)
        btns = [*cards,*buttons, *self.selectedCard.children]
        for gui in btns:
            gui.clicked = False
            if gui.mouse_over():
                if input.get_mouse() == 3 or input.get_mouse_right() == 3:
                    input.set_ui_focus(gui)
                    sound_click.play()
                break
            
        if input.get_mouse() < 2:
            if input.get_mouse() == 1 and input.get_ui_focus() == input.get_ui_hover():
                gui = input.get_ui_hover()
                gui.clicked = True
                if gui.__class__ == SongCard:
                    self.scrollEaseMarker = pygame.time.get_ticks()
                    self.scrollEaseFrom = self.scrollY
                    self.scrollEaseTo = gui.scroll
                    self.selectedFolderIdx = gui.idx
                    self.selectedCard = gui
                if gui.__class__ == DiffCard:
                    transition.begin(ticks, Intermission(gui.diff), self)
                    pygame.mixer.music.set_endevent(0)
                    pygame.mixer.music.fadeout(750)
                    sound_songselect.play()
            '''if input.get_mouse_right() == 1 and input.get_ui_focus() == input.get_ui_hover():
                gui = input.get_ui_hover()
                gui.rightclicked = True
                if gui.__class__ == SongCard:
                    self.scrollEaseMarker = pygame.time.get_ticks()
                    self.scrollEaseFrom = self.scrollY
                    self.scrollEaseTo = gui.scroll
                    self.selectedFolderIdx = gui.idx
                    self.selectedCard = gui
                if gui.__class__ == DiffCard:
                    transition.begin(ticks, Editor(gui.diff), self)
                    pygame.mixer.music.set_endevent(0)
                    pygame.mixer.music.fadeout(750)
                    sound_songselect.play()'''
            input.set_ui_focus(None)
    
    def Update(self):
        ticks = pygame.time.get_ticks()
        t = (ticks-self.scrollEaseMarker)/500
        t = min(1, max(0, t))
        t = t * (2-t)
        
        amtDiffs = len(difficulty_list[self.selectedFolderIdx])
        prevMinIdx = clamp(math.floor((self.transformScroll-360)/90), 0, len(song_list)-numcards)
        #prevMaxIdx = math.ceil((self.scrollY+720)/90)
        self.scrollY = self.scrollEaseFrom * (1-t) + self.scrollEaseTo * t
        
        if self.scrollY > (self.selectedFolderIdx + amtDiffs) * 90:
            self.transformScroll = self.scrollY - amtDiffs * 90
        elif self.scrollY > self.selectedFolderIdx * 90:
            self.transformScroll = self.selectedFolderIdx * 90
        else:
            self.transformScroll = self.scrollY 

        minIdx = clamp(math.floor((self.transformScroll-360)/90), 0, len(song_list)-numcards)
        #maxIdx = math.ceil((self.scrollY+720)/90)
        
        # Note: not the most efficient way of shifting through cards
        if minIdx > prevMinIdx:
            for i in range(prevMinIdx, minIdx):
                cards.pop(0)
                cards.append(SongCard(difficulty_list[i+numcards] , 90*(i+numcards), i+numcards)) 
        elif minIdx < prevMinIdx:
            j = 0
            for i in range(minIdx, prevMinIdx):
                cards.pop()
                cards.insert(j, SongCard(difficulty_list[i] , 90*i, i))
                j+=1
            
        
        for c in cards:
            if (c.idx > self.selectedFolderIdx):
                c.setscroll(self.scrollY-amtDiffs * 90)
            else:
                c.setscroll(self.scrollY)

        # Note: this may attempt to update children even when the card may be erased from the array itself, or even replaced by an identical object.
        for d in self.selectedCard.children:
            d.setscroll(self.scrollY)

    def Render(self, screen):
        # render background
        t = pygame.time.get_ticks()/1000
        background.draw(screen, t)
        for c in cards:
            c.draw(screen)
            # Note: this may attempt to render children even when the card may be erased from the array itself, or even replaced by an identical object.
            if self.selectedCard == c:
                for d in c.children:
                    d.draw(screen)

def clamp(x, mn, mx):
    return min(mx, max(mn, x))