class Settings:
    """存储游戏“外星人入侵”里的所有设置的类"""
    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕的设置
        self.alien_points = None
        self.fleet_direction = None
        self.alien_speed = None
        self.bullet_speed = None
        self.ship_speed = None
        self.screen_width = 1200  # 屏幕的宽度
        self.screen_height = 700  # 屏幕的高度
        self.bg_color = (230, 230, 230)  # 屏幕填充的颜色
        # 飞船的设置
        self.ship_limit = 3  # 初始飞船的个数，也可以理解为生命值
        # 子弹的设置
        self.bullet_width = 3000  # 设置子弹的宽度
        self.bullet_height = 15  # 设置子弹的高度
        self.bullet_color = (60, 60, 60)  # 设置子弹的颜色
        self.bullets_allowed = 3  # 设置最多允许存在的子弹数量
        # 外星飞船的设置
        self.fleet_drop_speed = 100
        # 以什么速度加快游戏的节奏
        self.speedup_scale = 1.1
        # 外星人分数的提高速度
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 1.5
        self.bullet_speed = 2.0  # 设置子弹的速度
        self.alien_speed = 1.0
        # self.fleet_direction为1表示向右移动，为-1表示向左移动
        self.fleet_direction = 1
        # 每次击落外星飞船的得分
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置的值和外星飞船分数"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
