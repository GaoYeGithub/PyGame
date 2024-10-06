import pygame

class Enemy:
    def __init__(self, x, y, width, height, end):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True
        self.respawn_timer = 0
        self.respawn_delay = 180
        self.load_frames()
        
    def respawn(self):
        if not self.visible:
            if self.respawn_timer <= 0:
                self.visible = True
                self.health = 10
                self.x = self.start_x
                self.y = self.start_y
                self.walkCount = 0
                self.vel = abs(self.vel)
            else:
                self.respawn_timer -= 1
    
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
            self.respawn_timer = self.respawn_delay

    def load_frames(self):
        self.walkRight = []
        self.walkLeft = []
        for i in range(1, 10):
            img_right = pygame.image.load(f".\\enemies\\R{i}E.png").convert_alpha()
            img_left = pygame.image.load(f".\\enemies\\L{i}E.png").convert_alpha()
            self.walkRight.append(img_right)
            self.walkLeft.append(img_left)
            
    def draw(self, screen):
        if self.visible:
            self.move()
            if self.walkCount + 1 >= 27:
                self.walkCount = 0
                
            if self.vel > 0:
                screen.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                screen.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
                
            pygame.draw.rect(screen, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(screen, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            
    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] - self.vel:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0
                
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False