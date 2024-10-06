import pygame
from player import Player
from enemy import Enemy
from camera import *

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 432
canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Forest Walking Sim")

run = True

cat = Player()
camera = Camera(cat)
follow = Follow(camera, cat)
border = Border(camera, cat)
auto = Auto(camera, cat)
camera.setmethod(border)

ground_image = pygame.image.load(".\\image\\ground.png").convert_alpha()
attack = pygame.image.load(".\\image\\attack_animation.png").convert_alpha()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

bg_images = []
for i in range(1, 6):
    bg_image = pygame.image.load(f".\\image\\plx-{i}.png").convert_alpha()
    bg_images.append(bg_image)

bg_width = bg_images[0].get_width()

def draw_bg():
    for x in range(5):
        speed = 1
        for i in bg_images:
            screen.blit(i, ((x * bg_width) - camera.offset.x * speed, 0))
            speed += 0.2

def draw_ground():
    for x in range(15):
        screen.blit(ground_image, ((x * ground_width) - camera.offset.x * 2, SCREEN_HEIGHT - ground_height))


class Projectile:
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

def redrawGameWindow():
    cat.update()
    camera.scroll()
    screen.fill((0, 0, 0))
    canvas.fill((0, 0, 0, 0))
    screen.blit(canvas, (0, 0))
    draw_bg()
    draw_ground()
    
    font = pygame.font.SysFont('comicsans', 30, True)
    text = font.render('Score: ' + str(cat.score), 1, (255,255,255))
    screen.blit(text, (350, 10))
    
    screen.blit(cat.current_image, (cat.rect.x - camera.offset.x, cat.rect.y - camera.offset.y))
    
    goblin.respawn()
    if goblin.visible:
        goblin.draw(screen)
        
    for bullet in bullets:
        bullet.draw(screen)
    
    pygame.display.update()
    
shootLoop = 0
bullets = []
goblin = Enemy(100, 325, 64, 64, 450)

while run:
    clock.tick(FPS)
    
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
        
    if goblin.visible:
        player_rect = pygame.Rect(cat.hitbox)
        goblin_rect = pygame.Rect(goblin.hitbox)
        
        if player_rect.colliderect(goblin_rect) and cat.invincibility_frames <= 0:
            cat.hit()
            cat.invincibility_frames = 60
    
    if cat.invincibility_frames > 0:
        cat.invincibility_frames -= 1
    
    for bullet in bullets:
        if goblin.visible:
            if (bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and 
                bullet.y + bullet.radius > goblin.hitbox[1]):
                if (bullet.x + bullet.radius > goblin.hitbox[0] and 
                    bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]):
                    goblin.hit()
                    cat.score += 1
                    bullets.pop(bullets.index(bullet))
                    
        if bullet.x < SCREEN_WIDTH and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                cat.LEFT_KEY, cat.FACING_LEFT = True, True
            elif event.key == pygame.K_RIGHT:
                cat.RIGHT_KEY, cat.FACING_LEFT = True, False
            elif event.key == pygame.K_SPACE and shootLoop == 0:
                cat.ATTACK_KEY = True
                facing = -1 if cat.FACING_LEFT else 1
                if len(bullets) < 5:
                    bullets.append(
                        Projectile(
                            round(cat.x + cat.width //4), 
                            round(cat.y + cat.height//4), 
                            6, (0,0,0), facing
                        )
                    )
                shootLoop = 1
            elif event.key == pygame.K_UP and not cat.isJump:
                cat.isJump = True
            elif event.key == pygame.K_1:
                camera.setmethod(follow)
            elif event.key == pygame.K_2:
                camera.setmethod(auto)
            elif event.key == pygame.K_3:
                camera.setmethod(border)
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                cat.LEFT_KEY = False
            elif event.key == pygame.K_RIGHT:
                cat.RIGHT_KEY = False
    
    redrawGameWindow()
    pygame.display.update()
pygame.quit()