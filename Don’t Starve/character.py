from pygame import *
from random import randrange
from math import pow


# --------------------------------人物相关--------------------------------------------------
class Player(sprite.Sprite):
    def __init__(self, settings):
        super().__init__()
        self.image = image.load('images/player.png')
        self.message = image.load('images/message.png')
        self.rect = self.image.get_rect()  # 获取X,Y坐标和大小
        self.rect.x = (settings.movie_screen_width - self.rect.width) / 2
        self.rect.y = (settings.movie_screen_height - self.rect.width) / 3
        self.blood = 100    # 血量
        self.move_able = [1, 1, 1, 1]   # 碰撞后限制移动 分别为上下左右
        self.current_weapon_number = 0      # 当前武器是物品栏的几号位
        self.current_weapon_name = ""   # 武器名称
        self.item_column = sprite.Group()   # 物品栏精灵组
        # 添加一些基本武器
        self.item_column.add(Sword(len(self.item_column)))  # 剑
        self.item_column.add(Aex(len(self.item_column)))    # 斧子
        self.item_column.add(Draft(len(self.item_column)))  # 镐子

    def update(self, pressed_keys, settings, block_elements, screen):
        # 移动控制
        self.move_able = [1, 1, 1, 1]  # 上下左右
        e = self.get_collide_element(block_elements)    # 检测碰撞
        if e:   # 如果返回碰撞元素
            self.collect_item(e, pressed_keys, screen, block_elements)
            # 判断碰撞物体位置，限制角色朝这个方向的移动
            if sprite.collide_rect(self, e):
                if self.rect.y <= e.rect.bottom <= self.rect.bottom:
                    self.move_able[0] = 0  # 上
                elif self.rect.bottom >= e.rect.y >= self.rect.y:
                    self.move_able[1] = 0  # 下
                if self.rect.x <= e.rect.right <= self.rect.right:
                    self.move_able[2] = 0  # 左
                elif self.rect.x <= e.rect.x <= self.rect.right:
                    self.move_able[3] = 0  # 右
        # 按键响应
        keys = [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0]
        for i in range(len(keys)):
            if pressed_keys[keys[i]]:
                self.current_weapon_number = i

    def get_collide_element(self, block_elements):
        for e in block_elements:
            if pow(pow(e.rect.centerx - self.rect.centerx, 2) + pow(e.rect.centery - self.rect.bottom, 2),
                   0.5) < e.volume:
                return e
        return False

    def collect_item(self, e, pressed_keys, screen, block_elements):
        screen.blit(self.message, (self.rect.x - self.rect.width * 1.5, self.rect.y - self.rect.height / 2))
        text = e.action
        text_render = e.font.render(text, True, (0, 0, 0))
        screen.blit(text_render, (self.rect.x - self.rect.width * 1.3, self.rect.y - self.rect.height / 2))
        if pressed_keys[K_SPACE] and (self.current_weapon_name == e.need_weapon or e.need_weapon is None):
            self.item_column.add(e.resource(len(self.item_column)))
            block_elements.remove(e)


# --------------------------------物品相关--------------------------------------------------

class Items(object):  # 物品父类/基类
    def __init__(self, img_path, current_item_nums):  # 当前物品是物品栏中的第几个
        self.number = current_item_nums
        self.name = ""
        self.image = image.load(img_path)
        self.image_frame = image.load('images/cloumn_frame.png')
        self.rect = self.image.get_rect()  # 获取X,Y坐标和大小
        self.rect.x = - 50
        self.rect.y = - 50
        self.rect_item_x = (current_item_nums % 6) * 50 + 605 + 15
        self.rect_item_y = int(current_item_nums / 6) * 50 + 600 + 15

    def update(self, player, screen):  # 当前此物品是物品栏中第几个
        screen.blit(self.image, (self.rect_item_x, self.rect_item_y))
        if self.number == player.current_weapon_number:
            player.current_weapon_name = self.name
            self.rect.x = player.rect.centerx + 15
            self.rect.y = player.rect.centery - 10
            screen.blit(self.image_frame, (self.rect_item_x - 15, self.rect_item_y - 15))
            # screen.blit(self.image, (player.rect.centerx + 15, player.rect.centery - 25))
        else:
            self.rect.x = - 50
            self.rect.y = - 50


class Sword(Items, sprite.Sprite):
    def __init__(self, current_item_nums):
        img_path = 'images/sword.png'
        super(Sword, self).__init__(img_path, current_item_nums)
        sprite.Sprite.__init__(self)
        self.name = "Sword"


class Aex(Items, sprite.Sprite):
    def __init__(self, current_item_nums):
        img_path = 'images/axe.png'
        super(Aex, self).__init__(img_path, current_item_nums)
        sprite.Sprite.__init__(self)
        self.name = "Aex"


