import pygame
import math


def cropWall(index):
    return WALL_TILES.subsurface((index % WALL_TILES_COLS * WALL_IMAGE_WIDTH,
                                  index // WALL_TILES_COLS * WALL_IMAGE_HEIGHT,
                                  WALL_IMAGE_WIDTH,
                                  WALL_IMAGE_HEIGHT))

def cropSprite(index):
    return SPRITE_TILES.subsurface((index % SPRITE_TILES_COLS * SPRITE_IMAGE_WIDTH,
                                    index // SPRITE_TILES_COLS * SPRITE_IMAGE_HEIGHT,
                                    SPRITE_IMAGE_WIDTH,
                                    SPRITE_IMAGE_HEIGHT))

def renderSprites(walls):
    screen = []
    sx = 0.; sy = 0.
    sfar = 0.; sdir=0.
    ssize = 0

    for i in SPRITE_MAP.keys():
        i = SPRITE_MAP[i]
        sx = i[0]; sy = i[1]
        sfar = math.sqrt(math.pow(PLAYER_X - sx, 2) + math.pow(PLAYER_Y - sy, 2))
        sdir = math.atan2(sy - PLAYER_Y, sx - PLAYER_X)

        while sdir - PLAYER_ANGLE < -3.14: sdir += 6.28
        while sdir - PLAYER_ANGLE > 3.14: sdir -= 6.28

        ssize = min(1000, int(DISPLAY_HEIGHT / sfar))
        shor = int((sdir - PLAYER_ANGLE + FOV / 2) / FOV_STEP - ssize / 2)
        if shor + ssize >= 0 and shor <= DISPLAY_WIDTH:
            start_scan = shor if shor > 0 else 0
            end_scan = shor + ssize if shor + ssize < DISPLAY_WIDTH else DISPLAY_WIDTH
            for j in walls[start_scan:end_scan]:
                if j[1] > sfar:
                    sver = DISPLAY_HEIGHT // 2 - ssize // 2
                    nobj = SPRITE_DATA[i[2]]
                    if type(nobj) is list:
                        angle = i[3] - PLAYER_ANGLE + .3925

                        while angle < 0: angle += 6.28
                        while angle > 6.28: angle -= 6.28

                        nobj = nobj[int(angle / (6.28 / len(nobj)))]
                    screen.append([1, sfar, nobj, ssize, shor, sver])
                    break
    return screen

