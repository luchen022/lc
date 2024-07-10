import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_states import GameStates
from button import Button
from scoreboard import ScoreBoard


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        self.settings = Settings()
        self.size = (self.settings.screen_width, self.settings.screen_height)
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('外星人入侵')
        self.bg_color = self.settings.bg_color
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # 创建一个用于存储游戏统计信息的实例
        self.states = GameStates(self)
        self.sb = ScoreBoard(self)
        # 游戏启动后处于活动状态
        self.game_active = False
        # 创建Play 按钮
        self.play_button = Button(self, "Play")

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()  # 检测用户操作，并判断是否添加子弹

            if self.game_active:
                pygame.mouse.set_visible(False)
                self.ship.update()  # 根据操作改变飞船的位置
                self._update_bullets()  # 更新子弹
                self._update_aliens()
            else:
                pygame.mouse.set_visible(True)
            self._update_screen()
            self.clock.tick(60)

    def _fire_bullet(self):
        """创建一颗子弹,并将其加入编组bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            # noinspection PyTypeChecker
            self.bullets.add(new_bullet)

    def _check_keydown_events(self, event):
        """相应按下键盘事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # 按下Q键结束游戏
                sys.exit()
            else:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                if event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                if event.key == pygame.K_SPACE:
                    self._fire_bullet()

    def _check_keyup_events(self, event):
        """相应释放键盘事件"""
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = False

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            self._check_keydown_events(event)
            self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """在玩家单击Play时,开始新游戏"""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.game_active:
            # 重置游戏的速度设置
            self.settings.initialize_dynamic_settings()
            # 重置游戏的统计信息
            self.states.reset_stats()
            self.sb.prep_score()
            self.sb.check_high_score()
            self.sb.prep_ships()
            self.game_active = True
            # 清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()
            # 创建一个新的外星舰队，并将飞船放在屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.bg_color)  # 设置屏幕的颜色
        self.ship.blitme()  # 重新绘制飞船
        self.aliens.draw(self.screen)
        # 显示得分
        self.sb.show_score()
        # 如果游戏处于非活动状态，就绘制Play按钮
        if not self.game_active:
            self.play_button.draw_button()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()  # 重新绘制子弹

        pygame.display.flip()

    def _update_bullets(self):
        """更新子弹的位置并删除已消失的子弹"""
        # 更新每个子弹的位置
        self.bullets.update()
        # 删除已经消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人的碰撞"""
        # 检查是否有子弹击中了外星飞船
        # 如果是，就删除相应的子弹和外星飞船
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.states.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()
        if not self.aliens:
            # 提高等级
            self.states.level += 1
            self.sb.prep_level()
            # 删除现有的子弹并制造一个新的外星舰队
            self.settings.increase_speed()
            self.bullets.empty()
            self._create_fleet()

    def _create_fleet(self):
        """创建一个外星舰队"""
        # 创建一个外星飞船，再不断添加，直到没有空间添加外星飞船为止
        # 外星人的间距为外星人的宽度和外星飞船的高度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x = alien_width + 2 * alien_width
        current_y = alien_height
        while current_y < (self.settings.screen_height - 4 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._creat_alien(current_x, current_y)
                current_x += 2 * alien_width
            #  添加一行外星飞船后重置x的值并递增y值
            current_x = alien_width + 2 * alien_width
            current_y += 2 * alien_height

    def _creat_alien(self, x_position, y_position):
        """创建一个外星飞船并将其放在当前行中"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = new_alien.x
        new_alien.rect.y = y_position
        # noinspection PyTypeChecker
        self.aliens.add(new_alien)

    # noinspection PyTypeChecker
    def _update_aliens(self):
        """更新外星飞船舰队的位置"""
        self._check_fleet_edges()
        self.aliens.update()
        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查是否有外星人到达了屏幕的下边缘
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """在有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整个外星舰队向下移动，并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """响应飞船和外星飞船的碰撞"""
        print("您的飞船被撞击！")
        if self.states.ships_left > 0:
            # 将剩余的飞船数量减一
            self.states.ships_left -= 1
            self.sb.prep_ships()
            # 清空外星飞船列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()
            # 创建一个新的外星舰队，并将飞船放在屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()
            # 暂停
            sleep(0.5)
        else:
            self.game_active = False

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕的下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # 像飞船被撞到一样进行处理
                self._ship_hit()
                break


if __name__ == '__main__':
    """创建实例并运行游戏"""
    ai = AlienInvasion()
    ai.run_game()
