from Tanks import *
# every module imports is in the Tank.py file

# Tinitializing pygame, setting window fullscreen and fill background gray
pg.init()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
screen.fill(colors['gray'])

# creating font with defoult fontstile and fontsize 36px
font1 = pg.font.Font(None, 36)
    
# creating group "targets" wich will include all targets
targets = pg.sprite.Group()
# creating function pull wich will clear targets group and then full it with randonly created targets
def pull():
    targets.empty()
    # creating map of all targets
    targetsMap = COMMON_MAP.copy()  # see COMMON_MAP in configs
    for i in range(len(targetsMap)):
        if rn.randrange(15) == 7:   # chance for target to appear in any pos is 1/15
            targetsMap[i] = 1
    row = 0
    # add all targets to the targets group by it's pos in targetsMap
    for i in range(len(targetsMap)):
        if targetsMap[i] == 1:
            targets.add(Target('Sprites\Target.png', MAP[row][i%19]))   # see Tanks.py/class Target
        if i % 19 == 18:
            row += 1
pull()  #doing pull for the fist targets appear

# creating tank wich will be controled by player
tank = Tank(screen, 'Sprites\Tank.png', 'Sprites\Bullet.png', 150, screen.get_height()//2)  # see Tanks.py/class Tank
tank.drawIt()   # see Tanks.py/class Tank/method drawIt
 
# creating list of all tanks(later we'll append there an enemy tank) 
all_tanks = [tank]

# creating group of all walls
walls = pg.sprite.Group()
# creating list of all maps, see Configs.py
maps = [MAP1, MAP2, MAP3, BOSS_MAP]
# creating function new_map wich will:
def new_map(map_blueprint):
    walls.empty()   # clear walls group
    row = 0
    # then add brick walls depends on the maps from configs.py
    for i in range(len(map_blueprint)):
        if map_blueprint[i]:
            walls.add(Wall(wall_path, MAP[row][i%19]))
        if i % 19 == 18:
            row += 1
    # then create and add to the walls group black walls on every adge of 
    # the screen besides right one(next map change)
    for i in range(screen.get_height() // 100 + 1):
        walls.add(Wall(edgeWall_path, (50, 50 + 100*i)))
    for i in range((screen.get_width() - 100) // 100 + 2):
        walls.add(Wall(edgeWall_path, (50 + i*100, 50)))
        walls.add(Wall(edgeWall_path, (50 + i*100, screen.get_height() - 30)))
new_map(maps[0])    # doing new_map for the first map


# preparing before main loop
clock = pg.time.Clock() # clock to lock the FPS
run = True # standart run bool
# and some variable wich will be used later
score = 0
map_num = 0
map_change = False
ticks = 0
while run:
    clock.tick(FPS) # lock the FPS

    # looking for every event
    for event in pg.event.get():
        # exit the game whenever windows get closed or escape key gets pressed
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                run = False
        
        # turning player's tank when he press buttons WASD
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                tank.rot('up')  # see Tanks.py/class Tank/method rot
            elif event.key == pg.K_a:
                tank.rot('left')
            elif event.key == pg.K_d:
                tank.rot('right')
            elif event.key == pg.K_s:
                tank.rot('down')
        # if player click LMB or press space key - tank shoots
        if event.type == pg.MOUSEBUTTONDOWN or (event.type == pg.KEYDOWN and event.key == pg.K_SPACE):
            tank.shoot()    # see Tanks.py/class Tank/method shoot

    # looking for all pressed buttons
    keys = pg.key.get_pressed()
    # if there's only one key pressed(besides space) - tank moves with WASD controls
    if keys.count(True) - keys[pg.K_SPACE] <= 1:
        if keys[pg.K_w]:
            if tank.go(0, -10, walls):  # see Tanks.py/class Tank/method go
                map_change = True
        if keys[pg.K_a]:
            if tank.go(-10, 0, walls):
                map_change = True
        if keys[pg.K_s]:
            if tank.go(0, 10, walls):
                map_change = True
        if keys[pg.K_d]:
            if tank.go(10, 0, walls):
                map_change = True
    
    # for all tanks
    for i in all_tanks:
        for bullet in i.all_bullets:    # for all it's bullets
            bullet.fly()    # see Tanks.py/class Bullet/method fly()
            # looking for bulet + walls/targets collision and if it
            # collide - remove bullet and(maybe) target
            if not screen.get_rect().colliderect(bullet.rect):
                i.all_bullets.remove(bullet)    # if bullet got out of screen - remove it
            for target in targets:
                if target.rect.colliderect(bullet.rect):
                    targets.remove(target)
                    i.all_bullets.remove(bullet)
                    score += 1  # if it was target - score is increses
            for wall in walls:
                if wall.rect.colliderect(bullet.rect):
                    i.all_bullets.remove(bullet)
    # if map got changed(see Tanks.py/class Tank/method go) - we change the map with previous functions
    if map_change:
        if map_num < len(maps) - 2:
            map_num += 1
        else:
            # if it's lact(boss) map - creating an enemy tank
            enemy_tank = Tank(screen, 'Sprites\EnemyTank.png', 'Sprites\EnemyTarget.png', 1400, screen.get_height()//2)
            all_tanks.append(enemy_tank)
            enemy_tank.rot('right')
            map_num += 1
        pull()
        new_map(maps[map_num])
        map_change = False

    # recolor background(for clear every outtime sprites from screen)
    screen.fill(colors['gray'])
    # draw all targets and walls
    targets.draw(screen)
    walls.draw(screen)
    # draw player's tank and enemy tank if it is last map now
    tank.drawIt()
    if map_num == len(maps) - 1:
        enemy_tank.drawIt()
        # for every 1.5s enemy tank shoots
        ticks += 1
        if ticks == int(FPS * 1.5):
            enemy_tank.shoot()
            ticks = 0
    # add score counter to the left top side of the screen    
    score_render = font1.render(f'Your SCORE: {score}', True, colors['white'])
    screen.blit(score_render, (50, 50))

    # flipping the screen(it's better then update, more )
    pg.display.flip()

# if main loop is ended - quit out the game and end the script
pg.quit()