def renderWalls():
    screen = []
    angle = PLAYER_ANGLE - FOV / 2
    angleEndPoint = PLAYER_ANGLE + FOV / 2
    cos = .0; sin = .0
    yx = 0; yy = 0; xx = 0; xy = 0
    xdir = False; ydir = False
    xobj = 0; yobj = 0
    xfar = .0; yfar = .0
    ipx = int(PLAYER_X); ipy = int(PLAYER_Y)
    xdelta = 0; ydelta = 0
    xside = False
    far = 0; obj = 0; cut = 0
    count = 0
    isdoor = False
    doorIndex = 0

    while angle < angleEndPoint:
        isdoor = False
        yfar = 0; xfar = 0
        cos = math.cos(angle); sin = math.sin(angle)
        xdir = cos > 0
        ydir = sin > 0

        if sin:
            yy = 0
            if ydir:
                ydelta = PLAYER_Y - int(PLAYER_Y)
                while yfar < 100.:
                    yy += 1
                    yfar = (yy - ydelta) / sin
                    yx = int(PLAYER_X + yfar * cos)
                    if not 0 <= yy + ipy < len(LEVEL_MAP): yfar=100; break
                    if not 0 <= yx < len(LEVEL_MAP[yy + ipy]): yfar=100; break
                    if LEVEL_MAP[yy + ipy][yx]:
                        if LEVEL_MAP[yy + ipy][yx] == DOOR_CODE:
                            isdoor = False
                            doorIndex = 0
                            yfar = (yy + .5 - ydelta) / sin
                            for i in DOOR_MAP:
                                if i[0] == yx and i[1] == yy + ipy:
                                    if i[2] > PLAYER_X + yfar * cos - int(PLAYER_X + yfar * cos):
                                        isdoor = True
                                        doorIndex = DOOR_MAP.index(i)
                                    break
                            if isdoor:
                                break
                        else:
                            break
            else:
                ydelta = PLAYER_Y - int(PLAYER_Y)
                while yfar < 100.:
                    yfar = (yy - ydelta) / sin
                    yy -= 1
                    yx = int(PLAYER_X + yfar * cos)
                    if not 0 <= yy + ipy < len(LEVEL_MAP): yfar=100; break
                    if not 0 <= yx < len(LEVEL_MAP[yy + ipy]): yfar=100; break
                    if LEVEL_MAP[yy + ipy][yx]:
                        if LEVEL_MAP[yy + ipy][yx] == DOOR_CODE:
                            isdoor = False
                            doorIndex = 0
                            yfar = (yy + .5 - ydelta) / sin
                            for i in DOOR_MAP:
                                if i[0] == yx and i[1] == yy + ipy:
                                    if i[2] > PLAYER_X + yfar * cos - int(PLAYER_X + yfar * cos):
                                        isdoor = True
                                        doorIndex = DOOR_MAP.index(i)
                                    break
                            if isdoor:
                                break
                        else:
                            break
        else:
            yfar = 100
        if cos:
            xx = 0
            if xdir:
                xdelta = PLAYER_X - int(PLAYER_X)
                while xfar < 100.:
                    xx += 1
                    xfar = (xx - xdelta) / cos
                    xy = int(PLAYER_Y + xfar * sin)
                    if not 0 <= xy < len(LEVEL_MAP): xfar=100; break
                    if not 0 <= xx + ipx < len(LEVEL_MAP[xy]): xfar=100; break
                    if LEVEL_MAP[xy][xx + ipx]:
                        if LEVEL_MAP[xy][xx + ipx] == DOOR_CODE:
                            isdoor = False
                            doorIndex = 0
                            xfar = (xx + .5 - xdelta) / cos
                            for i in DOOR_MAP:
                                if i[0] == xx + ipx and i[1] == xy:
                                    if i[2] > PLAYER_Y + xfar * sin - int(PLAYER_Y + xfar * sin):
                                        isdoor = True
                                        doorIndex = DOOR_MAP.index(i)
                                    break
                            if isdoor:
                                break
                        else:
                            break
            else:
                xdelta = PLAYER_X - int(PLAYER_X)
                while xfar < 100.:
                    xfar = (xx - xdelta) / cos
                    xx -= 1
                    xy = int(PLAYER_Y + xfar * sin)
                    if not 0 <= xy < len(LEVEL_MAP): xfar=100; break
                    if not 0 <= xx + ipx < len(LEVEL_MAP[xy]): xfar=100; break
                    if LEVEL_MAP[xy][xx + ipx]:
                        if LEVEL_MAP[xy][xx + ipx] == DOOR_CODE:
                            isdoor = False
                            doorIndex = 0
                            xfar = (xx + .5 - xdelta) / cos
                            for i in DOOR_MAP:
                                if i[0] == xx + ipx and i[1] == xy:
                                    if i[2] > PLAYER_Y + xfar * sin - int(PLAYER_Y + xfar * sin):
                                        isdoor = True
                                        doorIndex = DOOR_MAP.index(i)
                                    break
                            if isdoor:
                                break
                        else:
                            break
        else:
            xfar = 100
        xside = xfar < yfar
        if xside:
            far = xfar
            obj = LEVEL_MAP[xy][xx + ipx]
            if xx + ipx < PLAYER_X:
                cut = xy + 1 - PLAYER_Y - far * sin
                if obj == DOOR_CODE:
                    cut = cut - 1 + DOOR_MAP[doorIndex][2]
            else:
                cut = PLAYER_Y + far * sin - xy
                if obj == DOOR_CODE:
                    cut = DOOR_MAP[doorIndex][2] - cut
        else:
            far = yfar
            obj = LEVEL_MAP[yy + ipy][yx]
            if yy + ipy > PLAYER_Y:
                cut = yx + 1 - PLAYER_X - far * cos
                if obj == DOOR_CODE:
                    cut = cut - 1 + DOOR_MAP[doorIndex][2]
            else:
                cut = PLAYER_X + far * cos - yx
                if obj == DOOR_CODE:
                    cut = DOOR_MAP[doorIndex][2] - cut
                    if cut < 0:
                        cut += 1

        screen.append([0, far, obj, count, cut, xside])

        angle += FOV_STEP
        count += 1
    return screen


