import pygame as pg
from Configs import *
import random as rn

# wall is just an sprite with no special methods
class Wall(pg.sprite.Sprite):
    def __init__(self, img_path: str, x_y: tuple):
        super().__init__()
        self.image = pg.image.load(img_path)
        self.rect = self.image.get_rect(center=x_y)
               
# bullet is a sprite
class Bulet(pg.sprite.Sprite):
    def __init__(self, img_path: str, x: int, y: int, direction: int):
        super().__init__()
        # direction needs to set bullet's fly direction(setted in degrees)
        self.__direction = direction
        self.image = pg.image.load(img_path)
        self.rect = self.image.get_rect(center=(x, y))
        
    def fly(self):
        # deppends on degree move bullet with bullet speed(should be higher then tanks's speeds)
        if self.__direction == 0:
            self.rect.y -= bulletSPD
        if self.__direction == 90:
            self.rect.x -= bulletSPD
        if self.__direction == -90:
            self.rect.x += bulletSPD
        if self.__direction == 180:
            self.rect.y += bulletSPD


# tank is the main class of the game
class Tank(pg.sprite.Sprite):
    def __init__(self, surface: pg.surface.Surface, tank_img_path: str, bullet_img_path: str, x: int, y: int):
        super().__init__()
        # all of this properties will be used later if you want to understand them now - jast read it's names
        self.image = pg.image.load(tank_img_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.all_bullets = pg.sprite.Group()
        self.__surface = surface
        self.__bullet_img_path = bullet_img_path
        self.__x = x
        self.__y = y
        self.__angle = 0
        self.__bullets_offset = {
                0: (0, -self.image.get_width()//2), 
                90: (-self.image.get_width()//2, 0), 
                -90: (self.image.get_width()//2, 0), 
                180: (0, self.image.get_width()//2)
            }

    # method go moves the tank, but for the first checking for possible wall collision
    # if it is - won't accept to move    
    def go(self, x: int, y: int, walls: pg.sprite.Group):
        self.__new_rect = self.rect.copy()
        self.__new_rect.x += x
        self.__new_rect.y += y
        for wall in walls:
            if wall.rect.colliderect(self.__new_rect):
                return False
        if self.__surface.get_rect().colliderect(self.__new_rect):
            self.__x += x
            self.__y += y
            self.rect = self.__new_rect.copy()
            return False
        else:
            self.__x = 150
            self.__y = self.__surface.get_height()//2
            self.rect.x = 150 - self.image.get_width()//2
            self.rect.y = self.__surface.get_height()//2 - self.image.get_width()//2
            return True
    # drawIt just "draw the tank"    
    def drawIt(self):
        self.__surface.blit(self.image, self.rect)
        self.all_bullets.draw(self.__surface)

    # rotate just rotates the tank with setted direction    
    def rot(self, direction: str):
        self.image = pg.transform.rotate(self.image, angles[direction] -self.__angle)
        self.__angle = angles[direction]

    # shoot is creating bullet and add it to tank's all_bullet group
    def shoot(self):
        x, y = self.__x + self.__bullets_offset[self.__angle][0], self.__y + self.__bullets_offset[self.__angle][1]
        bullet = Bulet(self.__bullet_img_path, x, y, self.__angle)
        self.all_bullets.add(bullet)

# target is just the sprites
class Target(pg.sprite.Sprite):
    def __init__(self, img_path: str, x_y: tuple):
        super().__init__()
        self.image = pg.image.load(img_path)
        self.rect = self.image.get_rect(center=x_y)
