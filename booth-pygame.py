import time

import pygame
from pygame.locals import K_ESCAPE, K_SPACE, QUIT, USEREVENT

COUNTDOWN_DELAY = 4


def timerFunc(countdown, background):
    print("Timer CallBack", time.time())
    print(countdown)
    print("--")

    # Display some text
    font = pygame.font.Font(None, 36)
    text = font.render(str(countdown), 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = background.get_rect().centery
    background.blit(text, textpos)

    if countdown == 0:
        print("SHOOT")


def top_text(background):
    # Display some text
    font = pygame.font.Font(None, 36)
    text = font.render("space to shoot / esc to quit", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(text, textpos)


def main():
    pygame.init()
    countdown = COUNTDOWN_DELAY
    stop_photobooth = False
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption('Photobooth')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((30, 250, 120))
    top_text(background)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    while not stop_photobooth:
        background.fill((30, 250, 120))
        top_text(background)

        for event in pygame.event.get():
            # any other key event input
            if event.type == QUIT:
                stop_photobooth = True
            if event.type == USEREVENT+1:
                if countdown == -1:
                    pygame.time.set_timer(USEREVENT+1, 0)
                    countdown = COUNTDOWN_DELAY
                else:
                    timerFunc(countdown, background) #calling the function wheever we get timer event.
                    countdown -= 1



        # get key current state
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            pygame.time.set_timer(USEREVENT+1, 1000)
        elif keys[K_ESCAPE]:
            print("quit")
            stop_photobooth = True

        screen.blit(background, (0, 0))
        pygame.display.flip()

if __name__ == "__main__":
    main()
