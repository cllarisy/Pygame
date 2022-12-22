import pygame


class Settings():
    def __init__(self):
        self.screen_width = 900
        self.screen_height = 900

        self.movie_screen_width = self.screen_width
        self.movie_screen_height = self.screen_height  # * 0.6
        self.movie_screen_loc_x = (-self.movie_screen_width * 0.5, self.movie_screen_width * 1.5)
        self.movie_screen_loc_y = (-self.movie_screen_height * 0.5, self.movie_screen_height * 1.5)

        self.fresh_area_width = self.movie_screen_width * 3
        self.fresh_area_height = self.movie_screen_height * 3
        self.fresh_area_loc_x = (-self.fresh_area_width / 3, self.fresh_area_width * (2/3))
        self.fresh_area_loc_y = (-self.fresh_area_height / 3, self.fresh_area_height * (2/3))

        pygame.display.set_caption("One World")
        # icon = pygame.image.load('images/a.png')
        # pygame.display.set_icon(icon)
        # self.bg_color=(0,0,0)
        self.fps = 60
        # screen = pygame.display.set_mode((self.screen_width, self.screen_height))
