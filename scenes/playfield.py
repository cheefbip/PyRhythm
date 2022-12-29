import pygame
import time
import math
from colour import Color

import config
import input
import ui.button as btn
import transition
from ease import easings
from scenes.scene import Scene
from scenes.results import Results

global rot, rot_mat, fov, camera, curCamEvent, scale
    # orientation index  >>  0: rotation around y-axis; 1: rotation around x-axis
    # Order of rotations : Euler Angles YXZ / Pitch Yaw Roll
clipZ = 1
scrollspeed = 800 # Lerp time in ms
songoffset = 0
dt = 0


combomult = 1
combo = 0
scorecombo = 100
# results
maxcombo = 0
score = 0
accuracy = 0
judge_hit = [
    0,     # 1      Great
    0,     # 1/2    Good
    0,     # 1/4    Okay
    0      # 0 miss, antimash
]
combopulsemarker = 0


font48 = pygame.font.Font(None, 30)
font30 = pygame.font.Font(None, 30)
font24 = pygame.font.Font(None, 24)


btn_resume =      btn.Button("Resume", (200,40), (640-100, 350), color="#1768C4")
btn_retry =      btn.Button("Retry", (200,40), (640-100, 450))
btn_quit =      btn.Button("Quit", (200,40), (640-100, 400))

buttons = (btn_resume, btn_quit, btn_retry)

sound_click = pygame.mixer.Sound("resources/audio/click.wav")
sound_hit = pygame.mixer.Sound("resources/audio/hitsound.wav")
sound_hit.set_volume(0.2)
sound_pause = pygame.mixer.Sound("resources/audio/SynthChime1.wav")

