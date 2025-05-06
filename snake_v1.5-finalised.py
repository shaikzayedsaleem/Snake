'''Coding ka Rule No. 1: If it runs, don't touch it hehe'''

import pygame                                               #imports Pygame module (for functions that need... -_-)
import time                                                 #imports time module   (for functions that need time)
import random                                               #imports random module (for functions that need randomisation)
import os                                                   #imports os module     (for functions that interact with operating system )
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()                                               #initializing Pygame module

white = (255, 255, 255)                                     #definition of variables (tuples) that hold numbers
black = (0, 0, 0)                                           #because we need to have rgb color code for various purposes
game_over_color = (252, 64, 64)
sapphire_blue = (41, 128, 185)                              #deeper sapphire blue for better contrast

dis_width = 1024                                            #display window width
dis_height = 680                                            #display window height

dis = pygame.display.set_mode((dis_width, dis_height))      #display window setup
pygame.display.set_caption('Snake Game by Sapphire')        #display window caption

# Load background images using resource_path
background = pygame.image.load(resource_path(os.path.join("Snake Development","Snake_v1.5-finalised","Snake_v1.5","Snake_v1.5","snake_v1.5","snake", "assets", "images", "background of pure sand.png")))
background = pygame.transform.scale(background, (dis_width, dis_height))
background_game_over = pygame.image.load(resource_path(os.path.join("Snake Development","Snake_v1.5-finalised","Snake_v1.5","Snake_v1.5","snake_v1.5","snake", "assets", "images", "desert floor blurred.png")))
background_game_over = pygame.transform.scale(background_game_over, (dis_width, dis_height))

snake_block = 20                                            #snake head size

'''Asset config done by Roushna'''
food_image = pygame.image.load(resource_path(os.path.join("Snake Development","Snake_v1.5-finalised","Snake_v1.5","Snake_v1.5","snake_v1.5","snake", "assets", "images", "food.png")))
food_size = snake_block * 4                                 # Increase the food size to twice the snake block size
food_image = pygame.transform.scale(food_image, (food_size/2, food_size/2))

snake_head_image = pygame.image.load(resource_path(os.path.join("Snake Development","Snake_v1.5-finalised","Snake_v1.5","Snake_v1.5","snake_v1.5","snake", "assets", "images", "desert_krait_head.png")))
snake_head_image = pygame.transform.scale(snake_head_image, (snake_block, snake_block))

# Load and set window icon
logo_image = pygame.image.load(resource_path(os.path.join("Snake Development","Snake_v1.5-finalised","Snake_v1.5","Snake_v1.5","snake_v1.5","snake", "assets", "images", "Sapphire.png")))
window_icon = pygame.transform.scale(logo_image, (64, 64))  # Larger window icon
pygame.display.set_icon(window_icon)

# Load game logo for main menu
game_logo = pygame.image.load(resource_path(os.path.join("Snake Development","Snake_v1.5-finalised","Snake_v1.5","Snake_v1.5","snake_v1.5","snake", "assets", "images", "game_logo.png")))
logo_size = 300                                             # Adjust this value based on your logo size needs
game_logo_display = pygame.transform.scale(game_logo, (logo_size, logo_size))
game_logo_rect = game_logo_display.get_rect()

snake_body_image = pygame.image.load(resource_path(os.path.join("Snake Development","Snake_v1.5-finalised","Snake_v1.5","Snake_v1.5","snake_v1.5","snake", "assets", "images", "desert_krait_body.png")))
snake_body_image = pygame.transform.scale(snake_body_image, (snake_block, snake_block))

snake_tail_image = pygame.image.load(resource_path(os.path.join("Snake Development","Snake_v1.5-finalised","Snake_v1.5","Snake_v1.5","snake_v1.5","snake", "assets", "images", "desert_krait_tail.png")))
snake_tail_image = pygame.transform.scale(snake_tail_image, (snake_block, snake_block))

bgm_path = resource_path(os.path.join("Snake Development","Snake_v1.5-finalised","Snake_v1.5","Snake_v1.5","snake_v1.5","snake", "assets", "music"))
bgm = pygame.mixer.music.load(os.path.join(bgm_path, "Heights at 4.mp3"))

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

clock = pygame.time.Clock()                                 #game clock

# Global variables
snake_speed = 15  # Default speed
min_speed = 5
max_speed = 30

def draw_speed_slider(speed):
    # Draw speed adjustment UI
    slider_width = 200
    slider_height = 20
    slider_x = dis_width / 2 - slider_width / 2
    slider_y = dis_height / 1.17
    
    # Draw slider background
    pygame.draw.rect(dis, black, [slider_x, slider_y, slider_width, slider_height], 2)
    
    # Draw slider position
    pos = ((speed - min_speed) / (max_speed - min_speed)) * slider_width
    pygame.draw.rect(dis, sapphire_blue, [slider_x + pos - 5, slider_y - 5, 10, slider_height + 10])
    
    # Draw speed text
    speed_text = score_font.render(f"Speed: {speed}", True, sapphire_blue)
    dis.blit(speed_text, [slider_x, slider_y - 30])
    
    # Draw min/max labels
    min_text = score_font.render(str(min_speed), True, sapphire_blue)
    max_text = score_font.render(str(max_speed), True, sapphire_blue)
    dis.blit(min_text, [slider_x - 20, slider_y])
    dis.blit(max_text, [slider_x + slider_width + 5, slider_y])
    
    return slider_x, slider_y, slider_width

def our_snake(snake_block, snake_list):
    # for x in snake_list:
    #     pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
    for i, x in enumerate(snake_list):
        if i == 0:
            dis.blit(snake_head_image, (x[0], x[1]))  # Draw the head
        elif i == len(snake_list) - 1:
            dis.blit(snake_tail_image, (x[0], x[1]))  # Draw the tail
        else:
            dis.blit(snake_body_image, (x[0], x[1]))  # Draw the body


