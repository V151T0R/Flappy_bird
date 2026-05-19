import pygame
from pygame.locals import *
import random

# Initialize Pygame
pygame.init()

# Set up the window
width, height = 900, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird in Space -- Capsotne project - [ROLL:1931026] -  [Course:Software Development] ")
clock = pygame.time.Clock()
font=pygame.font.Font('freesansbold.ttf',20)

# colors class
class colors:
    black=(0,0,0)
    white=(255,255,255)
    gray=(128,128,128)
    brown=(255,212,0)
    fire=(255,137,0)
    red=(255,0,0)
    pink=(255,192,203)

#color as an object 
color=colors
#----------------- -------------------------------------------------varriable library-------------------------------------------------------------------------------------

# bird properties
bird_radius = 30
bird_x = 225
bird_y = height // 2
bird_velocity = 2

#scores 
score=0
high_score=0

# Gravity
gravity = 0.7
game_over=False

# obstacle
obstacles_x = [400, 700, 1000, 1300, 1600] #obstacle position in x direction
obstacles_y = []                           #obstacle position in Y direction 
generate_obstacles_places = True
obstacle_speed=1

#stars
stars=[]



#------------------------------------------------------------User Defined Functions--------------------------------------------------------------------------------------


def draw_bird(bird_x, bird_y):
    """
    Draw the bird on the display.

    Parameters:
    - bird_x (int): The x-coordinate of the bird.
    - bird_y (int): The y-coordinate of the bird.

    Returns:
    - bird (Rect): The rectangle representing the bird on the display.
    """
    global bird_velocity

    # Bird components
    jetpack = pygame.draw.rect(screen, color.brown, [bird_x, bird_y + 20, 28, 18], 15, 12)
    mouth = pygame.draw.circle(screen, color.pink, [bird_x + 25, bird_y + 15], 12)
    bird = pygame.draw.rect(screen, color.red, [bird_x, bird_y, 30, 30], 0, 12)
    eye = pygame.draw.circle(screen, color.black, [bird_x + 20, bird_y + 12], 5)
    ear = pygame.draw.circle(screen, color.red, [bird_x, bird_y], 5)

    # Jetpack effect
    if bird_velocity < 0:
        flame1 = pygame.draw.rect(screen, color.brown, [bird_x, bird_y + 30, 10, 15], 5)
        flame2 = pygame.draw.rect(screen, color.brown, [bird_x + 15, bird_y + 30, 10, 15], 5)

    return bird


def draw_obstacles(x_pos, y_pos):
    """
    Draw the obstacles on the display.

    Parameters:
    - x_pos(list): The x-coordinates of the obstacles.
    - y_pos (list): The y-coordinates of the obstacles.

    Returns:
    None
    """
    for i in range(len(x_pos)):
        y_cord = y_pos[i]
        top_rect = pygame.draw.rect(screen, color.gray, [x_pos[i], 0, 30, y_cord])
        top_rect_cap = pygame.draw.rect(screen, color.gray, [x_pos[i] - 3, y_cord - 20, 36, 20], 0, 5)
        bottom_rect = pygame.draw.rect(screen, color.gray, [x_pos[i], y_cord + 200, 30, height - y_cord + 70])
        bottom_rect_cap = pygame.draw.rect(screen, color.gray, [x_pos[i] - 3, y_cord + 200, 36, 20], 0, 5)


def check_collision(bird_x, bird_y, bird_radius, obstacle_x, obstacle_y, obstacle_width, obstacle_height):
    """
    Check if there is a collision between the bird and an obstacle.

    Parameters:
    - bird_x (int): The x-coordinate of the bird.
    - bird_y (int): The y-coordinate of the bird.
    - bird_radius (int): The radius of the bird.
    - obstacle_x (int): The x-coordinate of the obstacle.
    - obstacle_y (int): The y-coordinate of the obstacle.
    - obstacle_width (int): The width of the obstacle.
    - obstacle_height (int): The height of the obstacle.

    Returns:
    - collision (bool): True if there is a collision, False otherwise.
    """
    bird_rect = pygame.Rect(bird_x, bird_y, bird_radius, bird_radius)
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
    collision = bird_rect.colliderect(obstacle_rect)
    return collision