class Playfield(Scene):
    def __init__(self, difficulty, chart):
        Scene.__init__(self)
        self.canEscape = False

        self.difficulty = difficulty
        self.chart = chart

        self.ticks = time.time_ns()//1000000
        self.timebegin = self.ticks + 3000
        self.time = self.ticks - self.timebegin

        self.songplaying = False
        self.chartfinished = False

        self.pausetime = 0
        self.pausestart = 0
        self.paused = False
        self.paused_text = font30.render('PAUSED', True, '#FFFFFF')
        self.paused_text_rect = self.paused_text.get_rect(center = (640,300))

        global combo, combopulsemarker, combomult, scorecombo, score, accuracy, judge_hit, maxcombo
        combo = 0
        maxcombo = 0
        scorecombo = 100
        combomult = 1
        score = 0
        accuracy = 0
        combopulsemarker = 0
        self.comboprev = combo
        self.combotext = font30.render(str(combo), True, '#FFFFFF')
        self.combotext_rect = self.combotext.get_rect(midleft = (20,700))
        self.acctext = font30.render(f'{accuracy}', True, '#FFFFFF')
        self.acctext_rect = self.combotext.get_rect(midleft = (20,700))
        judge_hit = [
            0,     # 1      Great
            0,     # 1/2    Good
            0,     # 1/4    Okay
            0      # 0 miss, antimash
        ]

        self.keycount = chart.keymode
        k = self.keycount
        self.trackkeybinds = []
        cfgbinds = config.settings.get('LANE_KEYBINDS')[k-1]
        for key in cfgbinds:
            self.trackkeybinds.append(getattr(pygame, "K_"+key))
        
        pygame.mixer.music.load(f'{self.difficulty.folder}\\{self.difficulty.audiofile}')

        global rot, rot_mat, fov, camera, curCamEvent, scale
        rot = [-math.pi * 0.35,0,0] # i am so stupid
        rot_mat = ((math.cos(rot[0]), math.sin(rot[0])), (math.cos(rot[1]), math.sin(rot[1])), (math.cos(rot[2]), math.sin(rot[2])))
        fov = math.radians(config.settings.get('FOV') or 70)
        camera = vectorAdd([0,0,-2], [0,k,-k])
        curCamEvent = 0
        scale = 1280 / 2 / math.tan(fov * 0.5)
        
        self.trackpoints = ((-k/2,0,-20),(k/2,0,-20),(k/2,0,100),(-k/2,0,100))
        self.trackfaces = (
            ((-k/2,0,0),(k/2,0,0),(k/2,0,100)),
            ((k/2,0,100),(-k/2,0,100),(-k/2,0,0))
        )
    
    def ProcessInput(self, events, pressed_keys):
        global camera, dt
        timems = time.time_ns()//1000000
        dms = timems - self.ticks
        dt = (dms)/1000
        self.ticks = timems
        
        for event in events:
            if event.type == pygame.KEYDOWN: # Level editor in the future (?)
                if event.key == pygame.K_ESCAPE:
                    if self.time > self.chart.endtime:
                        continue
                    if self.paused:
                        self.pausetime += self.ticks - self.pausestart
                        if self.songplaying:
                            self.timebegin = self.ticks - pygame.mixer.music.get_pos()
                            pygame.mixer.music.unpause()
                        else:
                            self.timebegin = self.creation_time + 3000 + self.pausetime
                    else:
                        self.pausestart = self.ticks
                        if self.songplaying:
                            pygame.mixer.music.pause()
                        sound_pause.play()
                    self.paused = not self.paused
                    
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            if keys[pygame.K_d]: # -x
                camera = vectorAdd(camera, (dt,0,0))
            if keys[pygame.K_a]: # +x
                camera = vectorAdd(camera, (-dt,0,0))
            if keys[pygame.K_e]: # +y
                camera = vectorAdd(camera, (0,dt,0))
            if keys[pygame.K_q]: # -y
                camera = vectorAdd(camera, (0,-dt,0))
            if keys[pygame.K_w]: # +z
                camera = vectorAdd(camera, (0,0,dt))
            if keys[pygame.K_s]: # -z
                camera = vectorAdd(camera, (0,0,-dt))
        
        if self.paused:
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
            if btn_resume.clicked:

                if self.songplaying:
                    self.timebegin = self.ticks - pygame.mixer.music.get_pos() - songoffset
                else:
                    self.timebegin = self.creation_time + 3000 + self.pausetime - songoffset
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.set_pos(self.time/1000)
                self.paused = not self.paused
                #self.pausetime += self.ticks - self.pausestart
                self.time = (self.ticks - self.timebegin) # - self.pausetime
                pygame.mixer.music.unpause()
        else:
            # keyboard inputs
            for i, track in enumerate(self.chart.tracks):
                if keys[self.trackkeybinds[i]]:
                    if track.state < 2:
                        track.state = 3 # Mouse has been clicked
                        #sound_hit.play()
                    else:
                        track.state = 2 # Mouse is being held down
                else:
                    if track.state > 1:
                        track.state = 1 # Mouse has been released
                    else:
                        track.state = 0 # Mouse is idle
            self.time = self.ticks - self.timebegin# - self.pausetime
            
        
    def Update(self):

        if self.time > self.chart.endtime+1000 and not self.chartfinished:
            self.chartfinished = True
            transition.begin(pygame.time.get_ticks(), Results(maxcombo, score, accuracy, judge_hit), self.prev)
            pygame.mixer.music.fadeout(750)
        

        if transition.active == False:
            if btn_retry.clicked:
                pygame.mixer.music.unload()
                self.chart.reset()
                transition.begin(pygame.time.get_ticks(), Playfield(self.difficulty, self.chart), self.prev)
            elif btn_quit.clicked:
                pygame.mixer.music.set_endevent(2)
                pygame.mixer.music.stop()
                transition.begin(pygame.time.get_ticks(), self.prev)

        if self.time - songoffset > 0 and not self.songplaying:
            pygame.mixer.music.play()
            self.timebegin = self.ticks - pygame.mixer.music.get_pos() - songoffset# - self.pausetime
            self.songplaying = True

        if not self.paused:
            for track in self.chart.tracks:
                doRemove(track, self.time)
                if track.state == 3 and track.currentnote < len(track.notes):
                    keyPressed(track, self.time)
                if track.state == 1 and track.currentnote < len(track.notes):
                    keyReleased(track, self.time)
        
        # Hit/release note
        
    
    def Render(self, screen):
        ticks = self.ticks
        if not self.paused:
            update_cam(self.chart.cameraevents, self.time)
        
        # Render background
        bgCol = Color(hsl = (.6, 0.2, 0.2))
        screen.fill(bgCol.hex_l)

        # Render track
        renderquad(screen,self.trackpoints, (25,25,25))

        # Render notes and track receptors
        xoff = -self.chart.keymode/2
        for i, track in enumerate(self.chart.tracks):
            col = track.color
            x0 = xoff + i
            x1 = x0 + 1
            receptor = (
                (x0,0,0),
                (x1,0,0),
                (x1,0,-0.25),
                (x0,0,-0.25),
            )
            trackcol = (200,200,200) if track.state > 1 else (63,63,63)
            renderquad(screen, receptor, trackcol)
            for j in range(track.currentnote, min(track.currentnote + 10, len(track.notes))):
                note =  track.notes[j]
                t = (self.time - note.time) / scrollspeed + 1
                isln = note.release != None
                if j == track.currentnote and track.held:
                    z0 = 0
                    if self.time > note.release:
                        continue
                else:
                    z0 = 10*(1-t) + 0*t
                if isln:
                    t2 = (self.time - note.release) / scrollspeed + 1
                    z1 = 10*(1-t2) + 0*t2
                else:
                    z1 = z0 + 0.5

                quad = (
                    (x0,0,z0),
                    (x1,0,z0),
                    (x1,0,z1),
                    (x0,0,z1)
                )
                renderquad(screen,quad, col)


        # Render UI
        if self.comboprev != combo:
            self.combotext = font30.render(str(combo), True, '#FFFFFF')
            self.combotext_rect = self.combotext.get_rect(midleft = (20,700))
        t = clamp((self.ticks - combopulsemarker)/200, 0, 1)
        t = t * (2-t)
        scaley = 1.5 * (1-t) + t
        scalecombotext = pygame.transform.smoothscale(self.combotext, (self.combotext_rect.size[0],self.combotext_rect.size[1] * scaley))
        scalecomborect = self.combotext.get_rect(midleft = (20, 125))
        global accuracy
        totalhit = sum(judge_hit)
        if totalhit > 0:
            accuracy = sum(map(lambda total, weight: total * weight, judge_hit, judge_weight)) / totalhit / judge_weight[0]
        else:
            accuracy = 1
        self.acctext = font30.render(f'{format(accuracy*100, ".2f")}%', True, '#FFFFFF')
        self.acctext_rect = self.combotext.get_rect(midleft = (20, 85))
        self.scoretext = font30.render(str(self.time), True, '#FFFFFF')
        self.scoretext_rect = self.combotext.get_rect(midleft = (20, 35))

        screen.blit(scalecombotext, scalecomborect)
        screen.blit(self.acctext, self.acctext_rect)
        screen.blit(self.scoretext, self.scoretext_rect)
        self.comboprev = combo

        urbar_update(ticks)
        urbar_draw(screen, ticks)

        if self.paused:
            btn_resume.draw(screen)
            btn_retry.draw(screen)
            btn_quit.draw(screen)
            screen.blit(self.paused_text, self.paused_text_rect)

