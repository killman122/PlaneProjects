import random
from random import *
import pygame, sys
import traceback
from pygame.locals import *
import myplane
import enemy
import bullet
import buji
import time
from pygame import *

pygame.init()
pygame.mixer.init()

# pygame.display.update
# 更新软件显示的屏幕部分

# 设置游戏图标
icon = pygame.image.load("image/icon.png")
pygame.display.set_icon(icon)

bg_size = width, height = 480, 768
# 创建目录
screen = pygame.display.set_mode(bg_size)  # 设置显示窗口的模式尺寸

# 创建背景
pygame.display.set_caption("飞机大战")

background = pygame.image.load("image/background.jpg").convert()
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
# 载入音乐
pygame.mixer.music.load("sound/game_music.wav")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound('sound/use_bomb.wav')
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/game_music.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
get_bullet_sound.set_volume(0.2)
# upgrade_sound = pygame.mixer.Sound("sound/")
enem0_fly_sound = pygame.mixer.Sound("sound/enemy0_down.wav")
enem0_fly_sound.set_volume(0.2)
enem1_fly_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enem1_fly_sound.set_volume(0.2)
enem2_fly_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enem2_fly_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound("sound/game_over.wav")
me_down_sound.set_volume(0.2)


def add_small_enemies(group0, group1, num):
    for i in range(num):
        e1 = enemy.smallEnemy(bg_size)
        group0.add(e1)
        group1.add(e1)


def add_mid_enemies(group0, group1, num):
    for i in range(num):
        e2 = enemy.midEnemy(bg_size)
        group0.add(e2)
        group1.add(e2)


def add_big_enemies(group0, group1, num):
    for i in range(num):
        e3 = enemy.bigEnemy(bg_size)
        group0.add(e3)
        group1.add(e3)


def increase_speed(target, inc):
    for each in target:
        each.speed += inc


