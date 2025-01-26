import sys
import time
import random

class Game:
    def __init__(self):
        self.alien = Actor('alien_right', midbottom=(400, 600))  # karakteri oluştur
        self.alien_left = "alien_left"
        self.alien_right = "alien_right"
        self.WIDTH = 800
        self.HEIGHT = 600

        self.enemy_starting_position = [0, 800]

        self.is_sound_active = True
        self.is_in_menu = True

        self.contiunebutton = Rect((300, 100), (200, 75))
        self.soundbutton = Rect((300, 300), (200, 75))
        self.exitbutton = Rect((300, 500), (200, 75))

        self.is_directed_to_right = True  # eğer karakter sağ tarafa dönükse laser karakterden çıkıp sağ tarafa doğru gidecek
        self.lasers = []  # her bir laseri buraya ekleyeceğim sonra iterate yapacağım
        self.last_laser_time = 0
        self.laser_cooldown = 1

        self.enemy_1 = []
        self.enemy_2 = []

        self.counter = 0

    def draw(self):
        if self.is_in_menu:
            screen.blit("background", (0, 0))
            screen.draw.filled_rect(self.contiunebutton, "#1E90FF")
            screen.draw.text(
                "Continue",
                center=self.contiunebutton.center,
                fontsize=30,
                color="white",
                shadow=(1, 1),
            )

            screen.draw.filled_rect(self.soundbutton, "#1E90FF")
            screen.draw.text(
                f"Sound:{str(self.is_sound_active)}",
                center=self.soundbutton.center,
                fontsize=30,
                color="white",
                shadow=(1, 1),
            )

            screen.draw.filled_rect(self.exitbutton, "#1E90FF")
            screen.draw.text(
                "Exit",
                center=self.exitbutton.center,
                fontsize=30,
                color="white",
                shadow=(1, 1),
            )
        else:
            screen.clear()
            screen.blit("game", (0, 0))
            self.alien.draw()

            for laser in self.lasers:
                laser[0].draw()
            for enemy in self.enemy_1:
                enemy[0].draw()

    def update(self):
        if self.is_in_menu:
            return  # menüdeyken oyunun güncellenmesini durdur

        if keyboard.left:
            self.alien.image = self.alien_left
            self.alien.x -= 3
            self.is_directed_to_right = False
        elif keyboard.right:
            self.alien.image = self.alien_right
            self.alien.x += 3
            self.is_directed_to_right = True

        for laser in self.lasers[:]:
            for enemy in self.enemy_1[:]:
                if laser[1]:
                    laser[0].x += 5
                else:
                    laser[0].x -= 5

                if laser[0].colliderect(enemy[0]):  # lazer düşmana çarptı
                    sounds.explosion.play()
                    self.enemy_1.remove(enemy)
                    self.lasers.remove(laser)
                    self.counter += 1
                    break

        for enemy in self.enemy_1[:]:
            if enemy[1] == 0:
                enemy[0].x += 1
            elif enemy[1] == 800:
                enemy[0].x -= 1

            if enemy[0].colliderect(self.alien):  # düşman oyuncuya çarptı
                self.is_in_menu = True
                self.counter = 0
                sounds.fail.play()
                return

        if self.counter == 10:
            self.is_in_menu = True
            sounds.win.play()

        self.lasers = [laser for laser in self.lasers if 0 < laser[0].x < self.WIDTH]
        self.enemy_1 = [enemy for enemy in self.enemy_1 if 0 < enemy[0].x < self.WIDTH]

    def fire_laser(self):
        
        current_time = time.time()
        if current_time - self.last_laser_time >= self.laser_cooldown:
            if self.is_directed_to_right:
                laser = Actor("laserimage", (self.alien.x + 20, self.alien.y))
                self.lasers.append((laser, self.is_directed_to_right))
                sounds.fire.play()

            else:
                laser = Actor("laserimage", (self.alien.x - 20, self.alien.y))
                self.lasers.append((laser, self.is_directed_to_right))
                sounds.fire.play()
            self.last_laser_time = current_time

    def on_mouse_down(self, pos):
        if self.is_in_menu and self.contiunebutton.collidepoint(pos):
            self.is_in_menu = False  # oyunu burdan başlatacağım
            self.enemy_1.clear()  # düşmanları temizle
            self.lasers.clear()  # lazerleri temizle
            self.create_enemy()
        elif self.is_in_menu and self.soundbutton.colliderect(pos):
            if self.is_sound_active:
                self.is_sound_active = False
                sounds.mainsound.stop()
            else:
                self.is_sound_active = True
                sounds.mainsound.play()
        elif self.is_in_menu and self.exitbutton.collidepoint(pos):
            sys.exit()

    def create_enemy(self):
        which_side = random.sample(self.enemy_starting_position, 1)
        if which_side[0] == 0:
            enemy = Actor("enemyleft", midbottom=(0, 600))
            self.enemy_1.append((enemy, 0))
        if which_side[0] == 800:
            enemy = Actor("enemyright", midbottom=(800, 600))
            self.enemy_1.append((enemy, 800))
        clock.schedule(self.create_enemy, 2.0)

    def on_music_end(self):
        sounds.mainsound.play()

    def on_key_down(self, key):
        if key == keys.ESCAPE:
            self.is_in_menu = True
        if key == keys.SPACE:
            self.fire_laser()
            

game = Game()
sounds.mainsound.play()  # default olarak şarkı çalsın
game.create_enemy()

def draw():
    game.draw()

def update():
    game.update()

def on_mouse_down(pos):
    game.on_mouse_down(pos)

def on_key_down(key):
    game.on_key_down(key)

def on_music_end():
    game.on_music_end()