judgemash = 200 # antimash
judge_window = [
    30,     # 1      Great
    60,     # 1/2    Good
    100,     # 1/4    Okay
]
judge_weight = [
    4,     # 1
    2,     # 1/2
    1,     # 1/4
    0,     # 0, miss
]
judge_score = [
    800,     # 1
    400,     # 1/2
    200,     # 1/4
]
judge_color = [
    (100,200,200), # Great (Cyan)
    (100,200,100), # Good (Green)
    (200,200,100), # Okay (Orange)
    (200,100,100), # Miss (Red)
]
urbar_spawntime = []
urbar_timedelta = []
urbar_color = []

def trackmiss(track):
    global combo, combomult, scorecombo, combopulsemarker
    judge_hit[-1] += 1
    track.currentnote += 1
    track.held = 0
    if combo != 0:
        combopulsemarker = time.time_ns()//1000000
    combo = 0
    combomult = 0.5
    scorecombo = 0

def doRemove(track, t):
    global combo, maxcombo, combomult, scorecombo, combopulsemarker, score
    while (track.currentnote < len(track.notes)):
        n = track.notes[track.currentnote]
        t2 = (n.time if (not track.held) else n.release)
        if (t - t2 > judge_window[-1]):
            if track.held:
                combopulsemarker = time.time_ns()//1000000
                combo += 1
                scorecombo = min(scorecombo+1, 100)
                combomult = (1+scorecombo/100)/2
                maxcombo = max(maxcombo, combo)
                judge_hit[track.heldresult] += 1
                score += math.floor(combomult * judge_score[track.heldresult])
                track.held = False
                track.currentnote+=1
            else:
                trackmiss(track)
        else:
            return

