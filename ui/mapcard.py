import pygame
import input
from glob import glob1
from colour import Color

# initialize font module
font30 = None
font24 = None
def init(size):
    global font30, font24
    pygame.font.init()
    pygame.display.set_mode(size)
    font30 = pygame.font.Font(None, 30)
    font24 = pygame.font.Font(None, 24)

metadata_map = {
    "Title"             : 0,
    "Artist"            : 1,
    "Creator"           : 2,
    "Mode"              : 3,
    "AudioFile"         : 4,
    "CoverFile"         : 5,
    "SongPreviewTime"   : 6,
    "DifficultyName"    : 7,
    "Description"       : 8
}

pyr_sections = {
    "[Metadata]\n"  : 0,
    "[Events]\n"    : 1,
    "[Timing]\n"    : 2,
    "[Velocity]\n"  : 3,
    "[Objects]\n"   : 4
}


# Chart folder song card, uses first song's metadata to determine style
class SongCard():
    def __init__(self, diffs, scroll, idx):
        
        self.idx = idx
        self.diffs = diffs
        if len(diffs) > 0:
            diff = diffs[0]
            self.title = diff.title
            self.artist = diff.artist
            self.audiofile = diff.audiofile
        else:
            self.title = None
            self.artist = None
            self.audiofile = None


        self.body_rect = pygame.Rect(0,0,640,72)
        self.body_col = "#949AB2"
        
        self.title_text_surf = font30.render(self.title or "", True, "#FFFFFF")
        self.title_text_rect = None
        self.artist_text_surf = font24.render(self.artist or "", True, "#FFFFFF")
        self.artist_text_rect = None

        self.shadow = pygame.Surface((640,72))
        self.shadow = self.shadow.convert_alpha()
        self.shadow.fill((0, 0, 0, 0))
        pygame.draw.rect(self.shadow, (0, 0, 0), pygame.Rect((0,0), (640, 72)), border_radius = 4)
        self.shadow.set_alpha(64)
        self.shadow_rect = None

        self.scroll = scroll
        self.y = 0
        self.setscroll(0)

        self.clicked = False
        self.rightclicked = False

        self.children = []
        for i, diff in enumerate(diffs):
            self.children.append(DiffCard(diff, scroll+90*(i+1)))

    def setscroll(self, y):
        px = (self.scroll - y)
        self.y = px + 360
        x = (px/360)**2 
        self.body_rect.midright = (1280+x*50,self.y)
        self.title_text_rect = self.title_text_surf.get_rect(midleft = self.body_rect.midleft).move(12,-20)
        self.artist_text_rect = self.artist_text_surf.get_rect(midleft = self.body_rect.midleft).move(16,0)
        self.shadow_rect = self.body_rect.move(8, 8)

    def mouse_over(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.body_rect.collidepoint(mouse_pos):
            input.set_ui_hover(self)
            return True
        return False

    def draw(self, screen):
        screen.blit(self.shadow, self.shadow_rect)
        pygame.draw.rect(screen, self.body_col, self.body_rect,border_top_left_radius=4, border_bottom_left_radius=4)
        screen.blit(self.title_text_surf, self.title_text_rect)
        screen.blit(self.artist_text_surf, self.artist_text_rect)
    


# Individual Difficulty Card
class DiffCard():
    def __init__(self, difficulty, scroll):

        self.diff = difficulty
        self.title = difficulty.title
        self.artist = difficulty.artist
        self.creator = difficulty.creator
        self.audiofile = difficulty.audiofile
        self.diffname = difficulty.diffname

        self.body_rect = pygame.Rect(0,0,560,72)
        self.body_col = "#233f63"
        
        self.title_text_surf = font30.render(self.diffname or "\\\\", True, "#FFFFFF")
        self.title_text_rect = None
        self.artist_text_surf = font24.render(self.creator or "\\\\", True, "#FFFFFF")
        self.artist_text_rect = None

        self.shadow = pygame.Surface((560,72))
        self.shadow = self.shadow.convert_alpha()
        self.shadow.fill((0, 0, 0, 0))
        pygame.draw.rect(self.shadow, (0, 0, 0), pygame.Rect((0,0), (720, 72)), border_radius = 4)
        self.shadow.set_alpha(64)
        self.shadow_rect = None

        self.scroll = scroll
        self.y = 0
        self.setscroll(0)

        self.clicked = False

    def setscroll(self, y):
        px = (self.scroll - y)
        self.y = px + 360
        x = (px/360)**2 
        self.body_rect.midright = (1280+x*50,self.y)
        self.title_text_rect = self.title_text_surf.get_rect(midleft = self.body_rect.midleft).move(12,-20)
        self.artist_text_rect = self.artist_text_surf.get_rect(midleft = self.body_rect.midleft).move(16,0)
        self.shadow_rect = self.body_rect.move(8, 8)

    def mouse_over(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.body_rect.collidepoint(mouse_pos):
            input.set_ui_hover(self)
            return True
        return False

    def draw(self, screen):
        screen.blit(self.shadow, self.shadow_rect)
        pygame.draw.rect(screen, self.body_col, self.body_rect,border_top_left_radius=4, border_bottom_left_radius=4)
        screen.blit(self.title_text_surf, self.title_text_rect)
        screen.blit(self.artist_text_surf, self.artist_text_rect)
    