def draw_star():
    """
    Draw stars on the display and update their positions.

    Parameters:
    None

    Returns:
    - stars (list): The list of stars with updated positions.
    """
    global total
    for i in range(total - 1):
        pygame.draw.rect(screen, color.white, [stars[i][0], stars[i][1], 3, 3], 0, 2)
        stars[i][0] -=2#stars velocity 10 pixel per frame

        if stars[i][0] < -3:
            stars[i][0] = width + 3
            stars[i][1] = random.randint(0, height)

    return stars



    



# Game loop
running = True
while running:
    
    screen.fill(color.black)                         # Clear the screen
    
    if generate_obstacles_places:              #generate obstacle-y position randomly 
        for i in range(len(obstacles_x)):
            obstacles_y.append(random.randint(0, 300))
        total=100
        for i in range(total):                  #generate stars_x and stars_y position randomly
            stars_x=random.randint(0,width)
            stars_y=random.randint(0,height)
            stars.append([stars_x,stars_y])
        generate_places = False



    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE and not game_over:
                bird_velocity = -8  # Jump up
                
#-------------------------------when game_over=True it start the game again----------------------------                 
                
            if event.key == K_SPACE and game_over: 
                    score=0
                    bird_x = 225
                    bird_y = height // 2
                    obstacles_x = [400, 700, 1000, 1300, 1600] 
                    obstacles_y = []
                    generate_places=True
                    if generate_obstacles_places:
                     for i in range(len(obstacles_x)):
                       obstacles_y.append(random.randint(0, 300))
                       generate_places = False
                    game_over=False
                    bird_velocity = 2
                    obstacle_speed=1
 #-----------------------------------------------------------------------------------------------------              




    # Update bird position
    bird_y += bird_velocity
    bird_velocity += gravity

    # creating boundary so that the bird can't go down from the screen
    if bird_y >= height:
        bird_y = height - 30

    #draw the stars
    draw_star()
    
    # Draw the bird
    bird=draw_bird(bird_x, bird_y)
   
    # Draw the obstacles
    obstacles=draw_obstacles(obstacles_x, obstacles_y)
    
    



#**(adding obstacles continously and randomly)
    for i in range (len(obstacles_x)):
        if not game_over:
            obstacles_x[i]-=obstacle_speed  #obstacles moving speed is 1 pixel per frame
            if obstacles_x[i]<-30:
                obstacles_x.remove(obstacles_x[i])
                obstacles_y.remove(obstacles_y[i])
                obstacles_x.append(random.randint(obstacles_x[-1]+280,obstacles_x[-1]+320))
                obstacles_y.append(random.randint(0, 300))
                score+=1
        

 
    # Check collision
    for i in range(len(obstacles_x)):
        if check_collision(bird_x, bird_y, bird_radius, obstacles_x[i], 0, 30, obstacles_y[i]) or  check_collision(bird_x, bird_y, bird_radius, obstacles_x[i], obstacles_y[i] + 200, 30, height - obstacles_y[i] + 70):
            game_over = True
               
    
     #display game over   
    if game_over:
        game_over_text=font.render('NICE TRY!! Better luck next time :( ',True,color.red)
        screen.blit(game_over_text,(225,225))
        restart_text=font.render('Restart [space bar]',True,color.red)
        screen.blit(restart_text,(300,270))
    
    if score>high_score:
        high_score=score  
    
    #Display score     
    score_text=font.render('score:'+str(score),True,color.white)
    screen.blit(score_text,(10,450))
    
    #Display High score 
    high_score_text=font.render('High score:'+str(high_score),True,color.white)
    screen.blit(high_score_text,(10,470))
    
    
  
   
    pygame.display.flip()    # Update the display
    clock.tick(60  )           # Limit frame rate to 60 FPS
    



# Quit the game
pygame.quit()
