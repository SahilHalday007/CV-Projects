import pygame
import numpy as np
from B_Basics.CustomClasses.Button import ButtonImg
import Scene_manager



def Menu():
    # Initialize
    pygame.init()
    pygame.event.clear()

    # Create Window/Display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Menu")

    # load images
    img_bg = pygame.image.load("../../Resources/Project - Balloon Pop/BackgroundBalloonPop.png").convert()

    # button
    button_start = ButtonImg((465, 420), "../../Resources/Project - Balloon Pop/ButtonStart.png",
                             pathSoundClick='../../Resources/Sounds/click.mp3',
                             pathSoundHover='../../Resources/Sounds/hover.mp3')

    # Initialize Clock for FPS
    fps = 30
    clock = pygame.time.Clock()

    # load background music
    pygame.mixer.pre_init()
    pygame.mixer.music.load("../../Resources/Project - Balloon Pop/BackgroundMusicMenu.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()

    # Main loop
    start = True
    while start:
        # Get Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()

        # Apply Logic
        window.blit(img_bg, (0, 0))
        button_start.draw(window)

        if button_start.state == "clicked":
            pygame.mixer.music.stop()
            Scene_manager.open_scene("Game")


        # Update Display
        pygame.display.update()
        # Set FPS
        clock.tick(fps)

if __name__ == "__main__":
    Menu()