class Draft(Items, sprite.Sprite):
    def __init__(self, current_item_nums):
        img_path = 'images/draft.png'
        super(Draft, self).__init__(img_path, current_item_nums)
        sprite.Sprite.__init__(self)
        self.name = "Draft"


class Wood(Items, sprite.Sprite):
    def __init__(self, current_item_nums):
        img_path = 'images/Wood.png'
        super(Wood, self).__init__(img_path, current_item_nums)
        sprite.Sprite.__init__(self)
        self.name = "Wood"


class DryGrass(Items, sprite.Sprite):
    def __init__(self, current_item_nums):
        img_path = 'images/DryGrass.png'
        super(DryGrass, self).__init__(img_path, current_item_nums)
        sprite.Sprite.__init__(self)
        self.name = "DryGrass"


class BreakStone(Items, sprite.Sprite):
    def __init__(self, current_item_nums):
        img_path = 'images/breakstone.png'
        super(BreakStone, self).__init__(img_path, current_item_nums)
        sprite.Sprite.__init__(self)
        self.name = "BreakStone"


# --------------------------------地图元素--------------------------------------------------

class Element(object):  # 地图元素 基类
    def __init__(self, img_path, x_min_max, y_min_max):
        self.name = ""
        self.image = image.load(img_path)
        self.rect = self.image.get_rect()  # 获取X,Y坐标和大小
        self.volume = self.rect.width / 2
        self.rect.x = randrange(x_min_max[0], x_min_max[1])
        self.rect.y = randrange(y_min_max[0], y_min_max[1])
        # 测试代码：
        # ---------------------------------------
        self.font = font.Font('images/MIAO.TTF', 30)
        # ---------------------------------------

    def update(self, screen, pressed_keys, player, block_elements):
        # # 测试代码： 显示坐标
        # # ---------------------------------------
        # text = "x:" + str(self.rect.x) + " y:" + str(self.rect.y)
        # text_render = self.font.render(text, True, (255, 255, 255))
        # screen.blit(text_render, (self.rect.x, self.rect.y))
        # # ---------------------------------------
        if pressed_keys[K_UP]:      # 如果”上“键按下
            if player.move_able[0]:  # 如果玩家当前方向移动未被限制
                self.rect.move_ip(0, 3)  # 更新rect的X,Y
            else:
                self.rect.move_ip(0, -1)  # 更新rect的X,Y
        elif pressed_keys[K_DOWN]:
            if player.move_able[1]:  # 如果玩家当前方向移动未被限制
                self.rect.move_ip(0, -3)  # 更新rect的X,Y
            else:
                self.rect.move_ip(0, 1)  # 更新rect的X,Y
        if pressed_keys[K_LEFT]:
            if player.move_able[2]:  # 如果玩家当前方向移动未被限制
                self.rect.move_ip(3, 0)  # 更新rect的X,Y
            else:
                self.rect.move_ip(-1, 0)  # 更新rect的X,Y
        elif pressed_keys[K_RIGHT]:
            if player.move_able[3]:  # 如果玩家当前方向移动未被限制
                self.rect.move_ip(-3, 0)  # 更新rect的X,Y
            else:
                self.rect.move_ip(1, 0)  # 更新rect的X,Y


class Alives(Element, sprite.Sprite):
    def __init__(self, img_path, x_min_max, y_min_max):
        super(Alives, self).__init__(img_path, x_min_max, y_min_max)
        sprite.Sprite.__init__(self)
        self.volume = self.rect.width
        self.walk_speed = 3
        self.walk_speed_change_lock = False
        self.move_distance = randrange(50, 80)
        self.last_direction = randrange(0, 5)

    def update(self, screen, pressed_keys, player, block_elements):
        # print(self.move_distance)
        if pressed_keys[K_UP]:
            if player.move_able[0]:  # 如果按下的是方向上键
                self.rect.move_ip(0, 3)  # 更新rect的X,Y
            else:
                self.rect.move_ip(0, -0.5)  # 更新rect的X,Y
        elif pressed_keys[K_DOWN]:
            if player.move_able[1]:  # 如果按下的是方向下键
                self.rect.move_ip(0, -3)  # 更新rect的X,Y
            else:
                self.rect.move_ip(0, 0.5)  # 更新rect的X,Y
        if pressed_keys[K_LEFT]:
            if player.move_able[2]:  # 如果按下的是方向左键
                self.rect.move_ip(3, 0)  # 更新rect的X,Y
            else:
                self.rect.move_ip(-0.5, 0)  # 更新rect的X,Y
        elif pressed_keys[K_RIGHT]:
            if player.move_able[3]:  # 如果按下的是方向右键
                self.rect.move_ip(-3, 0)  # 更新rect的X,Y
            else:
                self.rect.move_ip(0.5, 0)  # 更新rect的X,Y
        if self.move_distance > 0:
            result = sprite.spritecollideany(self, block_elements, collided=None)
            if result is not None:
                if result.name != "enemy" and not self.walk_speed_change_lock:
                    self.walk_speed = - self.walk_speed
                    self.walk_speed_change_lock = True

            if self.last_direction == 0:  # 上
                self.rect.move_ip(0, -self.walk_speed)  # 更新rect的X,Y
            elif self.last_direction == 1:  # 右
                self.rect.move_ip(self.walk_speed, 0)  # 更新rect的X,Y
            elif self.last_direction == 2:  # 下
                self.rect.move_ip(0, self.walk_speed)  # 更新rect的X,Y
            elif self.last_direction == 3:  # 左
                self.rect.move_ip(-self.walk_speed, 0)  # 更新rect的X,Y
            self.move_distance -= 1
        else:
            new_direction = randrange(0, 5)
            negative_direction = self.last_direction - 2
            if negative_direction < 0:
                negative_direction = 2
            while new_direction == negative_direction:
                new_direction = randrange(0, 5)
            self.last_direction = new_direction
            self.move_distance = randrange(50, 80)
            self.walk_speed_change_lock = False


