# Import
import pygame
import SceneManager
from B_Basics.CustomClasses.Button import ButtonImg


def Menu():
    # Initialize
    pygame.init()
    pygame.event.clear()

    # Create Window/Display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Fruit Slicer")

    # Initialize Clock for FPS
    fps = 30
    clock = pygame.time.Clock()

    # Images
    imgBackground = pygame.image.load("../../Resources/Project - Fruit Ninja/BackgroundMenu.png").convert()

    # Buttons
    buttonStart = ButtonImg((500, 290), "../../Resources/Project - Fruit Ninja/ButtonStart.png",
                            pathSoundClick="../../Resources/Sounds/click.mp3",
                            pathSoundHover="../../Resources/Sounds/hover.mp3")

    # Main loop
    start = True
    while start:
        # Get Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    SceneManager.OpenScene("Game")

        # Apply Logic

        window.blit(imgBackground, (0, 0))
        buttonStart.draw(window)
        if buttonStart.state == "clicked":
            SceneManager.OpenScene("Game")

        # Update Display
        pygame.display.update()
        # Set FPS
        clock.tick(fps)


if __name__ == "__main__":
    Menu()
