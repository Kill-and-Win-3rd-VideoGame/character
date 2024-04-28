import pygame
import random
import math

class GameObject:
    def __init__(self, imgUrl, size, x, y, speed):
        self.imgUrl = imgUrl
        self.size = size
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = random.choice(["up", "down", "left", "right"])
        self.health = 100

    def draw(self, screen):
        img = pygame.image.load(self.imgUrl)
        screen.blit(img, (self.x, self.y))

    def move(self):
        if self.direction == "up":
            self.y -= 0.5
        elif self.direction == "down":
            self.y += 0.5
        elif self.direction == "left":
            self.x -= 0.5
        elif self.direction == "right":
            self.x += 0.5

        if random.random() < 0.001:
            self.direction = random.choice(["up", "down", "left", "right"])

        if self.x < 0:
            self.x = 0
        elif self.x > 800:
            self.x = 800
        if self.y < 0:
            self.y = 0
        elif self.y > 400:
            self.y = 400

    def hit(self, other):
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        if distance <= self.size / 2 + other.size / 2:
            return True
        return False

    def distance_to(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class Sword(GameObject):
    def __init__(self, imgUrl, size, x, y, speed):
        super().__init__(imgUrl, size, x, y, speed)

    def draw(self, screen):
        super().draw(screen)


class Player(GameObject):
    def __init__(self, imgUrl, size, x, y, speed):
        super().__init__(imgUrl, size, x, y, speed)
        self.sword_length = 50
        self.sword_angle = 0
        self.sword_offset = 30  # Offset from the player's position
        self.sword = Sword("sword.png", 20, self.x + self.sword_offset, self.y + self.sword_offset, 0)  # Example parameters, adjust as needed

    def handle_input(self, keys):
        if keys[pygame.K_UP]:
            self.y -= 0.5
        elif keys[pygame.K_DOWN]:
            self.y += 0.5
        elif keys[pygame.K_LEFT]:
            self.x -= 0.5
        elif keys[pygame.K_RIGHT]:
            self.x += 0.5

        if keys[pygame.K_SPACE]:
            self.attack()

    def attack(self):
        # Logic for attacking with the sword
        pass

    def draw(self, screen):
        super().draw(screen)
        self.draw_sword(screen)

    def draw_sword(self, screen):
        # Calculate sword tip position
        sword_tip_x = self.x+30 + self.sword_offset + self.sword_length * math.cos(math.radians(self.sword_angle))
        sword_tip_y = self.y +50+ self.sword_offset + self.sword_length * math.sin(math.radians(self.sword_angle))

        # Update sword position
        self.sword.x = sword_tip_x
        self.sword.y = sword_tip_y

        # Draw sword
        self.sword.draw(screen)


class YellowObject(GameObject):
    def __init__(self, imgUrl, size, x, y, speed):
        super().__init__(imgUrl, size, x, y, speed)
        self.enemy_sword_length = 30  # Increase the length to make it bigger
        self.enemy_sword_angle = 0
        self.enemy_sword_offset =-70  # Adjust the offset to move it more to the left side of the enemy
        self.enemy_sword_imgUrl = "enemySword.png"  # Path to the enemy sword image
        self.enemy_sword = Sword(self.enemy_sword_imgUrl, 20, self.x + self.enemy_sword_offset, self.y + 280, 0)  # Example parameters, adjust as needed

    def sense_and_move(self, player):
        if player.x < self.x:
            self.direction = "left"
        elif player.x > self.x:
            self.direction = "right"
        if player.y < self.y:
            self.direction = "up"
        elif player.y > self.y:
            self.direction = "down"

    def draw(self, screen):
        super().draw(screen)
        self.draw_enemy_sword(screen)  # Make sure to call draw_enemy_sword after drawing the YellowObject

    def draw_enemy_sword(self, screen):
        # Calculate sword tip position
        enemy_sword_tip_x = self.x + self.enemy_sword_offset + self.enemy_sword_length * math.cos(math.radians(self.enemy_sword_angle))
        enemy_sword_tip_y = self.y + 180 + self.enemy_sword_offset + self.enemy_sword_length * math.sin(math.radians(self.enemy_sword_angle))

        # Update sword position
        self.enemy_sword.x = enemy_sword_tip_x
        self.enemy_sword.y = enemy_sword_tip_y

        # Draw sword
        self.enemy_sword.draw(screen)



