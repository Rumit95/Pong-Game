import pygame
import pymunk
import random

pygame.init()

display = pygame.display.set_mode((1000,600))
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 144

left = 25
right = 975
top = 35
bottom = 565
middlex = 500
middley = 300
dummy = True

def print_text(text, x, y=5, alpha=255, size = 45, font=None):
    font = pygame.font.SysFont(None, size, False, False)
    text = font.render(text, True, (255,255,255))
    text.set_alpha(alpha)
    display.blit(text, (x, y))

class Ball():
    def __init__(self):
        self.body = pymunk.Body()
        self.reset(0,0,0)
        self.body.velocity = (400, -300)
        self.shape = pymunk.Circle(self.body, 10)
        self.shape.density = 1
        self.shape.elasticity = 1
        space.add(self.body,self.shape)
        self.shape.collision_type = 1

    def draw(self):
        x, y = self.body.position
        pygame.draw.circle(display, (255,255,255), (int(x), int(y)), 10)

    def reset(self, space=0, arbiter=0, data=0):
        self.body.position = middlex,middley
        self.body.velocity = (-400*random.choice([-1,1]), -300*random.choice([-1,1])) #diff
        return False
    
    def standarize_velocity(self, space=0, arbiter=0, data=0):
        self.body.velocity = self.body.velocity*(750/self.body.velocity.length)
    

class Wall():
    def __init__(self, p1, p2, collision_number=None):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, 8)
        self.shape.elasticity = 1
        space.add(self.body, self.shape) 
        if collision_number:
            self.shape.collision_type = collision_number

    def draw(self):
        pygame.draw.line(display, (255,255,255), self.shape.a, self.shape.b, 8)


class Player():
    def __init__(self, x):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = (x, middley)
        self.shape = pymunk.Segment(self.body, (0,-50), (0,50), 10) #diff
        self.shape.elasticity = 1
        space.add(self.body, self.shape)
        self.shape.collision_type = 100
        self.score = 0 

    def draw(self):
        p1 = self.body.local_to_world(self.shape.a)
        p2 = self.body.local_to_world(self.shape.b)
        pygame.draw.line(display, (255,255,255), p1, p2, 12)

    def on_edge(self):
        p1_y = self.body.local_to_world(self.shape.a)[1]
        p2_y = self.body.local_to_world(self.shape.b)[1]

        if p1_y < top:
            self.body.position = (self.body.position[0], top + 50)
        if p2_y > bottom:
            self.body.position = (self.body.position[0], bottom - 50)

    def move(self, up=True):
        self.body.velocity = (0, -800) if up  else (0, 800)

    def stop(self):
        self.body.velocity = (0,0)


def game():
    ball = Ball()
    wall_left = Wall((left,top),(left,bottom), 102)
    wall_right = Wall((right,top),(right,bottom), 101)
    wall_top = Wall((left,top),(right,top))
    wall_bottom = Wall((left,bottom),(right,bottom))
    player1 = Player(left+15)
    player2 = Player(right-15)

    scored_p1 = space.add_collision_handler(1,101)
    scored_p2 = space.add_collision_handler(1,102)


    def player1_scored(space, arbiter, data):
        player1.score += 1
        if player1.score >= 10:
            player1.score = 0
            player2.score = 0
            show_winner_screen("Player 1 Wins!")
        ball.reset()
        return False
    
    scored_p1.begin = player1_scored

    def player2_scored(space, arbiter, data):
        player2.score += 1
        if player2.score >= 10:
            player1.score = 0
            player2.score = 0
            show_winner_screen("Player 2 Wins!")
        ball.reset()
        return False
    
    scored_p2.begin = player2_scored

    contact_with_player = space.add_collision_handler(1, 100)
    contact_with_player.post_solve = ball.standarize_velocity


    def show_winner_screen(winner_text):
        waiting_for_enter = True
        while waiting_for_enter:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    global dummy
                    dummy = False
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting_for_enter = False

            display.fill((0, 0, 0))
            print_text(winner_text, middlex - 230, middley - 150, size=100)
            print_text("Press Enter to Restart", middlex - 250, middley - 20, size=75, alpha=50)
            pygame.display.update()


    waiting_for_enter = True
    while waiting_for_enter:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting_for_enter = False

        display.fill((0,0,0))
        print_text("P'o'NG", middlex-100, middley-150, size=100)
        print_text("Press Enter to Start", middlex-230, middley-20, size=75, alpha=50)
        # print_text("Press Enter to Restart", middlex - 250, middley - 0, size=75, alpha=50)
        # print_text("Player 2 Wins!", middlex - 230, middley - 150, size=100)
        pygame.display.update()

    
    while True:
        if dummy:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                player1.move(True)
            elif keys[pygame.K_s]:
                player1.move(False)
            else:
                player1.stop()

            if keys[pygame.K_UP]:
                player2.move(True)
            elif keys[pygame.K_DOWN]:
                player2.move(False)
            else:
                player2.stop()

            player1.on_edge()
            player2.on_edge()
                
            display.fill((0,0,0))
            ball.draw()
            wall_left.draw()
            wall_right.draw()
            wall_top.draw()
            wall_bottom.draw()
            player1.draw()
            player2.draw()
            pygame.draw.line(display, (255,255,255), (middlex,top), (middlex,bottom), 4)
            print_text(f"{player1.score}", left+400)
            print_text("-", left+470)
            print_text(f"{player2.score}", right-400)

            pygame.display.update()
            clock.tick(FPS)
            space.step(1/FPS)

        else:
            pygame.quit()

game()
pygame.quit()