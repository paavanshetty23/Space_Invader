

# Space Invader Game

Welcome to **Space Invader**, a classic arcade-style shooting game built using Python's `pygame` library. This game challenges you to defend your spaceship from waves of enemy ships while dodging their attacks. It's a fun way to dive into game development using Python!

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Code Overview](#code-overview)
  - [Laser Class](#laser-class)
  - [Ship Class](#ship-class)
  - [Player Class](#player-class)
  - [Enemy Class](#enemy-class)
  - [Main Game Loop](#main-game-loop)
  - [Main Menu](#main-menu)
- [Acknowledgments](#acknowledgments)

## Introduction

**Space Invader** is a simple 2D shooting game where the player controls a spaceship and must eliminate incoming enemy ships. The player can move the spaceship left, right, up, and down, and can shoot lasers to destroy enemies. The game progresses in levels, with each level increasing the difficulty by introducing more enemies.

## Features

- Multiple levels with increasing difficulty.
- Smooth player and enemy movements.
- Health and lives tracking for the player.
- Cooldown system to prevent constant shooting.
- Animated lasers and ships.
- Collision detection between lasers and ships.

## Installation

To run this game on your local machine, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/paavanshetty23/Space_Invader.git
cd Space_Invader
```

### 2. Install Required Packages

Ensure you have Python installed (version 3.6 or later is recommended). Install the `pygame` library using pip:

```bash
pip install pygame
```

### 3. Run the Game

You can start the game by running the following command:

```bash
python space_invader.py
```

## How to Play

- Use the **A** key to move left.
- Use the **D** key to move right.
- Use the **W** key to move up.
- Use the **S** key to move down.
- Press **SPACE** to shoot lasers.
- Destroy all enemy ships to advance to the next level.
- Avoid getting hit by enemy lasers or colliding with enemy ships.

## Code Overview

Here's a breakdown of the main classes and functions in the game:

### Laser Class

The `Laser` class handles the creation and movement of laser projectiles fired by both the player and enemies.

```python
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
```

### Ship Class

The `Ship` class is the base class for both the player's ship and enemy ships. It handles movement, shooting, and managing health.

```python
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
```

### Player Class

The `Player` class is derived from the `Ship` class and represents the player's spaceship. It includes additional functionality like the health bar display.

```python
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
        pygame.draw.rect(win, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width()*(self.health/self.max_health), 10) )                
```

### Enemy Class

The `Enemy` class, also derived from `Ship`, manages the behavior of enemy ships, including their movement and shooting.

```python
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
```

### Main Game Loop

The `main()` function contains the primary game loop, handling events, player input, and updating the game state.

```python
def main():
    # Initial setup and variables
    # Game loop with events handling, player input, and updating game state
```

### Main Menu

The `main_menu()` function displays the start screen and waits for the player to press the SPACE key to begin the game.

```python
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

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()

    pygame.quit()
```

## Acknowledgments

- The game concept is inspired by classic arcade games like Space Invaders.
- Graphics and sounds used in the game are credited to their respective creators.

---

This README template should provide a good starting point for documenting your Space Invader game. You can further customize it based on your project's specifics and any additional features you might add in the future!
## Installation

Install my-project with npm

```bash
  npm install my-project
  cd my-project
```
    