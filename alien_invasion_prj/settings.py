class Settings:
    """储存游戏《外星人入侵》中所有设置的类"""
    def __init__(self):
        """初始化游戏的静态设置"""
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (129,207,255)

        #飞船的设置
        self.ship_limit = 3

        #子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 6

        #外星人设置
        self.fleet_drop_speed = 10

        #加快游戏节奏的速度，提高外星人分数的速度
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.5
        self.alien_speed = 1.0

        #fleet_direction为1表示向右，为-1表示向左
        self.fleet_direction = 1

        #积分设置
        self.alien_points = 10

    def increase_speed(self):
        """提高速度设置的值"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

