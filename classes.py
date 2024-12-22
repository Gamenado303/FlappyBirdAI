import pygame
import random
import c

class Pipe():
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.colour = (50, 205, 50)
        self.scored = 0
    
    def draw_pipe(self):
        top_pipe = pygame.rect.Rect(self.x - c.PIPE_WIDTH/2, -c.NECK_HEIGHT, c.PIPE_WIDTH, self.y)
        top_neck = pygame.rect.Rect(self.x - c.NECK_WIDTH/2, self.y - c.NECK_HEIGHT, c.NECK_WIDTH, c.NECK_HEIGHT)
        btm_pipe = pygame.rect.Rect(self.x - c.PIPE_WIDTH/2, self.y + c.PIPE_GAP + c.NECK_HEIGHT, c.PIPE_WIDTH, c.HEIGHT)
        btm_neck = pygame.rect.Rect(self.x - c.NECK_WIDTH/2, self.y + c.PIPE_GAP, c.NECK_WIDTH, c.NECK_HEIGHT)
        rects = [top_pipe, top_neck, btm_pipe, btm_neck]
        for r in rects:        
            pygame.draw.rect(self.screen, self.colour, r)
            pygame.draw.rect(self.screen, c.BLACK, r, 1)
    
    def move_pipe(self, dt):
        self.x -= 0.2*dt

    def get_rects(self):
        top_pipe = pygame.rect.Rect(self.x - c.PIPE_WIDTH/2, -c.NECK_HEIGHT, c.PIPE_WIDTH, self.y)
        top_neck = pygame.rect.Rect(self.x - c.NECK_WIDTH/2, self.y - c.NECK_HEIGHT, c.NECK_WIDTH, c.NECK_HEIGHT)
        btm_pipe = pygame.rect.Rect(self.x - c.PIPE_WIDTH/2, self.y + c.PIPE_GAP + c.NECK_HEIGHT, c.PIPE_WIDTH, c.HEIGHT)
        btm_neck = pygame.rect.Rect(self.x - c.NECK_WIDTH/2, self.y + c.PIPE_GAP, c.NECK_WIDTH, c.NECK_HEIGHT)
        return [top_pipe, top_neck, btm_pipe, btm_neck]


class Bird():
    def __init__(self, screen):
        self.screen = screen
        self.x = c.START_X
        self.y = c.HEIGHT//2
        self.radius = c.BIRD_RADIUS
        self.speedy = 0
        self.score = 0
        self.alive = 1
    
    def draw_sprite(self):
        if not self.alive: return
        pygame.draw.circle(self.screen, (255,255,0), (self.x, self.y), self.radius)
        pygame.draw.circle(self.screen, c.BLACK, (self.x, self.y), self.radius, width=2)       
        
    def move_sprite(self, dt):
        if not self.alive: return
        self.speedy += 0.04
        self.y += self.speedy*dt
        self.y = min(self.y, c.HEIGHT-self.radius)
        self.y = max(self.y, -self.radius)
        
    def jump(self, dt):
        if not self.alive: return
        self.speedy = -0.04*dt 
    
    def check_collide(self, rects, cur_score):   
        if not self.alive: return     
        flappy_rect = pygame.rect.Rect(0, 0, 1.7*self.radius, 1.9*self.radius)
        flappy_rect.center = (self.x, self.y)
        if pygame.Rect.collidelist(flappy_rect, rects) != -1:
            self.alive = 0
            self.score = cur_score



class Flappy():
    def __init__(self, screen):
        self.screen = screen
        self.pipes = []
        self.birds = []
        self.pipe_total = 6
        self.gap = 400
        self.cur_score = 0
        self.init_game()
        
    def create_pipe(self, x):
        extreme = random.randint(-10,10)
        h = c.HEIGHT - c.PIPE_GAP - c.NECK_HEIGHT
        lower = h//8
        upper = h*7//8
        if extreme >= 3:
            y = random.randint(c.NECK_HEIGHT, lower)
        elif extreme <= -3:
            y = random.randint(upper, h)
        else:
            y = random.randint(lower, upper)

        self.pipes.append(Pipe(self.screen, x, y))
    
    def init_game(self):
        for i in range(self.pipe_total):
            self.create_pipe(c.WIDTH + self.gap*i)
            
    def reset_game(self):
        self.cur_score = 0
        self.birds = []
        self.pipes = []
        for i in range(self.pipe_total):
            self.create_pipe(c.WIDTH + self.gap*i)
            
    def draw_sprites(self):

        f = pygame.font.SysFont('Comic Sans MS', 120)
        text_surface = f.render(str(self.cur_score), False, c.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (c.WIDTH//2,c.HEIGHT//2)
        self.screen.blit(text_surface, text_rect)
        
        for p in self.pipes:
            p.draw_pipe()
        
        for b in self.birds:
            b.draw_sprite()
    
    def move_sprites(self, dt):
        for p in self.pipes:
            p.move_pipe(dt)
        
        for b in self.birds:
            b.move_sprite(dt)
        
        if self.pipes[0].x < -c.NECK_WIDTH:
            self.pipes.pop(0)
        
        if len(self.pipes) < self.pipe_total:
            self.create_pipe(self.pipes[-1].x + self.gap)
            
        if not self.pipes[0].scored and self.pipes[0].x <= c.START_X - c.NECK_WIDTH:
            self.cur_score += 1
            self.pipes[0].scored = 1
        
        # check collisions
        rects = self.get_rects()
        for b in self.birds:
            b.check_collide(rects, self.cur_score)
        
    
    def get_rects(self):
        rects = []
        for p in self.pipes:
            rects += p.get_rects()
        
        return rects
    
