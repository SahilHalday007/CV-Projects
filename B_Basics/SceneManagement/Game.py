# Import
import pygame
import SceneManager

def Game():
    # Initialize
    pygame.init()
    pygame.event.clear()

    # Create Window/Display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("My Awesome Game")

    # Initialize Clock for FPS
    fps = 30
    clock = pygame.time.Clock()

    # Main loop
    start = True
    while start:
        # Get Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    SceneManager.OpenScene("Menu")


        # Apply Logic
        window.fill((255, 255, 255))
        displayText = "Game - press a to go to menu"
        font = pygame.font.Font(None, 50)
        text = font.render(displayText, True, (50, 50, 50))
        window.blit(text, (350, 300))
        # Update Display
        pygame.display.update()
        # Set FPS
        clock.tick(fps)


if __name__ == "__main__":
    Game()