def message(msg, color, x_pos=None, y_pos=None):
    # Create outline by rendering black text slightly offset
    outline_color = black
    outline_offset = 2
    
    # Render the outline by placing text at slight offsets
    text_outline = font_style.render(msg, True, outline_color)
    text = font_style.render(msg, True, white)  # Main text in white
    
    if x_pos is None:
        x_pos = dis_width / 4
    if y_pos is None:
        y_pos = dis_height / 2
    
    # Draw the outline
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        dis.blit(text_outline, [x_pos + dx * outline_offset, y_pos + dy * outline_offset])
    
    # Draw the main text
    dis.blit(text, [x_pos, y_pos])

def start_screen():
    intro = True
    global snake_speed
    while intro:
        dis.blit(background, (0, 0))
        
        # Draw game logo at the top center of the screen, (Done by Roushna)
        logo_x = dis_width / 2 - game_logo_rect.width / 2
        logo_y = dis_height / 5 - game_logo_rect.height / 2
        dis.blit(game_logo_display, (logo_x, logo_y))
        
        # Centered text positions with new color, (Done by Roushna)
        center_x = dis_width / 2
        message("Press SPACE to Start", sapphire_blue, center_x - 150, int(dis_height / 2.4))
        message("Arrow keys or WASD to move", sapphire_blue, center_x - 180, dis_height / 2.1)
        message("Press P to Pause", sapphire_blue, center_x - 100, dis_height / 1.87)
        message("Press R to Resume", sapphire_blue, center_x - 100, dis_height / 1.7)
        message("Press M to mute, U to unmute", sapphire_blue, center_x - 180, dis_height / 1.55)
        message("Press Q to Quit", sapphire_blue, center_x - 100, dis_height / 1.44)
        
        # Add clear gap before speed controls, (Done by Roushna)
        message("Speed Controls", sapphire_blue, center_x - 100, dis_height / 1.34)
        slider_x, slider_y, slider_width = draw_speed_slider(snake_speed)
        message("Use LEFT/RIGHT arrows to adjust", sapphire_blue, center_x - 200, dis_height / 1.1)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_LEFT and snake_speed > min_speed:
                    snake_speed -= 1
                elif event.key == pygame.K_RIGHT and snake_speed < max_speed:
                    snake_speed += 1

def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, black)
    dis.blit(value, [0, 0])

#Background music configuration
pygame.mixer.init()
pygame.mixer.music.load(resource_path(os.path.join("Snake Development","Snake_v1.5-finalised","Snake_v1.5","Snake_v1.5","snake_v1.5","snake", "assets", "music", "Heights at 4.mp3")))
pygame.mixer.music.set_volume(0.10)
pygame.mixer.music.play(-1)

def pause_game():
    paused = True
    message("Game Paused", sapphire_blue, dis_width / 2 - 100, dis_height / 2 - 50)
    message("Press R to Resume", sapphire_blue, dis_width / 2 - 120, dis_height / 2)
    pygame.display.update()
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    paused = False

def game_loop():
    game_over = False
    game_close = False
    score = 0
    global snake_speed

    x1 = round(random.randint(0, dis_width - snake_block) / 30.0) * 30.0
    y1 = round(random.randint(0, dis_height - snake_block) / 30.0) * 30.0

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - food_size) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - food_size) / 10.0) * 10.0

    while not game_over:
        while game_close == True:
            dis.blit(background_game_over, (0,0))
            message("Game Over!", game_over_color, dis_width/2 - 100, dis_height/2 - 50)
            message(f"Final Score: {score}", white, dis_width/2 - 100, dis_height/2)
            message("Q-Menu   R-Restart", white, dis_width/2 - 150, dis_height/2 + 50)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False  # Exit game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:     # Q for menu
                        return True  # Return to menu
                    if event.key == pygame.K_r:     # R for restart
                        return game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Exit game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Q during gameplay also returns to menu
                    return True
                if event.key in [pygame.K_LEFT, pygame.K_a] and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key in [pygame.K_RIGHT, pygame.K_d] and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key in [pygame.K_UP, pygame.K_w] and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key in [pygame.K_DOWN, pygame.K_s] and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:
                    pause_game()
                elif event.key == pygame.K_m:
                    pygame.mixer.music.pause()
                elif event.key == pygame.K_u:
                    pygame.mixer.music.unpause()

        if x1 >= dis_width-1 or x1 < 0 or y1 >= dis_height-1 or y1 < 0:     #if snake head touches either boundaries, game closes
            game_close = True
        x1 += x1_change     
        y1 += y1_change
        dis.blit(background, (0, 0))    # Draw Background
        dis.blit(food_image, (foodx, foody))          # Display food image
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:     #if snake bites itself, game lost
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(score)  # Display score
        
        # Display current speed
        speed_text = score_font.render(f"Speed: {snake_speed}", True, black)
        dis.blit(speed_text, [dis_width - 150, 10])  # Top-right corner

        pygame.display.update()

        # Check if the snake's head collides with the food
        if x1 >= foodx and x1 < foodx + food_size and y1 >= foody and y1 < foody + food_size:
            foodx = round(random.randrange(0, dis_width - food_size) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - food_size) / 10.0) * 10.0
            Length_of_snake += 1            #snake's length increment, when upon eating food
            score += 10  # Increment score by 10 points when food is eaten

        clock.tick(snake_speed)  # Use the adjustable snake_speed

    pygame.quit()       #click quit (cross) button to exit window
    sys.exit()

# Main game loop
running = True
while running:
    try:
        start_screen()
        game_loop()
    except SystemExit:
        running = False
    except:
        break

pygame.quit()
sys.exit()