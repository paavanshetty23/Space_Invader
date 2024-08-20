import pygame
import os
import random 
import time
pygame.font.init()

width, height = 800, 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space_Invader")

red_ship = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
blue_ship = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
green_ship = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
# players
yellow_ship = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

red_laser = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
blue_laser = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
green_laser = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
yellow_laser = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

bg = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (width, height))


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    
    def move(self, vel):
        self.y += vel
    
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)
    
    def collision(self, obj):
        return collide(self, obj)

class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        self.COOLDOWN = 30  # 30 frames cooldown

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
        
    def move_lasers(self, vel, obj):
        self.handle_cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def handle_cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = yellow_ship
        self.laser_img = yellow_laser
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def draw(self,window):
        super().draw(window)
        self.healthbar()

    def healthbar(self):
        pygame.draw.rect(win, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(win, (0,255,0), (self.x, self.y +self.ship_img.get_height() + 10, self.ship_img.get_width()*(self.health/self.max_health), 10) )                

    
    def move_lasers(self, vel, objs):
        self.handle_cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

class Enemy(Ship):
    color_map = {
        "red": (red_ship, red_laser),
        "green": (green_ship, green_laser),
        "blue": (blue_ship, blue_laser)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.color_map[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    fps = 60
    level = 1
    lives = 5
    player_vel = 5
    main_font = pygame.font.SysFont("comicsans", 25)
    lost_font = pygame.font.SysFont("comicsans", 25)
    
    lost = False
    enemies = []
    wave_length = 5
    enemy_vel = 1
    lost_count = 0

    player_ship = Player(300, 630)

    clock = pygame.time.Clock()

    def redraw_window():
        win.blit(bg, (0, 0))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 0, 0))

        win.blit(lives_label, (10, 10))
        win.blit(level_label, (width - level_label.get_width() - 10, 10))
        
        for enemy in enemies:
            enemy.draw(win)

        player_ship.draw(win)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255, 0, 0))
            win.blit(lost_label, (width/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(fps)

        redraw_window()  

        if lives <= 0 or player_ship.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > fps * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy_ship = Enemy(random.randrange(50, width-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy_ship)

        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player_ship.x - player_vel > 0:  # Left
            player_ship.x -= player_vel
        if keys[pygame.K_d] and player_ship.x + player_vel + player_ship.get_width() < width:  # Right
            player_ship.x += player_vel
        if keys[pygame.K_w] and player_ship.y - player_vel > 0:  # Up
            player_ship.y -= player_vel
        if keys[pygame.K_s] and player_ship.y + player_vel + player_ship.get_height()+15< height:  # Down
            player_ship.y += player_vel
        if keys[pygame.K_SPACE]:
            player_ship.shoot()

        for enemy_ship in enemies[:]:
            enemy_ship.move(enemy_vel)
            enemy_ship.move_lasers(4, player_ship)

            if random.randrange(0, 2*60) == 1:
                enemy_ship.shoot()

            if collide(enemy_ship, player_ship):
                player_ship.health -= 10
                enemies.remove(enemy_ship)

            if enemy_ship.y + enemy_ship.get_height() > height:
                lives -= 1
                enemies.remove(enemy_ship)
            
            

        player_ship.move_lasers(-4, enemies)


def main_menu():
    run = True
    title_font = pygame.font.SysFont("comicsans", 60)
    start_font = pygame.font.SysFont("comicsans", 40)

    while run:
        win.blit(bg, (0, 0))
        title_label = title_font.render("...Welcome to Space Invader...", 1, (255, 255, 255))
        win.blit(title_label, (width/2 - title_label.get_width()/2, 300))
        start_label = start_font.render("Press SPACE to start", 1, (255, 255, 255))
        win.blit(start_label, (width/2 - start_label.get_width()/2, 450))

        pygame.display.update()  # Update the screen to show the title and start labels

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()

    pygame.quit()
main_menu()
