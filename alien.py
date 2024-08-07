import pygame


class Alien(pygame.sprite.Sprite):
    """表示单个外星人的类"""
    def __init__(self, ai_games):
        """初始化外星人并设置其初始位置"""
        super(Alien, self).__init__()
        self.screen = ai_games.screen
        self.setting = ai_games.settings
        # 加载外星人图像并设置其rect属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        # 每个外星人最初都在屏幕的左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # 存储外星人的精确水平位置
        self.x = float(self.rect.x)

    def update(self):
        """向右移动外星飞船"""
        self.x += self.setting.alien_speed*self.setting.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """如果外星舰队位于屏幕边缘,就返回true"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
