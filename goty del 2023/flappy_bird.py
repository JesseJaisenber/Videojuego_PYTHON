import pygame, sys, time, random
import pygame.mixer
from pygame.locals import *

pygame.init()
width = 500
height = 700
play_surface = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flapi berd")
background_image = pygame.image.load("back.png").convert()
bird_image = pygame.image.load("bird.png").convert_alpha()
top_pipe = pygame.image.load("pipe_top.png").convert_alpha()
bot_pipe = pygame.image.load("pipe_bot.png").convert_alpha()
fps = pygame.time.Clock()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Define font
font = pygame.font.SysFont(None, 48)

class Button:
    def __init__(self, x, y, width, height, color, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = font

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

def show_menu():
    # Carga la imagen de fondo
    background_image = pygame.image.load('huevada.png')

    # Define el botón de "Jugar"
    play_button = Button(width/2-75, height/2, 150, 50, BLUE, "Jugar", font)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if play_button.rect.collidepoint(event.pos):
                    return

        # Dibuja la imagen de fondo y el botón de jugar
        play_surface.blit(background_image, (0, 0))
        play_button.draw(play_surface)



        pygame.display.update()
def choose_bird():
    bird_images = ["bird.png", "bird2.png", "bird3.png", "bird4.png"]  # lista de imágenes del pájaro
    current_bird = 0  # índice de la imagen actual del pájaro

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Si se presiona Enter, iniciar el juego
                    return bird_images[current_bird]
                elif event.key == pygame.K_RIGHT:  # Si se presiona la flecha derecha, cambiar a la siguiente imagen
                    current_bird = (current_bird + 1) % len(bird_images)
                elif event.key == pygame.K_LEFT:  # Si se presiona la flecha izquierda, cambiar a la imagen anterior
                    current_bird = (current_bird - 1) % len(bird_images)

        play_surface.blit(background_image, [0, 0])

        # Dibujar las imágenes de los pájaros y una flecha indicando la imagen actual
        font = pygame.font.Font(None, 36)
        bird_text = font.render("Selecciona un pájaro", True, (255, 255, 255))
        bird_rect = bird_text.get_rect()
        bird_rect.centerx = width / 2
        bird_rect.centery = height / 2 - 100
        play_surface.blit(bird_text, bird_rect)

        bird_image = pygame.image.load(bird_images[current_bird]).convert_alpha()
        play_surface.blit(bird_image, (int(width / 2 - bird_image.get_width() / 2), int(height / 2 - bird_image.get_height() / 2)))

        arrow_left = font.render("<", True, (255, 255, 255))
        arrow_right = font.render(">", True, (255, 255, 255))
        arrow_left_rect = arrow_left.get_rect()
        arrow_right_rect = arrow_right.get_rect()
        arrow_left_rect.centery = height / 2
        arrow_right_rect.centery = height / 2
        arrow_left_rect.right = width / 2 - 10
        arrow_right_rect.left = width / 2 + 10
        play_surface.blit(arrow_left, arrow_left_rect)
        play_surface.blit(arrow_right, arrow_right_rect)

        pygame.display.flip()
        fps.tick(25)
    
#top pipe
def pipe_random_height():
    pipe_h = [random.randint(200,(height/2)-20), random.randint((height/2)+20, height-200)]
    return pipe_h

def main():
    show_menu()
    choose_bird()

    # Carga la música de fondo
    pygame.mixer.music.load("musicazelda.mp3")
    
    # Inicia la reproducción de la música en bucle
    pygame.mixer.music.play(-1)
    bird_image_file = choose_bird()
    bird_image = pygame.image.load(bird_image_file).convert_alpha()
    score = 0
    player_pos = [100, 350]
    gravity = 1
    speed = 0
    jump = -30

    #pipe
    pipe_pos = 700
    pipe_width = 50
    pipe_height = pipe_random_height()

    # Game Over flag
    game_over = False

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if game_over:
                            game_over = False
                            score = 0
                            player_pos = [100, 350]
                            pipe_pos = 700
                            pipe_height = pipe_random_height()
                            speed = 0
                        else:
                            speed += jump

        #Down Force
        speed += gravity
        speed *= 0.95
        player_pos[1] += speed

        #pipe
        if pipe_pos >= -20:
            pipe_pos -= 10
        else:
            pipe_pos = 700
            pipe_height = pipe_random_height()
            score += 1

        #Surface
        play_surface.blit(background_image, [0, 0])

        #drawpipe
        play_surface.blit(top_pipe, (pipe_pos, -pipe_height[0]))
        play_surface.blit(bot_pipe, (pipe_pos, pipe_height[1]))

        #player
        play_surface.blit(bird_image, (int(player_pos[0]), int(player_pos[1])))

        #Collision
        if player_pos[1] <= (-pipe_height[0]+500) or player_pos[1] >= pipe_height[1]:
            if player_pos[0] in list(range(pipe_pos, pipe_pos+pipe_width)):
                game_over = True

        #Borders
        if player_pos[1] >= height:
            player_pos[1] = height
            speed = 0
        elif player_pos[1] <= 0:
            player_pos[1] = 0
            speed = 0

        # Draw the score and game over message
        font = pygame.font.Font(None, 22)
        score_text = font.render("Puntaje: " + str(score), True, (255, 255, 255))
        play_surface.blit(score_text, (10, 10))
        if game_over:
            game_over_text = font.render("Papi ha perdido, Presione Espacio para volver a jugar xd", True, (255, 0, 0))
            play_surface.blit(game_over_text, (50, height/2))

        pygame.display.flip()
        fps.tick(25)


main()
pygame.quit()