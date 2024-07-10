import pygame


class Ship(pygame.sprite.Sprite):
    """管理飞船的类"""
    def __init__(self, ai_games):
        """初始化飞船并设置其初始位置"""
        super(Ship, self).__init__()
        self.screen = ai_games.screen
        self.settings = ai_games.settings
        self.screen_rect = self.screen.get_rect()
        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        # 每艘飞船都放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom
        # 在飞船的属性x中存储一个浮点数
        self.x = float(self.rect.x)
        # 移动标志（飞船一开始不移动）
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志调整飞船的位置"""
        if self.moving_right:
            self.x += self.settings.ship_speed
            if self.rect.right > self.screen_rect.right:
                self.x -= self.settings.ship_speed
        if self.moving_left:
            self.x -= self.settings.ship_speed
            if self.rect.left < self.screen_rect.left:
                self.x += self.settings.ship_speed
        self.rect.x = self.x

    def blitme(self):
        """在指定的位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """将飞船放在屏幕底部的中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
