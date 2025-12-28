# Import
import sys

import pygame
import SceneManager
from Button import ButtonImg

def Menu():
    # Initialize
    pygame.init()
    pygame.event.clear()

    # Create Window/Display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Squid Game")

    # Initialize Clock for FPS
    fps = 30
    clock = pygame.time.Clock()

    # Images
    imgBackground = pygame.image.load("Resources/Project - SquidGame/MainMenuBackground.png").convert()

    # Buttons
    buttonGreenLight = ButtonImg((160, 290), "Resources/Project - SquidGame/Buttons/1.png",
                        pathSoundClick="Resources/Sounds/click.mp3",
                        pathSoundHover="Resources/Sounds/hover.mp3")
    buttonCookieCutter = ButtonImg((160, 410), "Resources/Project - SquidGame/Buttons/2.png",
                        pathSoundClick="Resources/Sounds/click.mp3",
                        pathSoundHover="Resources/Sounds/hover.mp3")
    buttonQuit = ButtonImg((160, 530), "Resources/Project - SquidGame/Buttons/3.png",
                        pathSoundClick="Resources/Sounds/click.mp3",
                        pathSoundHover="Resources/Sounds/hover.mp3")


    # Main loop
    start = True
    while start:
        # Get Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    SceneManager.OpenScene("Game")

        # Apply Logic

        # Draw Background/Buttons
        window.blit(imgBackground, (0, 0))
        buttonGreenLight.draw(window)
        buttonCookieCutter.draw(window)
        buttonQuit.draw(window)

        if buttonGreenLight.state == "clicked":
            SceneManager.OpenScene("GameGreenLight")
        if buttonCookieCutter.state == "clicked":
            SceneManager.OpenScene("GameCookieCutter")
        if buttonQuit.state == "clicked":
            pygame.quit()
            sys.exit()

        # Update Display
        pygame.display.update()
        # Set FPS
        clock.tick(fps)


if __name__ == "__main__":
    Menu()