class Enemy(Alives):
    def __init__(self, x_min_max, y_min_max):
        img_path = "images/enemy.png"
        super(Enemy, self).__init__(img_path, x_min_max, y_min_max)
        self.name = "enemy"
        self.action = "攻击"
        self.resource = Wood
        self.need_weapon = "Sword"


class Tree(Element, sprite.Sprite):
    def __init__(self, x_min_max, y_min_max):
        img_path = "images/tree0.png"
        super(Tree, self).__init__(img_path, x_min_max, y_min_max)
        sprite.Sprite.__init__(self)
        self.name = "tree"
        self.action = "砍倒"
        self.resource = Wood
        self.need_weapon = "Aex"
        self.volume = self.rect.width / 2
        self.image1 = image.load('images/tree1.png')

        self.rect_1 = self.image1.get_rect()  # 获取X,Y坐标和大小
        self.rect_1.centerx = self.rect.centerx + 5
        self.rect_1.bottom = self.rect.top

    def update(self, screen, pressed_keys, player, block_elements):
        # # 测试代码：
        # # ---------------------------------------
        # text = "x:" + str(self.rect.x) + " y:" + str(self.rect.y)
        # text_render = self.font.render(text, True, (255, 255, 255))
        # screen.blit(text_render, (self.rect.x, self.rect.y))
        # # ---------------------------------------
        screen.blit(self.image1, self.rect_1)
        if pressed_keys[K_UP]:
            if player.move_able[0]:  # 如果按下的是方向上键
                self.rect.move_ip(0, 3)  # 更新rect的X,Y
                self.rect_1.move_ip(0, 3)  # 更新rect的X,Y
            else:
                self.rect.move_ip(0, -1)  # 更新rect的X,Y
                self.rect_1.move_ip(0, -1)  # 更新rect的X,Y
        elif pressed_keys[K_DOWN]:
            if player.move_able[1]:  # 如果按下的是方向下键
                self.rect.move_ip(0, -3)  # 更新rect的X,Y
                self.rect_1.move_ip(0, -3)  # 更新rect的X,Y
            else:
                self.rect.move_ip(0, 1)  # 更新rect的X,Y
                self.rect_1.move_ip(0, 1)  # 更新rect的X,Y
        if pressed_keys[K_LEFT]:
            if player.move_able[2]:  # 如果按下的是方向左键
                self.rect.move_ip(3, 0)  # 更新rect的X,Y
                self.rect_1.move_ip(3, 0)  # 更新rect的X,Y
            else:
                self.rect.move_ip(-1, 0)  # 更新rect的X,Y
                self.rect_1.move_ip(-1, 0)  # 更新rect的X,Y
        elif pressed_keys[K_RIGHT]:
            if player.move_able[3]:  # 如果按下的是方向右键
                self.rect.move_ip(-3, 0)  # 更新rect的X,Y
                self.rect_1.move_ip(-3, 0)  # 更新rect的X,Y
            else:
                self.rect.move_ip(1, 0)  # 更新rect的X,Y
                self.rect_1.move_ip(1, 0)  # 更新rect的X,Y


class Grass(Element, sprite.Sprite):
    def __init__(self, x_min_max, y_min_max):
        img_path = "images/grass.png"
        super(Grass, self).__init__(img_path, x_min_max, y_min_max)
        sprite.Sprite.__init__(self)
        self.name = "grass"
        self.action = "采集"
        self.need_weapon = None
        self.volume = self.rect.width
        self.resource = DryGrass


class Stone(Element, sprite.Sprite):
    def __init__(self, x_min_max, y_min_max):
        img_path = "images/stone.png"
        super(Stone, self).__init__(img_path, x_min_max, y_min_max)
        sprite.Sprite.__init__(self)
        self.name = "stone"
        self.action = "挖掘"
        self.need_weapon = "Draft"
        self.volume = self.rect.width
        self.resource = BreakStone
