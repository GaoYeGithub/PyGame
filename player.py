import pygame
from spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT, self.ATTACK_KEY = False, False, False, False
        self.load_frames()
        self.rect = self.idle_frames_left[0].get_rect()
        self.invincibility_frames = 0

        self.ground_y = 432 - 70
        self.rect.midbottom = (570, self.ground_y)

        self.current_frame = 0
        self.last_updated = 0
        self.velocity = 0
        self.state = 'idle'
        self.current_image = self.idle_frames_left[0]

        self.left_border, self.right_border = 0, 5000

        self.box = pygame.Rect(self.rect.x, self.rect.y, self.rect.w * 2, self.rect.h)
        self.box.center = self.rect.center
        self.passed = False
        self.x = self.rect.x
        self.y = self.rect.y
        self.width = self.rect.width
        self.height = self.rect.height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.score = 0
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, display):
        display.blit(self.current_image, self.rect)

    def update(self):
        self.velocity = 0
        keys = pygame.key.get_pressed()
        
        if self.LEFT_KEY and self.x > self.vel:
            self.velocity = -self.vel
            self.FACING_LEFT = True
        elif self.RIGHT_KEY and self.x < 800 - self.width - self.vel:
            self.velocity = self.vel
            self.FACING_LEFT = False
            
        self.x += self.velocity
        self.rect.x = self.x
        
        if self.isJump:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= (self.jumpCount ** 2) * 0.5 * neg
                self.rect.y = self.y
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 10
        if self.invincibility_frames > 0:
            if self.invincibility_frames % 10 < 5:
                self.current_image.set_alpha(128)
            else:
                self.current_image.set_alpha(255)
        else:
            self.current_image.set_alpha(255)
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.set_state()
        self.animate()

    def set_state(self):
        if self.state != 'attacking':
            self.state = 'idle'
            if self.velocity > 0:
                self.state = 'moving right'
            elif self.velocity < 0:
                self.state = 'moving left'

    def animate(self):
        now = pygame.time.get_ticks()
        if self.state == 'attacking':
            if now - self.last_updated > 100:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.attack_frames)

                if self.FACING_LEFT:
                    self.current_image = pygame.transform.flip(self.attack_frames[self.current_frame], True, False)
                else:
                    self.current_image = self.attack_frames[self.current_frame]

                if self.current_frame == len(self.attack_frames) - 1:
                    self.ATTACK_KEY = False
                    self.state = 'idle'
                    self.current_frame = 0

        elif self.state == 'idle':
            if now - self.last_updated > 200:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames_left)
                if self.FACING_LEFT:
                    self.current_image = self.idle_frames_left[self.current_frame]
                elif not self.FACING_LEFT:
                    self.current_image = self.idle_frames_right[self.current_frame]
        else:
            if now - self.last_updated > 100:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_left)
                if self.state == 'moving left':
                    self.current_image = self.walking_frames_left[self.current_frame]
                elif self.state == 'moving right':
                    self.current_image = self.walking_frames_right[self.current_frame]

    def hit(self):
        if self.invincibility_frames <= 0:
            self.isJump = False
            self.jumpCount = 10
            self.x = 100
            self.y = self.ground_y
            self.rect.x = self.x
            self.rect.y = self.y
            self.current_frame = 0
            self.score -= 5
            self.invincibility_frames = 60

    def load_frames(self):
        my_spritesheet = Spritesheet('poppy_sheet.png')
        
        self.idle_frames_left = [my_spritesheet.parse_sprite("poppy_idle1.png"),
                                my_spritesheet.parse_sprite("poppy_idle2.png")]
        
        self.walking_frames_left = [my_spritesheet.parse_sprite(f"poppywalk{i}.png") for i in range(1, 9)]
        
        self.idle_frames_right = [pygame.transform.flip(frame, True, False) for frame in self.idle_frames_left]
        self.walking_frames_right = [pygame.transform.flip(frame, True, False) for frame in self.walking_frames_left]
        
        attack_sheet = pygame.image.load(".\\image\\attack_animation.png").convert_alpha()
        
        frame_width = attack_sheet.get_width() // 4
        frame_height = attack_sheet.get_height()
        self.attack_frames = []
        
        for i in range(4):
            frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frame = attack_sheet.subsurface(frame_rect)
            self.attack_frames.append(frame)