def keyPressed(track, t):
    global combo, maxcombo, combomult, scorecombo, combopulsemarker, score
    i = 0 # judge index
    noteidx = track.currentnote
    notetime = track.notes[noteidx].time
    delta = notetime - t
    while i < len(judge_window):
        if abs(delta) < judge_window[i]:
            urbar_add(delta, i)
            if track.notes[noteidx].release == None:
                track.currentnote += 1
                combo += 1
                scorecombo = min(scorecombo+1, 100)
                combomult = (1+combo/100)/2
                maxcombo = max(maxcombo, combo)
                combopulsemarker = time.time_ns()//1000000
                judge_hit[i] += 1
                score += math.floor(combomult * judge_score[i])
            else:
                track.held = True
                track.heldresult = i
            break
        i += 1
    '''
    if delta < judgemash:
        trackmiss(track)'''

def keyReleased(track, t):
    global combo, maxcombo, scorecombo, combomult, combopulsemarker, score 
    if not track.held:
        return
    noteidx = track.currentnote
    notetime = track.notes[noteidx].release
    delta = notetime - t
    if abs(delta) < judge_window[-1]:
        combopulsemarker = time.time_ns()//1000000
        combo += 1
        scorecombo = min(scorecombo+1, 100)
        combomult = (1+scorecombo/100)/2
        maxcombo = max(maxcombo, combo)
        judge_hit[track.heldresult] += 1
        score += math.floor(combomult * judge_score[track.heldresult])
    else:
        trackmiss(track)
        return

    track.currentnote +=1
    track.held = None

def urbar_add(delta, color):
    urbar_spawntime.append(time.time_ns()//1000000)
    urbar_timedelta.append(delta)
    urbar_color.append(color)
def urbar_update(ticks):
    i = 0
    while i < len(urbar_spawntime):
        if ticks - urbar_spawntime[i] > 4000:
            urbar_spawntime.pop(i)
            urbar_timedelta.pop(i)
            urbar_color.pop(i)
            continue
        i+=1
def urbar_draw(screen, ticks):
    l = pygame.Surface((5,10))
    l.fill((64,64,64))
    screen.blit(l,(640,370), special_flags=pygame.BLEND_ADD)
    for i in range(len(urbar_spawntime)):
        spawntime, delta, color = urbar_spawntime[i], urbar_timedelta[i], urbar_color[i]
        t = (ticks - spawntime)/4000
        l = pygame.Surface((5,10))
        r,g,b = judge_color[color]

        l.fill(vector_lerp(t,(r,g,b),(0,0,0)))
        screen.blit(l,(540+100+delta-2,370),special_flags=pygame.BLEND_ADD)
    
    
    


# Math Functions:
# Takes two tuples representing complex numbers in the form (re, im)
def complex_mult(a, b):
    re = a[0] * b[0] - a[1] * b[1]
    im = a[1] * b[0] + a[0] * b[1]
    return re, im

def vectorAdd(a, b):
    return tuple(map(lambda x, y: x + y, a, b))

def vectorSub(a, b):
    return tuple(map(lambda x, y: x - y, a, b))

def vectorMult(a, s):
    return tuple(map(lambda x: x * s, a))

def vector_lerp(t, a, b):
    return tuple(map(lambda x, y: x*(1-t) + y*t, a, b))

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))



