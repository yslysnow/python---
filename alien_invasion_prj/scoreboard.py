import pygame.font
from pygame.sprite import Group
from ship import Ship

class ScoreBoard:
    """计分板类"""

    def __init__(self,ai_game):
        """初始化记录分数的属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #显示得分信息时使用的字体设置
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,48)

        #准备初始得分图像
        self.prep_score()
        self.prep_highest_score()
        self.prep_level()
        self.prep_ships()


    def prep_score(self):
        """将得分渲染为图像"""
        rounded_score = round(self.stats.score,-1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str,True,self.text_color,self.settings.bg_color)

        #在屏幕右上角显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def prep_highest_score(self):
        """将最高分渲染为图像"""
        rounded_highest_score = round(self.stats.highest_score,-1)
        score_highest_str = f"{rounded_highest_score:,}"
        self.score_highest_image = self.font.render(score_highest_str,True,self.text_color,self.settings.bg_color)

        #在屏幕顶部中央
        self.score_highest_rect = self.score_highest_image.get_rect()
        self.score_highest_rect.centerx = self.screen_rect.centerx
        self.score_highest_rect.top = self.score_rect.top


    def prep_level(self):
        """将等级渲染为图像"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # 在得分最下方显示等级
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10


    def prep_ships(self):
        """显示还剩下多少艘飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * (ship.rect.width + 5)
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """在屏幕上显示得分和最高分,等级和余下的飞船"""
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.score_highest_image, self.score_highest_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_highest_score(self):
        """检查是否诞生了新的最高分"""
        if self.stats.score > self.stats.highest_score:
            self.stats.highest_score = self.stats.score
            self.prep_highest_score()