def draw(screen):
    pygame.draw.rect(display, TOP_FILL, (0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT // 2))
    pygame.draw.rect(display, BOTTOM_FILL, (0, DISPLAY_HEIGHT // 2, DISPLAY_WIDTH, DISPLAY_HEIGHT // 2))
    for i in screen:
        if i[0] == 0:
            height = int(DISPLAY_HEIGHT / i[1] / math.cos(i[3] * FOV_STEP - FOV / 2))
            if height < DISPLAY_HEIGHT:
                sDraw = DISPLAY_HEIGHT // 2 - height // 2
                sCut = 0
                eCut = height
            else:
                sDraw = 0
                sCut = height / 2 - DISPLAY_HEIGHT / 2
                eCut = DISPLAY_HEIGHT
            image = cropWall(i[2] - 1).subsurface((int(WALL_IMAGE_WIDTH * i[4]), 0, 1, WALL_IMAGE_HEIGHT))
            image = pygame.transform.scale(image, (1, height))
            display.blit(image, image.get_rect(topleft=(i[3], sDraw)), (0, sCut, 1, eCut))
        if i[0] == 1:
            image = cropSprite(i[2])
            image = pygame.transform.scale(image, (i[3], i[3]))
            image.set_colorkey((160, 0, 128))
            display.blit(image, image.get_rect(topleft=(i[4], i[5])))
    image = cropSprite(SPRITE_DATA[GUNS_OPTIONS[INVERTORY_CHOOSE][2][INVERTORY[INVERTORY_CHOOSE][1] // GUNS_OPTIONS[INVERTORY_CHOOSE][4]]])
    image = pygame.transform.scale(image, (RESIZE_WEAPON * SPRITE_IMAGE_WIDTH, RESIZE_WEAPON * SPRITE_IMAGE_HEIGHT))
    image.set_colorkey((160, 0, 128))
    display.blit(image, image.get_rect(topleft=(DISPLAY_WIDTH // 2 - SPRITE_IMAGE_WIDTH * RESIZE_WEAPON // 2, DISPLAY_HEIGHT - SPRITE_IMAGE_HEIGHT * RESIZE_WEAPON)))


def move(dx, dy):
    xdir = -1 if dx < 0 else 1
    ydir = -1 if dy < 0 else 1
    nx = PLAYER_X + dx
    ny = PLAYER_Y + dy
    snx, sny = True, True
    if LEVEL_MAP[int(ny)][int(nx)]:
        return PLAYER_X, PLAYER_Y
    for i in SPRITE_MAP.keys():
        i = SPRITE_MAP[i]
        if i[2] in SOLID_SPRITES:
            if i[0] - .5 < nx < i[0] + .5 and\
               i[1] - .5 < ny < i[1] + .5:
                if i[0] - .5 < PLAYER_X < i[0] + .5:
                    snx = False
                if i[1] - .5 < PLAYER_Y < i[1] + .5:
                    sny = False
                break

    if snx and sny:
        if not LEVEL_MAP[int(ny + .3)][int(nx + .3)] and\
            not LEVEL_MAP[int(ny - .3)][int(nx + .3)] and\
            not LEVEL_MAP[int(ny + .3)][int(nx - .3)] and\
            not LEVEL_MAP[int(ny - .3)][int(nx - .3)]:
            return nx, ny
    if snx:
        if not LEVEL_MAP[int(ny + .3)][int(PLAYER_X + .3)] and\
            not LEVEL_MAP[int(ny - .3)][int(PLAYER_X + .3)] and\
            not LEVEL_MAP[int(ny + .3)][int(PLAYER_X - .3)] and\
            not LEVEL_MAP[int(ny - .3)][int(PLAYER_X - .3)]:
            return PLAYER_X, ny
    if sny:
        if not LEVEL_MAP[int(PLAYER_Y + .3)][int(nx + .3)] and\
            not LEVEL_MAP[int(PLAYER_Y + .3)][int(nx - .3)] and\
            not LEVEL_MAP[int(PLAYER_Y - .3)][int(nx + .3)] and\
            not LEVEL_MAP[int(PLAYER_Y - .3)][int(nx - .3)]:
            return nx, PLAYER_Y
    return PLAYER_X, PLAYER_Y


pygame.init()

WALL_TILES = pygame.image.load('data/images/walls.bmp')
WALL_TILES_WIDTH, WALL_TILES_HEIGHT = WALL_TILES.get_size()
WALL_IMAGE_WIDTH, WALL_IMAGE_HEIGHT = 64, 64
WALL_TILES_COLS, WALL_TILES_ROWS = (
                 WALL_TILES_WIDTH // WALL_IMAGE_WIDTH,
                 WALL_TILES_HEIGHT // WALL_IMAGE_HEIGHT)

SPRITE_TILES = pygame.image.load('data/images/sprites.bmp')
SPRITE_TILES_WIDTH, SPRITE_TILES_HEIGHT = SPRITE_TILES.get_size()
SPRITE_IMAGE_WIDTH, SPRITE_IMAGE_HEIGHT = 64, 64
SPRITE_TILES_COLS, SPRITE_TILES_ROWS = (
                   SPRITE_TILES_WIDTH // SPRITE_IMAGE_WIDTH,
                   SPRITE_TILES_HEIGHT // SPRITE_IMAGE_HEIGHT)

SPRITE_DATA = [0,  # plant
               1,  # lamp
               2,  # table
               3, 4, 5, 6, 7, 8, 9, 10,  # stay
               11, 12, 13, 14, 15, 16, 17, 18,   # went 1
               19, 20, 21, 22, 23, 24, 25, 26,   # went 2
               27, 28, 29, 30, 31, 32, 33, 34,   # went 3
               35, 36, 37, 38, 39, 40, 41, 42,   # went 4
               [3, 4, 5, 6, 7, 8, 9, 10],        # 43
               [11, 12, 13, 14, 15, 16, 17, 18], # 44
               [19, 20, 21, 22, 23, 24, 25, 26], # 45
               [27, 28, 29, 30, 31, 32, 33, 34], # 46
               [35, 36, 37, 38, 39, 40, 41, 42], # 47
               43, 44, 45, 46, 47, 48, 49, 50, 51, # hurt / dead | +5
               52, 53, 54, 55, 56,  # gun / clip / heal
               57, 58, 59, 60, 61,  # knife
               62, 63, 64, 65, 66,  # pistol
               67, 68, 69, 70, 71,  # riffle
               72, 73, 74, 75, 76   # machinegun
               ]

SOLID_SPRITES = [0, 2]

SPRITE_MAP = {0: [2.5, 2.5, 0],
              1: [3.5, 2.5, 1],
              2: [4.5, 2.5, 2],
              3: [9.5, 1.5, 43, 0, 100],
              4: [1.5, 1.5, 57]}

SPRITE_ANIMATIONS = [[3, [44, 45, 46, 47], True, 250, 0]]

LEVEL_MAP = [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
             [2, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2],
             [2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2],
             [2, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 2],
             [2, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2],
             [2, 0, 3, 3, 4, 1, 1, 0, 3, 3, 0, 2],
             [2, 0, 3, 1, 0, 1, 1, 0, 2, 3, 0, 2],
             [2, 0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 2],
             [2, 0, 0, 1, 1, 1, 2, 2, 2, 0, 0, 2],
             [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
             [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
             [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]

DOOR_CODE = 4
DOOR_MAP = [[4, 5, .9, -1], [5, 3, .9, -1]]

TOP_FILL, BOTTOM_FILL = (125, 125, 125), (50, 50, 50)

GUNS_OPTIONS = {0: [10, -1, [62, 63, 64, 65, 66], [0, 4], 100, 'Knife.wav', 2, 2],
                1: [10, -1, [67, 68, 69, 70, 71], [0, 4], 100, 'Pistol.wav', 2, 100],
                2: [15, -1, [72, 73, 74, 75, 76], [2, 4], 100, 'Gatling Gun.wav', 2, 100],
                3: [20, -1, [77, 78, 79, 80, 81], [2, 3], 100, 'Machine Gun.wav', 2, 100]}

PLAYER_X, PLAYER_Y, PLAYER_ANGLE = 1.5, 2.5, 6.28
INVERTORY = {0: [True, 0, False], 1: [True, 0, False], 2: [True, 0, False], 3: [True, 0, False]}
INVERTORY_CHOOSE = 3
RESIZE_WEAPON = 2
WEAPON_SOUND = None
FOV, FOV_STEP = 1.2, .00375

DISPLAY_WIDTH, DISPLAY_HEIGHT = 320, 200

for y, i in enumerate(open('map.lev').read().split('e')[0].split('\n')):
    LEVEL_MAP.append([])
    for x, j in enumerate(i.split()):
        if x[0] == 'w':
            LEVEL_MAP[y].append(int(x[1:]))

FOV_STEP = FOV / DISPLAY_WIDTH

display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.DOUBLEBUF)
pygame.mouse.set_visible(0)

fps = 30
clock = pygame.time.Clock()

image = cropWall(0)
#display.blit(image, image.get_rect(topleft=(0, 0)))
renderWalls()
pygame.display.flip()

run = True
screen = []
remove_animations = []

sdir = -1
nangle = 0

while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            run = False

    if SPRITE_ANIMATIONS != []:
        for i in SPRITE_ANIMATIONS:
            if len(i[1]) <= i[4] // i[3]:
                if i[2]:
                    i[4] = 0
                else:
                    remove_animations.append(i)
            if len(i[1]) > i[4] // i[3]:
                SPRITE_MAP[i[0]][2] = i[1][i[4] // i[3]]
                i[4] += int(clock.get_fps() / fps * 30)
    if remove_animations != []:
        for i in remove_animations:
            SPRITE_ANIMATIONS.remove(i)
        remove_animations = []

    if clock.get_fps():
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            PLAYER_ANGLE += 3 / clock.get_fps()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            PLAYER_ANGLE -= 3 / clock.get_fps()

        if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
            PLAYER_X, PLAYER_Y = move(5 / clock.get_fps() * math.cos(PLAYER_ANGLE), 5 / clock.get_fps() * math.sin(PLAYER_ANGLE))
        if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
            PLAYER_X, PLAYER_Y = move(-5 / clock.get_fps() * math.cos(PLAYER_ANGLE), -5 / clock.get_fps() * math.sin(PLAYER_ANGLE))
        if pygame.key.get_pressed()[pygame.K_a]:
            PLAYER_X, PLAYER_Y = move(5 / clock.get_fps() * math.cos(PLAYER_ANGLE - 1.57), 5 / clock.get_fps() * math.sin(PLAYER_ANGLE - 1.57))
        if pygame.key.get_pressed()[pygame.K_d]:
            PLAYER_X, PLAYER_Y = move(5 / clock.get_fps() * math.cos(PLAYER_ANGLE + 1.57), 5 / clock.get_fps() * math.sin(PLAYER_ANGLE + 1.57))

        if pygame.key.get_pressed()[pygame.K_1]:
            INVERTORY_CHOOSE = 0
        if pygame.key.get_pressed()[pygame.K_2]:
            INVERTORY_CHOOSE = 1
        if pygame.key.get_pressed()[pygame.K_3]:
            INVERTORY_CHOOSE = 2
        if pygame.key.get_pressed()[pygame.K_4]:
            INVERTORY_CHOOSE = 3

        if pygame.mouse.get_pressed()[0] or pygame.key.get_pressed()[pygame.K_LCTRL]:
            WEAPON_SOUND = pygame.mixer.Sound(f'data/sounds/{GUNS_OPTIONS[INVERTORY_CHOOSE][5]}')
            INVERTORY[INVERTORY_CHOOSE][2] = True

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            xdoor, ydoor = int(PLAYER_X + 1.3 * math.cos(PLAYER_ANGLE)), int(PLAYER_Y + 1.3 * math.sin(PLAYER_ANGLE))
            for i in DOOR_MAP:
                if i[0] == int(xdoor) and i[1] == int(ydoor):
                    if i[2] == 0: i[3] = 1; i[2] = .000001; LEVEL_MAP[i[1]][i[0]] = DOOR_CODE
                    elif i[2] == 1: i[3] = -1; i[2] = .999999
                    break

        #if pygame.mouse.get_pos()[0] != DISPLAY_WIDTH // 2:
        #    PLAYER_ANGLE += (pygame.mouse.get_pos()[0] - DISPLAY_WIDTH // 2) / clock.get_fps() / 25
        #    pygame.mouse.set_pos(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2)

        if PLAYER_ANGLE < 3.14:
            PLAYER_ANGLE += 6.28
        if PLAYER_ANGLE > 9.42:
            PLAYER_ANGLE -= 6.28

        for i in range(len(DOOR_MAP)):
            if DOOR_MAP[i][2] != 0 and DOOR_MAP[i][2] != 1:
                DOOR_MAP[i][2] += DOOR_MAP[i][3] * .5 / clock.get_fps()
                if DOOR_MAP[i][2] < 0: DOOR_MAP[i][2] = 0; LEVEL_MAP[DOOR_MAP[i][1]][DOOR_MAP[i][0]] = 0
                if DOOR_MAP[i][2] > 1: DOOR_MAP[i][2] = 1

        if INVERTORY[INVERTORY_CHOOSE][2]:
            INVERTORY[INVERTORY_CHOOSE][1] += int(clock.get_fps() / fps * 30)
            if INVERTORY[INVERTORY_CHOOSE][1] // GUNS_OPTIONS[INVERTORY_CHOOSE][4] == GUNS_OPTIONS[INVERTORY_CHOOSE][3][0]:
                WEAPON_SOUND.stop()
                WEAPON_SOUND.play(0)
            if INVERTORY[INVERTORY_CHOOSE][1] // GUNS_OPTIONS[INVERTORY_CHOOSE][4] > GUNS_OPTIONS[INVERTORY_CHOOSE][3][1] and\
               (pygame.mouse.get_pressed()[0] or pygame.key.get_pressed()[pygame.K_LCTRL]):
                INVERTORY[INVERTORY_CHOOSE][1] = GUNS_OPTIONS[INVERTORY_CHOOSE][3][0] * GUNS_OPTIONS[INVERTORY_CHOOSE][4]
                
            if INVERTORY[INVERTORY_CHOOSE][1] // GUNS_OPTIONS[INVERTORY_CHOOSE][4] >= len(GUNS_OPTIONS[INVERTORY_CHOOSE][2]):
                INVERTORY[INVERTORY_CHOOSE][2] = False; INVERTORY[INVERTORY_CHOOSE][1] = 0

            if GUNS_OPTIONS[INVERTORY_CHOOSE][6] == INVERTORY[INVERTORY_CHOOSE][1] // 100 and\
               GUNS_OPTIONS[INVERTORY_CHOOSE][6] != (INVERTORY[INVERTORY_CHOOSE][1] - int(clock.get_fps() / fps * 30)) // 100:
                i = 0
                while i < GUNS_OPTIONS[INVERTORY_CHOOSE][7]:
                    gx = PLAYER_X + i * math.cos(PLAYER_ANGLE)
                    gy = PLAYER_Y + i * math.sin(PLAYER_ANGLE)
                    if 0 <= gy < len(LEVEL_MAP):
                        if 0 <= gx < len(LEVEL_MAP[int(gy)]): 
                            if LEVEL_MAP[int(gy)][int(gx)] != 0:
                                break
                        else:
                            break
                    else:
                        break
                    for j in SPRITE_MAP.keys():
                        if 42 < SPRITE_MAP[j][2] < 48:
                            if SPRITE_MAP[j][0] - .5 < gx < SPRITE_MAP[j][0] + .5 and\
                               SPRITE_MAP[j][1] - .5 < gy < SPRITE_MAP[j][1] + .5:
                                SPRITE_MAP[j][4] -= GUNS_OPTIONS[INVERTORY_CHOOSE][0]
                                SPRITE_MAP[j][2] = 51
                                if SPRITE_MAP[j][4] <= 0:
                                    SPRITE_MAP[j][4] = 0
                                    for s in SPRITE_ANIMATIONS:
                                        if s[0] == j:
                                            SPRITE_ANIMATIONS[SPRITE_ANIMATIONS.index(s)] = [s[0], [53, 54, 55, 56], False, 250, 0]
                                            break
                                i += 2
                    i += .1

    if clock.get_fps() and 42 < SPRITE_MAP[3][2] < 48:
        nex = SPRITE_MAP[3][0] + .5 / clock.get_fps() * sdir
        if LEVEL_MAP[int(SPRITE_MAP[3][1])][int(nex + .5 * sdir)] == 0:
            SPRITE_MAP[3][0] = nex
        else:
            if nangle < 3.14:
                nang = 5 / clock.get_fps()
                nangle += nang
                SPRITE_MAP[3][3] -= nang
                SPRITE_ANIMATIONS[0][3] = 1000000
                SPRITE_MAP[3][2] = 43
            else:
                SPRITE_MAP[3][3] = abs(SPRITE_MAP[3][3])
                nangle = 0
                sdir = -sdir
                SPRITE_ANIMATIONS[0][3] = 250


    clock.tick(fps)
    display.fill((0, 0, 0))
    #for row, i in enumerate(LEVEL_MAP):
    #    for col, j in enumerate(i):
    #        if j:
    #            pygame.draw.rect(display, (0, 0, 125), (col * 16, row * 16, 16, 16))

    screen = renderWalls()
    screen += renderSprites(screen)
    screen.sort(key=lambda i: i[1])
    screen = screen[::-1]
    draw(screen)

    pygame.display.flip()
