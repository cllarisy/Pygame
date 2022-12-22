import random
import pygame
import time
import sys

from settings import Settings
import character

pygame.init()

settings = Settings()
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))  # 屏幕分辨率

background = pygame.image.load('images/background.png')
status_menu = pygame.image.load('images/status_menu.png')
player_point = pygame.image.load('images/player_point.png')
tree_point = pygame.image.load('images/tree_point.png')
player = character.Player(settings)

role = pygame.sprite.Group()  # 环境元素
# role.add(player)

# block_elements = []     # 加载区块内的元素

# screen_elements = pygame.sprite.Group()     # 屏幕内的元素

# block_elements = pygame.sprite.Group()
# block_elements = pygame.sprite.LayeredUpdates()
block_elements = pygame.sprite.OrderedUpdates()
clock = pygame.time.Clock()


def create_map_elements(nums, x_min_max, y_min_max):  # 需要生成的元素数量、生成x的最大最小值元组、生成y的最大最小值元组
    weight = [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3]
    elements = {0: character.Grass, 1: character.Tree, 2: character.Stone, 3: character.Enemy}
    index = []
    for i in range(0, int(nums)):
        rus = random.choice(weight)  # 随机选取并生成一个元素
        index.append(rus)
    index.sort()
    for i in index:
        temp = elements[i]((x_min_max[0], x_min_max[1]), (y_min_max[0], y_min_max[1]))
        block_elements.add(temp)
        # if i == 0:
        #     temp = character.Grass((x_min_max[0], x_min_max[1]), (y_min_max[0], y_min_max[1]))
        #     block_elements.add(temp)
        #     # print("add grass x:" + str(temp.rect.x) + " y:" + str(temp.rect.y))
        #
        # elif i == 1:
        #     temp = character.Tree((x_min_max[0], x_min_max[1]), (y_min_max[0], y_min_max[1]))
        #     block_elements.add(temp)
        #     # print("add tree  x:" + str(temp.rect.x) + " y:" + str(temp.rect.y))
        #
        # elif i == 2:
        #     temp = character.Stone((x_min_max[0], x_min_max[1]), (y_min_max[0], y_min_max[1]))
        #     block_elements.add(temp)
        #
        # elif i == 3:
        #     temp = character.Enemy( (x_min_max[0], x_min_max[1]), (y_min_max[0], y_min_max[1]) )
        #     block_elements.add(temp)


def init():
    create_map_elements(settings.fresh_area_width ** 0.5, (settings.fresh_area_loc_x[0], settings.fresh_area_loc_x[1]),
                        (settings.fresh_area_loc_y[0], settings.fresh_area_loc_y[1]))


def block_fresh(pressed_keys):
    if pressed_keys[pygame.K_UP]:  # 通过人物移动方向 ，来进行地图刷新
        for e in block_elements:
            if e.rect.y > settings.fresh_area_loc_y[1]:
                block_elements.remove(e)
                create_map_elements(1, (settings.fresh_area_loc_x[0], settings.fresh_area_loc_x[1]),
                                    (settings.fresh_area_loc_y[0], settings.movie_screen_loc_y[0]))
    elif pressed_keys[pygame.K_DOWN]:
        for e in block_elements:
            if e.rect.y < settings.fresh_area_loc_y[0]:
                block_elements.remove(e)
                create_map_elements(1, (settings.fresh_area_loc_x[0], settings.fresh_area_loc_x[1]),
                                    (settings.movie_screen_loc_y[1], settings.fresh_area_loc_y[1]))
    if pressed_keys[pygame.K_LEFT]:
        for e in block_elements:
            if e.rect.x > settings.fresh_area_loc_x[1]:
                block_elements.remove(e)
                create_map_elements(1, (settings.fresh_area_loc_x[0], settings.movie_screen_loc_x[0]),
                                    (settings.fresh_area_loc_y[0], settings.fresh_area_loc_y[1]))
    elif pressed_keys[pygame.K_RIGHT]:
        for e in block_elements:
            if e.rect.x < settings.fresh_area_loc_x[0]:
                block_elements.remove(e)
                create_map_elements(1, (settings.movie_screen_loc_x[1], settings.fresh_area_loc_x[1]),
                                    (settings.fresh_area_loc_y[0], settings.fresh_area_loc_y[1]))


def map_fresh():
    screen.blit(player_point, (270 / 2, 760))
    tree_point_rect = tree_point.get_rect()
    for e in block_elements:
        if e.name != "grass":
            tree_point_rect.x = (274 / settings.fresh_area_width) * e.rect.x + 102
            tree_point_rect.y = (300 / settings.fresh_area_height) * e.rect.y + 724
            screen.blit(tree_point, tree_point_rect)
            # font = pygame.font.SysFont('arial', 20)
            # text = "x:" + str(e.rect.x) + " y:" + str(e.rect.y)
            # text_render = font.render(text, True, (255, 255, 255))
            # screen.blit(text_render, (tree_point_rect.x, tree_point_rect.y))


def get_fps(passed_time):
    if passed_time <=0 :
        passed_time = 1
    return int(1/passed_time*1000)


def mainloop():     # 主循环
    while True:
        timer = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        screen.fill((153, 204, 0))
        pressed_key = pygame.key.get_pressed()  # 获取按住的按键
        player.update(pressed_key, settings, block_elements, screen)   # 人物更新（移动部分
        # role.update(screen, player, pressed_key, block_elements)
        # screen.blit(background, (0, 0))
        block_fresh(pressed_key)   	# 边界元素刷新
        block_elements.draw(screen) 	# 环境元素绘制
        role.draw(screen)   # 应该没用
        screen.blit(player.image, (player.rect.x, player.rect.y))   # 绘制主人公
        player.item_column.draw(screen)     # 绘制物品栏
        block_elements.update(screen, pressed_key, player, block_elements) 	# 环境元素更新
        screen.blit(status_menu, (0, 600))    # 绘制下方属性栏
        player.item_column.update(player, screen)      # 绘制更新物品栏
        map_fresh()   	# 更新地图
        # block_show.update(screen, pressed_key)

        pygame.display.update()
        passed_time = clock.tick(settings.fps)
        fps = get_fps(passed_time)
        print("fps:"+str(fps))
init()
mainloop()
