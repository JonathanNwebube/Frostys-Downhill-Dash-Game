import pygame
import os
import time
import random
from random import randrange
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTHBG, HEIGHTBG = 1280, 720
WIN = pygame.display.set_mode((WIDTHBG, HEIGHTBG))
pygame.display.set_caption("Frosty's Downhill Dash")

FONT_MAIN = pygame.font.Font(os.path.join('assets', 'fonts', 'PressStart2P.ttf'), 32)
FONT_SMALL = pygame.font.Font(os.path.join('assets', 'fonts', 'PressStart2P.ttf'), 20)


WHITE =(255,255,255)
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('assets','images', 'SnowyBG.jpg')),(WIDTHBG, HEIGHTBG))
LOADINGSCREEN = pygame.transform.scale(pygame.image.load(os.path.join('assets','images', 'TwoSnowmen.jpg')),(WIDTHBG, HEIGHTBG))
FPS = 60

CARROT = pygame.transform.scale(pygame.image.load(os.path.join('assets','images','Carrot.png')),(50,50))
RAINDROP = pygame.transform.scale(pygame.image.load(os.path.join('assets','images', 'raindrop.png')),(50,50))
BALL = pygame.transform.scale(pygame.image.load(os.path.join('assets','images', 'Sball.png')),(64,64))
FIREBALL = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('assets','images', 'Fireball.png')),(50,50)), 180)


Carrot_collect = pygame.mixer.Sound(os.path.join('assets','sounds','PowerUpOhYeah.mp3'))
object_hit = pygame.mixer.Sound(os.path.join('assets','sounds','UGH.mp3'))
pygame.mixer.music.load(os.path.join('assets','sounds','Dream.mp3'))
pygame.mixer.music.play(-1)

SURFING_IMG = pygame.image.load(os.path.join('assets','images', 'Surfing22.png'))
SURFING_LEFT = pygame.transform.scale(SURFING_IMG,(160, 160))
SURFING_RIGHT = pygame.transform.flip(SURFING_LEFT, True, False)
STANDING_IMG = pygame.image.load(os.path.join('assets','images', 'Standing.png'))
STANDING = pygame.transform.scale(STANDING_IMG,(160,160))



class player:
    def __init__(self, x, y, WIDTH, HEIGHT, health=100):
        self.x = x
        self.y = y
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.VEL = 7
        self.left = False
        self.right = False
        self.health = health
        self.max_health = health
        self.snowman_img = STANDING
        self.mask = pygame.mask.from_surface(self.snowman_img)
        

    def draw(self,WIN):
        if self.left:
            WIN.blit(SURFING_LEFT,(self.x,self.y))
        elif self.right:
            WIN.blit(SURFING_RIGHT,(self.x,self.y))
        else:
            WIN.blit(STANDING, (self.x ,self.y))
        self.healthbar(WIN)

    def healthbar(self, WIN):
        pygame.draw.rect(WIN, (255,0,0), (self.x, self.y + self.snowman_img.get_height() + 10, self.snowman_img.get_width(), 10))
        pygame.draw.rect(WIN, (0,128,0), (self.x, self.y + self.snowman_img.get_height() + 10, self.snowman_img.get_width() * (self.health/self.max_health), 10))

    

class OBJECTS:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.object_img = None

    def draw(self, WIN):
        WIN.blit(self.object_img, (self.x, self.y))

    def collision(self, obj):
        return collide(self, obj)
    
    def get_width(self):
        return self.object_img.get_width()

    def get_height(self):
        return self.object_img.get_height()
       

class FallingObject(OBJECTS):
    POSSIBLE_OBJECT = {
                "POraindrop": (RAINDROP),
                "POfireball": (FIREBALL)
                }

    def __init__(self, x, y, choice):
        super().__init__(x,y)
        self.object_img = self.POSSIBLE_OBJECT[choice]
        self.mask = pygame.mask.from_surface(self.object_img)
    
    def move(self, vel):
        self.y += vel

class Snowball(OBJECTS):
    def __init__(self, x, y, ball):
        super().__init__(x, y)
        self.object_img = BALL
        self.mask = pygame.mask.from_surface(self.object_img)

    def move(self, vel):
        self.y += vel

class Carrots(OBJECTS):
    def __init__(self, x, y, carrot):
        super().__init__(x, y)
        self.object_img = CARROT
        self.mask = pygame.mask.from_surface(self.object_img)
    
    def move(self, vel):
        self.y += vel


    
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def pause_menu():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Resume
                    paused = False

        pause_text = FONT_MAIN.render("PAUSED", True, (255, 255, 255))
        resume_text = FONT_SMALL.render("Press P to Resume", True, (200, 200, 200))

        WIN.blit(pause_text, (WIDTHBG/2 - pause_text.get_width()/2, HEIGHTBG/2 - 100))
        WIN.blit(resume_text, (WIDTHBG/2 - resume_text.get_width()/2, HEIGHTBG/2))

        pygame.display.update()

