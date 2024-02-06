import pygame


def camMoved():
    DISPLAY.fill((0, 0, 0))
    xx, yy = 0, 0
    for i in MAP[camx:camx+16]:
        for j in i[camy:camy+16]:
            if j != 'w0':
                if j[0] == 'w':
                    img = pygame.image.load(WALLS[int(j[1:])])
                elif j[0] == 's':
                    img = pygame.image.load(SPRITES[int(j[1:])])
                elif j[0] == 'd':
                    if j[1] == 'p':
                        img = pygame.image.load(DEV[int(j[2]) + 1])
                img = pygame.transform.scale(img, (16, 16))
                DISPLAY.blit(img,
                             img.get_rect(topleft=(xx, yy)))
            xx += 16
        yy += 16
        xx = 0
    pygame.display.update()
    print(f'x0 = {camy}, y0 = {camx}')


WALLS = {

    1: 'data/images/walls/stone.bmp',
    2: 'data/images/walls/blue.bmp',
    3: 'data/images/walls/brick.bmp',
    4: 'data/images/walls/flag.bmp',
    5: 'data/images/walls/blue_metal.bmp',
    6: 'data/images/walls/wood.bmp',
    7: 'data/images/walls/prison.bmp',
    8: 'data/images/walls/prison_dead.bmp',
    9: 'data/images/walls/bad_sign_brick.bmp',
    10: 'data/images/walls/lift_rl.bmp',
    11: 'data/images/walls/lift_ud.bmp',
    12: 'data/images/walls/door_r.bmp',
    13: 'data/images/walls/door_track.bmp',
    14: 'data/images/walls/eagle_wood.bmp',
    15: 'data/images/walls/hitler_wood.bmp',
    16: 'data/images/walls/RR.bmp'

    }

SPRITES = {

    1: 'data/images/sprites/tree.bmp',
    2: 'data/images/sprites/top_lamp.bmp',
    3: 'data/images/sprites/table.bmp',
    4: 'data/images/guns_floor/gun_1.bmp',
    5: 'data/images/sprites/column.bmp',
    6: 'data/images/sprites/blood_pool.bmp',
    7: 'data/images/sprites/skeleton_blood.bmp',
    8: 'data/images/sprites/skeleton.bmp'

    }


DEV = {

    1 : 'data/images/dev/player_left.bmp',
    2 : 'data/images/dev/player_up.bmp',
    3 : 'data/images/dev/player_right.bmp',
    4 : 'data/images/dev/player_down.bmp'

    }


WORLD_SIZE = [120, 120]
camx, camy = 0, 0
DISPLAY = pygame.display.set_mode((256, 256))
MAP = [['w0' for j in range(WORLD_SIZE[0])] for i in range(WORLD_SIZE[1])]

tex = 'w1'

while True:
    
    pygame.time.delay(20)

    for i in pygame.event.get():
        if i == pygame.QUIT:
            break

    if pygame.key.get_pressed()[pygame.K_i]:
        tex = input()

    if pygame.key.get_pressed()[pygame.K_s]:
        wr = open('map.txt', 'w')
        for i in MAP:
            for j in i:
                wr.write(j + ' ')
            wr.write('\n')
        wr.close()

    if pygame.key.get_pressed()[pygame.K_DOWN]:
        if camx < WORLD_SIZE[0] - 16:
            camx += 1
            camMoved()
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        if camy < WORLD_SIZE[1] - 16:
            camy += 1
            camMoved()
    if pygame.key.get_pressed()[pygame.K_UP]:
        if camx > 0:
            camx -= 1
            camMoved()
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        if camy > 0:
            camy -= 1
            camMoved()

    if pygame.key.get_pressed()[pygame.K_r]:
        xx, yy = 0, 0
        camx, camy = 0, 0
        MAP = []
        for i in open('map.txt', 'r').read().split('\n'):
            MAP.append([])
            for j in i.split():
                MAP[-1].append(j)
                if j != 'w0':
                    if j[0] == 'w':
                        img = pygame.image.load(WALLS[int(j[1:])])
                    if j[0] == 's':
                        img = pygame.image.load(SPRITES[int(j[1:])])
                    if j[0] == 'd':
                        if j[1] == 'p':
                            img = pygame.image.load(DEV[int(j[2]) + 1])
                    if xx < 256 and yy < 256:
                        img = pygame.transform.scale(img, (16, 16))
                        DISPLAY.blit(img,
                                     img.get_rect(topleft=(xx, yy)))
                xx += 16
            yy += 16
            xx = 0
        pygame.display.update()

    if pygame.mouse.get_pressed()[0]:
        if 0 < pygame.mouse.get_pos()[0] < 256 and 0 < pygame.mouse.get_pos()[1] < 256:
            MAP[camx + pygame.mouse.get_pos()[1] // 16][camy + pygame.mouse.get_pos()[0] // 16] = tex
            if tex[0] == 'w': 
                img = pygame.image.load(WALLS[int(tex[1:])])
            if tex[0] == 's': 
                img = pygame.image.load(SPRITES[int(tex[1:])])
            if tex[0] == 'd':
                if tex[1] == 'p':
                    img = pygame.image.load(DEV[int(tex[2]) + 1])
            img = pygame.transform.scale(img, (16, 16))
            DISPLAY.blit(img,
                            img.get_rect(topleft=(pygame.mouse.get_pos()[0] // 16 * 16, pygame.mouse.get_pos()[1] // 16 * 16)))
            pygame.display.update()
            
    if pygame.mouse.get_pressed()[2]:
        if 0 < pygame.mouse.get_pos()[0] < 256 and 0 < pygame.mouse.get_pos()[1] < 256:
            MAP[camx + pygame.mouse.get_pos()[1] // 16][camy + pygame.mouse.get_pos()[0] // 16] = 'w0'
            pygame.draw.rect(DISPLAY, (0, 0, 0), (pygame.mouse.get_pos()[0] // 16 * 16, pygame.mouse.get_pos()[1] // 16 * 16, 16, 16))
            pygame.display.update()

