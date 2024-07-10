import pygame


class Bullet(pygame.sprite.Sprite):
    """管理飞船所发射子弹的类"""
    def __init__(self, ai_games):
        """在飞船当前位置创建一个子弹对象"""
        super(Bullet, self).__init__()
        self.screen = ai_games.screen
        self.settings = ai_games.settings
        self.color = self.settings.bullet_color
        # 在（0，0,）处创建一个表示子弹的矩形，再射置正确的位置
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_games.ship.rect.midtop
        # 存储用浮点数表示的子弹位置
        self.y = float(self.rect.y)

    def update(self):
        """向上移动子弹"""
        # 更新子弹的准确位置
        self.y -= self.settings.bullet_speed
        # 更新表示子弹的rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