def game_over_screen(score):
    click = False
    while True:
        WIN.blit(BACKGROUND, (0,0))

        # Dark overlay
        overlay = pygame.Surface((WIDTHBG, HEIGHTBG))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        WIN.blit(overlay, (0, 0))

        # Title + Score
        title_text = FONT_MAIN.render("GAME OVER", True, (255, 80, 80))
        score_text = FONT_SMALL.render(f"Final Score: {score}", True, (255, 255, 255))

        WIN.blit(title_text, (WIDTHBG//2 - title_text.get_width()//2, 180))
        WIN.blit(score_text, (WIDTHBG//2 - score_text.get_width()//2, 250))

        # Buttons
        mx, my = pygame.mouse.get_pos()

        button_play = pygame.Rect(WIDTHBG//2 - 260, 360, 240, 80)
        button_quit = pygame.Rect(WIDTHBG//2 + 20, 360, 240, 80)


        # Play button hover
        if button_play.collidepoint((mx, my)):
            pygame.draw.rect(WIN, (0, 255, 255), button_play)  # Neon Cyan hover
        else:
            pygame.draw.rect(WIN, (0, 200, 200), button_play)  # Default

        # Quit button hover
        if button_quit.collidepoint((mx, my)):
            pygame.draw.rect(WIN, (0, 255, 255), button_quit)
        else:
            pygame.draw.rect(WIN, (0, 200, 200), button_quit)

        pygame.draw.rect(WIN, (0,150,150), button_play, 5)  # border
        pygame.draw.rect(WIN, (0,150,150), button_quit, 5)

        play_text = FONT_SMALL.render("PLAY AGAIN", True, (0, 0, 0))
        quit_text = FONT_SMALL.render("QUIT", True, (0, 0, 0))
        WIN.blit(play_text, (button_play.x + 20, button_play.y + 25))
        WIN.blit(quit_text, (button_quit.x + 80, button_quit.y + 25))


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.collidepoint((mx, my)):
                    return  # Restart game
                if button_quit.collidepoint((mx, my)):
                    pygame.quit()
                    quit()
                    
def SBGmain():
    clock = pygame.time.Clock()  
    run = True
    snowman = player(600, 450, 160, 160)
    point_font = FONT_SMALL
    lost_font = FONT_MAIN
    score_font = FONT_MAIN
    score = 0
    level = 0
    objects = [] 
    wave_length = 5
    object_vel = 3
    balls = []
    constant = 2
    carrots = []

    def draw_window_FrostysDownhillDash(level):
        WIN.blit(BACKGROUND,(0,0))
        points_label = point_font.render(f'Score: {score}', 1, (0,0,0))
        WIN.blit(points_label, (10,10))

        level_label = point_font.render(f'Wave: {level}', 1, (0,0,0))
        WIN.blit(level_label, (WIDTHBG - level_label.get_width() - 20, 10))  # Top-right corner

        
        for object in objects:
            object.draw(WIN)

        for ball in balls:
            ball.draw(WIN)
        
        for carrot in carrots:
            carrot.draw(WIN)

        snowman.draw(WIN)
        

        pygame.display.update()

    while run:
        clock.tick(FPS)
        draw_window_FrostysDownhillDash(level)

        if snowman.health <=0:
            pygame.mixer.music.stop()
            game_over_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'game_over.wav'))
            game_over_sound.play()

            # Slow-motion effect
            for _ in range(20):
                pygame.time.delay(50)

            game_over_screen(score)
            return  # restart completely

        if len(objects) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                object = FallingObject(randrange(50, WIDTHBG-100), randrange(-1500, -100), random.choice(["POraindrop","POfireball"]))
                objects.append(object)

        if len(balls) == 0:
            for i in range(constant):
                ball = Snowball(randrange(50, WIDTHBG-100), randrange(-1500, -100), BALL)
                balls.append(ball)

        if len(carrots) == 0:
            for i in range(constant):
                carrot = Carrots(randrange(50, WIDTHBG-100), randrange(-1500, -100), CARROT)
                carrots.append(carrot)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pause_menu()
        

        keys_pressed = pygame.key.get_pressed()


        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            if snowman.x > 0:
                snowman.x -= snowman.VEL
            snowman.left = True
            snowman.right = False

        elif keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            if snowman.x < WIDTHBG - snowman.WIDTH:
                snowman.x += snowman.VEL
            snowman.right = True
            snowman.left = False

        else:
            snowman.left = False
            snowman.right = False
 

        for object in objects[:]:
            object.move(object_vel)
            if object.y + object.get_height() > HEIGHTBG:
                objects.remove(object)
            

            if collide(object, snowman):
                object_hit.play()
                snowman.health -=10
                objects.remove(object)

        
        for ball in balls[:]:
            ball.move(object_vel)
            if ball.y + ball.get_height() > HEIGHTBG:
                balls.remove(ball)

            if collide(ball, snowman) and snowman.health < 100:
                snowman.health +=10
                balls.remove(ball)
            
        for carrot in carrots[:]:
            carrot.move(object_vel)
            if carrot.y + carrot.get_height() > HEIGHTBG:
                carrots.remove(carrot)
            

            if collide(carrot, snowman):
                Carrot_collect.play()
                score +=1
                carrots.remove(carrot)

            

def main_menu():
    while True:
        WIN.blit(LOADINGSCREEN, (0,0))
        title = FONT_MAIN.render("Frosty's Downhill Dash", True, (255,255,255))
        start_text = FONT_SMALL.render("Click to Start", True, (200,200,200))
        WIN.blit(title, (WIDTHBG//2 - title.get_width()//2, 200))
        WIN.blit(start_text, (WIDTHBG//2 - start_text.get_width()//2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                SBGmain()

main_menu()