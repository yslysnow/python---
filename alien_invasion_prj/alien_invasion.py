"""
游戏外星人入侵中，玩家控制一艘最初出现在屏幕底部中央的武装飞船。
使用方向键左右移动飞船，使用空格键射击，
游戏开始，一支外星人舰队出现在天空，像屏幕下方移动。
玩家将当前外星人消灭干净后将出现一个新的外星舰队，移动速度更快。
只要有外星人撞击飞船或者到达屏幕下边缘，玩家损失一艘飞船。
损失三艘飞船后，游戏结束。
"""

import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (0,0),pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #游戏活动标志
        self.game_active = False

        #创建play按钮
        self.play_button = Button(self,"Play")


    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)


    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _check_play_button(self,mouse_pos):
        """响应按钮"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            #重置统计信息
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True

            #清空外星人和子弹列表
            self.bullets.empty()
            self.aliens.empty()

            #创建新飞船和舰队
            self._create_fleet()
            self.ship.center_ship()

            #隐藏光标
            pygame.mouse.set_visible(False)



    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _fire_bullet(self):
        """创建一颗子弹并将其加入编组bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """更新子弹位置并删除已消失的子弹"""
        self.bullets.update()

        #删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        # 检查是否有子弹击中了外星人，若是，则删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_highest_score()

        if not self.aliens:
            # 删除现有的子弹并创建一个新舰队
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #提高等级
            self.stats.level += 1
            self.sb.prep_level()


    def _update_aliens(self):
        """检测是否有外星人在屏幕边缘并更新外星舰队中所有外星人位置"""
        self._check_fleet_edges()
        self.aliens.update()

        #检测外星人和飞船之间碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

        #检查是否有外星人到达下边缘
        self._check_aliens_bottom()

    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        if self.stats.ships_left > 0:
           # 将ships_left减1并更新剩余飞船图像
           self.stats.ships_left -= 1
           self.sb.prep_ships()

           # 清空外星人列表和子弹列表
           self.bullets.empty()
           self.aliens.empty()

           # 创建一个新的外星舰队，并将飞船放在屏幕底部中央
           self._create_fleet()
           self.ship.center_ship()

           # 暂停
           sleep(0.5)
        else:
           self.game_active = False
           pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #x像飞船被撞到一样处理
                self._ship_hit()
                break


    def _create_fleet(self):
        """创建一个外星人舰队"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        #外星人间距为外星人宽度和高度
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 13 * alien_height):
            while current_x < (self.settings.screen_width-3 * alien_width):
                self._create_alien(current_x,current_y)
                current_x += 3 * alien_width

            #添加一行外星人后，重置x并递增y
            current_x = alien_width
            current_y += 2 * alien_height

        #为避免飞船计数遮挡外星人，舰队整体向下调整一定距离
        for alien in self.aliens.sprites():
            alien.rect.y += alien_height + 10


    def _create_alien(self,x_position,y_position):
        """创建一个外星人并将其加入舰队"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


    def _check_fleet_edges(self):
        """在外星人到达边缘时采取相应措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """将外星舰队整体向下移动，并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_screen(self):
        """更新屏幕图像并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        #显示得分
        self.sb.show_score()

        #非活动状态绘制play按钮
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()