# 3D-related functions

# render a 3d triangle to screen relative to camera
def rendertri(screen, tri, color = (255,255,255)):
    trans = list(map(apply_transform, tri))
    clips = clip_tri(trans)
    for face in clips:
        pts = list(map(projectto2d, face))
        pygame.gfxdraw.filled_polygon(screen, pts, color)

# render a 3d quad to screen relative to camera
def renderquad(screen, quad, color = (255,255,255)):
    A, B, C, D = quad
    rendertri(screen, (A,B,C), color)
    rendertri(screen, (C,D,A), color)

# Return a 2D vector representing the position on the screen
def projectto2d(vector3, offset = (640,-360)):
    x, y, z = vector3
    z_scale = scale / z
    x *= z_scale
    y *= z_scale
    # Flip y coordinates, so that y is upward.
    y = (720 - y)
    x += offset[0]
    y += offset[1]
    return (x, y)

# Apply rotations to a 3D point based on camera orientation
def apply_transform(vector3):
    x, y, z = vectorSub(vector3, camera)
    y_r = rot_mat[1]
    # Rotate points around y-axis
    x, z = complex_mult((x, z), (y_r[0], y_r[1]))
    # Rotate points around transformed x-axis
    x_r = rot_mat[0]
    y, z = complex_mult((y, z), (x_r[0], x_r[1]))
    # Rotate points around transformed z-axis
    z_r = rot_mat[2]
    x, y = complex_mult((x, y), (z_r[0], z_r[1]))
    return (x,y,z)
 
def update_cam(camevents, time):
    global camera, rot, rot_mat, curCamEvent
    while curCamEvent < len(camevents)-1 and time > camevents[curCamEvent+1].time:
        curCamEvent += 1
    c1 = camevents[curCamEvent]
    if curCamEvent == len(camevents)-1:
        camera = c1.pos
        rot = c1.rot
    else:
        c1 = camevents[curCamEvent]
        c2 = camevents[curCamEvent+1]
        t = clamp((time-c1.time)/(c2.time-c1.time),0,1)
        t = easings[c1.easetype](t) # linear easing
        camera = vector_lerp(t, c1.pos, c2.pos)
        rot = vector_lerp(t, c1.rot, c2.rot)

    rot_mat = ((math.cos(rot[0]), math.sin(rot[0])), (math.cos(rot[1]), math.sin(rot[1])), (math.cos(rot[2]), math.sin(rot[2])))

# Returns triangles representing clipped triangle against Z plane
def clip_tri(points):
    global clipZ
    sub = 0
    under = []
    over = []
    for point in points:
        if point[2] < clipZ:
            sub += 1
            under.append(point)
        else:
            over.append(point)
    if sub == 0: # Triangle completely above line
        return (points,)
    elif sub == 1: # One point below line
        A, B, C =   under[0],       over[0],        over[1]
        a, b, c =   clipZ - A[2],   B[2] - clipZ,   C[2] - clipZ
        t1,t2   =   a/(b+a),        a/(c+a)
        P1 = vector_lerp(t1, A, B)
        P2 = vector_lerp(t2, A, C)
        return ((C, P2, B), (B, P2, P1))
    elif sub == 2: # Two points below line
        A, B, C =   over[0],        under[1],       under[0]
        a, b, c =   A[2] - clipZ,   clipZ - B[2],   clipZ - C[2]
        t1,t2   =   a/(b+a),        a/(c+a)
        P1 = vector_lerp(t1, A, B)
        P2 = vector_lerp(t2, A, C)
        return ((A, P1, P2),)
    elif sub == 3: # Triangle out of bounds
        return ()

# color related functions
def hextorgb(hex):
    h = hex[1:]
    rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    
    return rgb