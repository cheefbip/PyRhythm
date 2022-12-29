import pygame
import math
from colour import Color

# Initialize background variables
left_face =     ((0,1,1), (1,1,1), (1,0,1), (0,0,1))
right_face =    ((1,1,1), (1,1,0), (1,0,0), (1,0,1))
top_face =      ((0,1,0), (1,1,0), (1,1,1), (0,1,1))
colors = ((200,100,100),(100,200,100),(100,100,200))
# orientation index  >>  0: rotation around y-axis; 1: rotation around x-axis
# Order of rotations : YX
rot = [0,0]
rot_mat = ((math.cos(rot[0]), math.sin(rot[0])), (math.cos(rot[1]), math.sin(rot[1])))
fov = math.radians(155)
scale = 1280 / 2 / math.tan(fov * 0.5)
camera = [0, 0, -60] # Position in 3D space
beat = 0
beatUnclamped = 0

def draw(surface, t):
    update_cam(t)
    bgCol = Color(hsl = (.6, 0.2, 0.2))
    surface.fill(bgCol.hex_l)
    faces = []
    xMin = None
    xMax = None
    yMin = None
    yMax = None
    for i, face in enumerate((left_face, right_face, top_face)):
        points = []
        for j, point in enumerate(face):
            x, y = apply_transform(point, (640, 360))
            points.append((x,y))
            if i == 0 and j == 0:
                xMin = x
                xMax = x
                yMin = y
                yMax = y
            else:
                xMin = min(xMin, x)
                xMax = max(xMax, x)
                yMin = min(yMin, y)
                yMax = max(yMax, y)
        faces.append(points)
    pts = ((xMin,yMin),(xMax,yMin),(xMax,yMax),(xMin,yMax))
    # Draw bounding box
    # pygame.gfxdraw.filled_polygon(screen, pts, (100,100,100))

    for face in faces:
        # Loop over points in face
        for i in range(len(face)):
            face[i] = vectorSub(face[i], (xMin,yMin))
    pts = ((xMin,yMin),(xMax,yMin),(xMax,yMax),(xMin,yMax))

    cubeSurface = pygame.Surface((math.floor(xMax - xMin), math.floor(yMax - yMin)))
    cubeSurface = cubeSurface.convert_alpha()
    cubeSurface.fill((0, 0, 0, 0))


    for i, face in enumerate(faces):
        pygame.gfxdraw.filled_polygon(cubeSurface, face, colors[i])

    # cursed code
    """
    # up = vectorSub(faces[0][1], faces[0][2])
    # right = vectorSub(faces[2][0], faces[2][1])
    # left = vectorSub(faces[2][1], faces[2][2])
    screen.blit(cubeSurface, pos)
    screen.blit(cubeSurface, vectorAdd(pos, vectorAdd(left,up)))
    screen.blit(cubeSurface, vectorSub(pos, vectorAdd(left,up)))
    screen.blit(cubeSurface, vectorAdd(pos, vectorAdd(up, right)))
    screen.blit(cubeSurface, vectorSub(pos, vectorAdd(up, right)))
    """
    xstep = math.floor(((beat/2+1)/2)%2)
    ystep = math.floor((beat/2)/2%2)


    beatoffset = ((xstep+(t/2%2))%2, (ystep+(t/4%2))%2)

    pos = vectorAdd((xMin-640, yMin-360),(0,0))
    for i in range(12):
        for j in range(9):
            if (j+i)%2 == 0:
                offset = vectorMult(vectorSub((i,j),beatoffset), scale)
                surface.blit(cubeSurface, vectorAdd(pos, offset))
    
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

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

# 3D-related functions
# Apply rotations to a 3D point based on camera orientation
# Return a 2D vector representing the position on the screen
def apply_transform(vector3, offset = (0,0)):
    x, y, z = vector3
    y_r = rot_mat[0]
    # Rotate points around y-axis
    x, z = complex_mult((x, z), (y_r[0], y_r[1]))
    # Rotate points around transformed x-axis
    x_r = rot_mat[1]
    y, z = complex_mult((y, z), (x_r[0], x_r[1]))
    z_scale = scale
    x *= z_scale
    y *= z_scale
    x += offset[0]
    y += offset[1]
    # Flip y coordinates, so that y is upward.
    y = 720 - y
    return x, y

def update_cam(t):
    global camera, rot, rot_mat, beat, beatUnclamped, colors
    camera = [100*math.cos(t), 0, 100*math.sin(t)]
    beat = ((pygame.mixer.music.get_pos()-15310) * 106/60000)
    beatUnclamped = beat
    beat = clamp(beat, 0, 264)
    colOffset = math.sin(beat/2%1 * math.pi/2)/4
    darken = vectorMult(Color(hsl = (.6, 0.25, 0.50-colOffset)).rgb, 255)
    lighten = vectorMult(Color(hsl = (.6, 0.25, 0.25+colOffset)).rgb, 255)
    colors = (darken, lighten, lighten)

    theta = -math.pi+math.sin(beat/2%1*math.pi/2)*math.pi/2
    if (beat/2 % 2 < 1):
        rot = [theta, 0]
    else:
        rot = [0, theta]
    rot_mat = ((math.cos(rot[0]), math.sin(rot[0])), (math.cos(rot[1]), math.sin(rot[1])))