def main():
    pygame.mixer.music.play(-1)
    # 生成我方飞机
    my = myplane.Myplane(bg_size)  # 实例化对象

    # 生成敌人飞机
    enemys = pygame.sprite.Group()
    # 生成敌方小型飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemys, 15)
    # 生成敌方中型飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemys, 5)
    # 生成敌方大型飞机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemys, 2)
    clock = pygame.time.Clock()
    # 生成敌方大飞机子弹检测
    big_enemies1 = enemy.bigEnemy(bg_size)  # 实例化对象

    # 统计分数
    score = 0
    score_font = pygame.font.Font("font/字魂50号-白鸽天行体.ttf", 36)

    # 设置难度级别
    level = 1

    # 设置道具全屏炸弹
    bomb_image = pygame.image.load("image/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/Marker Felt.ttf", 48)
    bomb_num = 3

    # 每三十秒发放一个补给包
    bullet_buji = buji.bullet_buji(bg_size)
    bomb_buji = buji.bomb_buji(bg_size)
    Time = USEREVENT
    pygame.time.set_timer(Time, 30 * 1000)

    # 二类子弹定时器
    Double_bullet_time = USEREVENT + 1

    # 解除无敌状态计时器
    wudi_time = USEREVENT + 2

    # 生成二类子弹
    bullet2 = []
    bullet2_index = 0
    BUTTET2_NUM = 10  # 当屏幕由四颗子弹组成时效果最佳
    for i in range(BUTTET2_NUM // 2):
        bullet2.append(bullet.bullet2((my.rect.centerx - 33, my.rect.centery)))  # 顶部中央定位子弹的生成位置
        bullet2.append(bullet.bullet2((my.rect.centerx + 30, my.rect.centery)))  # 顶部中央定位子弹的生成位置
    # 是否使用超级子弹
    is_double_bullet = False

    # 生命数量
    life_image = pygame.image.load("image/plane.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    # 生成标志是否暂停游戏
    paused = False
    pause_nor_image = pygame.image.load("image/game_pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("image/game_pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("image/game_resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("image/game_resume_pressed.png").convert_alpha()
    paused_rect = pause_nor_image.get_rect()  # 获取图片的大小
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_image = pause_nor_image
    # 生成一类子弹
    bullet1 = []
    bullet1_index = 0
    BUTTET1_NUM = 6  # 当屏幕由四颗子弹组成时效果最佳
    for i in range(BUTTET1_NUM):
        bullet1.append(bullet.bullet1(my.rect.midtop))  # 顶部中央定位子弹的生成位置

    # 生成敌人一类子弹
    bullet3 = []
    bullet3_index = 0
    BUTTET3_NUM = 6  # 当屏幕由四颗子弹组成时效果最佳
    for i in range(BUTTET3_NUM):
        # bullet3.append(bullet.bullet3((big_enemies1.rect.centerx+33),())  # 顶部中央定位子弹的生成位置
        # bullet3.append(bullet.bullet2((my.rect.centerx - 33, my.rect.centery)))  # 顶部中央定位子弹的生成位置
        bullet3.append(bullet.bullet2((big_enemies1.rect.centerx - 33, big_enemies1.rect.centery)))  # 顶部中央定位子弹的生成位置
        # print(bullet3)

    # 中弹图片索引列表
    fair0_destory_index = 0
    fair1_destory_index = 0
    fair2_destory_index = 0
    my_destory_index = 0
    # bool类型变量用于切换图片
    switch_image = True
    # 用于延迟
    delay = 100
    running = True
    while running:
        for event in pygame.event.get():  # 获取pygame的事件并遍历列表
            if event.type == QUIT:
                # 测试点击关闭按钮的事件print(111)
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(Time, 0)  # 取消自定义事件
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(Time, 30 * 1000)  # 取消自定义事件
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            elif event.type == MOUSEMOTION:  # 当鼠标移动时发出消息
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemys:
                            if each.rect.bottom > 0:
                                each.life = False
            elif event.type == Time:
                supply_sound.play()
                if choice([True, False]):
                    bomb_buji.reset()
                else:
                    bullet_buji.reset()

            elif event.type == Double_bullet_time:
                is_double_bullet = False
                pygame.time.set_timer(Double_bullet_time, 0)  # 关闭定时器

            elif event.type == wudi_time:
                my.wudi = False
                pygame.time.set_timer(wudi_time, 0)
            # elif event.type ==KEYDOWN:
            #     if event.key == K_w or event.key == K_UP:
            #         my.moveUp()
            #     if event.key == K_a or event.key == K_LEFT:
            #         my.moveLeft()
            #     if event.key == K_s or event.key == K_DOWN:
            #         my.moveDown()
            #     if event.key == K_d or event.key == K_RIGHT:
            #         my.moveRight()
        # 根据用户得分增加难度
        if level == 1 and score > 5000:
            level = 2
            # 增加三架小型敌机,2架中型敌机,一架大型敌机
            add_small_enemies(small_enemies, enemys, 3)
            add_mid_enemies(mid_enemies, enemys, 2)
            add_big_enemies(big_enemies, enemys, 1)
            # 提升小型敌机的速度
            increase_speed(small_enemies, 1)
        if level == 2 and score > 3000:
            level = 3
            # 增加5架小型敌机,2架中型敌机,1架大型敌机
            add_small_enemies(small_enemies, enemys, 2)
            add_mid_enemies(mid_enemies, enemys, 2)
            add_big_enemies(big_enemies, enemys, 1)
            # 提升小型敌机的速度
            increase_speed(small_enemies, 1)
            # 提升中型敌机的速度
            increase_speed(mid_enemies, 2)

        # 检测键盘操作
        key_presseds = pygame.key.get_pressed()  # 获取到按下的事件
        if key_presseds[K_w] or key_presseds[K_UP]:
            my.moveUp()
        if key_presseds[K_s] or key_presseds[K_DOWN]:
            my.moveDown()
        if key_presseds[K_a] or key_presseds[K_LEFT]:
            my.moveLeft()
        if key_presseds[K_d] or key_presseds[K_RIGHT]:
            my.moveRight()

        if life_num and not paused:  # 当未暂停并还活着
            # 绘制背景
            screen.blit(background, (0, 0))  # 背景图片坐标位置

            # 绘制子弹
            if not (delay % 10):  # 当每10帧调用一次
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((my.rect.centerx - 33, my.rect.centery))
                    bullets[bullet2_index + 1].reset((my.rect.centerx + 30, my.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BUTTET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(my.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BUTTET1_NUM

            # 检测子弹是否击中
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemys, False, pygame.sprite.collide_mask)
                    if enemy_hit:  # 相当于敌机中蛋
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.hit = True
                                e.energy -= 1
                                if e.energy == 0:
                                    e.life = False
                            else:
                                e.life = False
            # 碰撞检测,检测我方飞机是否被撞
            enemys_down = pygame.sprite.spritecollide(my, enemys, False, pygame.sprite.collide_mask)
            if enemys_down and not my.wudi:
                my.life = False
                for e in enemys_down:
                    e.life = False

            # 绘制我方飞机
            # switch_image = not switch_image
            if my.life:
                # print(my.rect.height)
                if switch_image:
                    screen.blit(my.image1, my.rect)
                else:
                    screen.blit(my.image2, my.rect)
            else:
                # 毁灭
                me_down_sound.play()
                if not (delay % 3):
                    screen.blit(my.destory_images[my_destory_index], my.rect)
                    my_destory_index = (my_destory_index + 1) % 4
                    if my_destory_index == 0:
                        life_num -= 1
                        my.reset()
                        pygame.time.set_timer(wudi_time, 3 * 1000)
                        # print("Game over")
                        # running=False

            # 绘制炸弹数量
            bomb_text = bomb_font.render(("x %d") % bomb_num, True, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))

            # 绘制剩余生命数量
            if life_num:
                for i in range(life_num):  # height指的是屏幕的高度
                    screen.blit(life_image, (width - 10 - (i + 1) * life_rect.width, height - 10 - life_rect.height))

            # 绘制全屏炸弹补给并检测是否获得
            if bomb_buji.active:
                bomb_buji.move()
                screen.blit(bomb_buji.image1, bomb_buji.rect)
                if pygame.sprite.collide_mask(bomb_buji, my):  # 检测我和炸弹是否碰撞吸取到了炸弹
                    get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_buji.active = False

            # 绘制子弹补给并检测是否获得
            if bullet_buji.active:
                bullet_buji.move()
                screen.blit(bullet_buji.image1, bullet_buji.rect)
                if pygame.sprite.collide_mask(bullet_buji, my):  # 检测我和子弹是否碰撞并西区到了子弹
                    get_bullet_sound.play()
                    is_double_bullet = True
                    pygame.time.set_timer(Double_bullet_time, 18 * 1000)
                    # 发射超级子弹
                    bullet_buji.active = False

            # 绘制分数
            score_text = score_font.render("Score:%s" % str(score), True, WHITE)
            screen.blit(score_text, (10, 5))

            # 绘制暂停按钮
            screen.blit(paused_image, paused_rect)

            # 绘制敌人大飞机
            for each in big_enemies:
                if each.life:
                    each.move()
                    if each.hit:
                        screen.blit(each.image3, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, BLACK, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)  # 在图像上方五像素位置处画血槽,血槽宽度为两个像素
                    # 当生命大于20%显示绿色,否则显红色
                    energy_remain = each.energy / enemy.bigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, \
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain, \
                                      each.rect.top - 5), 2)
                    # 即将出现在画面中的音效
                    if each.rect.bottom == -50:
                        enem2_fly_sound.play(-1)  # 设置为-1循环播放音效
                else:
                    # 毁灭
                    if not (delay % 3):
                        if fair2_destory_index == 0:
                            enem0_fly_sound.play()
                        screen.blit(each.destory_images[fair2_destory_index], each.rect)
                        fair2_destory_index = (fair2_destory_index + 1) % 6
                        if fair2_destory_index == 0:
                            enem2_fly_sound.stop()
                            score += 10000
                            each.reset()

            # 绘制敌人中飞机
            for each in mid_enemies:
                if each.life:
                    each.move()
                    if each.hit == True:
                        screen.blit(each.image1, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)
                    # 绘制血槽
                    pygame.draw.line(screen, BLACK, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)  # 在图像上方五像素位置处画血槽,血槽宽度为两个像素
                    # 当生命大于20%显示绿色,否则显红色
                    energy_remain = each.energy / enemy.midEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, \
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain, \
                                      each.rect.top - 5), 2)
                else:
                    # 毁灭
                    if not (delay % 3):
                        if fair1_destory_index == 0:
                            enem0_fly_sound.play()
                        screen.blit(each.destory_images[fair1_destory_index], each.rect)
                        fair1_destory_index = (fair1_destory_index + 1) % 4
                        if fair1_destory_index == 0:
                            score += 5000
                            each.reset()

            # 绘制敌人小型飞机
            for each in small_enemies:
                if each.life:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    # 毁灭
                    if not (delay % 3):
                        if fair0_destory_index == 0:
                            enem1_fly_sound.play()
                        screen.blit(each.destory_images[fair0_destory_index], each.rect)
                        fair0_destory_index = (fair0_destory_index + 1) % 4
                        if fair0_destory_index == 0:
                            score += 1000
                            each.reset()

            # 绘制敌人子弹测试
            if not (delay % 7):  # 当每7帧调用一次
                bullets1 = bullet3
                bullets1[bullet3_index].reset(big_enemies1.rect.midbottom)
                bullets1[bullet3_index].reset(my.rect.midtop)
                bullet3_index = (bullet3_index + 1) % BUTTET3_NUM

            # 检测子弹是否击中
            for a in bullet3:
                if a.active:
                    a.move()
                    screen.blit(a.image, a.rect)
                    # print(a.rect)
                    enemy_hit = pygame.sprite.spritecollide(a, enemys, False, pygame.sprite.collide_mask)
                    if enemy_hit:  # 相当于敌机中蛋
                        a.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.hit = True
                                e.energy -= 1
                                if e.energy == 0:
                                    e.life = False
                            else:
                                e.life = False

        elif life_num == 0:
            print("Game over")

        # 切换图片
        if not (delay % 5):
            switch_image = not switch_image
        delay -= 1
        if not delay:
            delay = 100
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
