# Import
import pygame
import SceneManager
from B_Basics.CustomClasses.Button import ButtonImg


def Menu():
    """Main Menu with fullscreen support"""

    # Initialize
    pygame.init()
    pygame.event.clear()

    # Get fullscreen resolution
    screen_info = pygame.display.Info()
    width, height = screen_info.current_w, screen_info.current_h

    # Create Fullscreen Window
    window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    pygame.display.set_caption("Squid Game")

    # Initialize Clock for FPS
    fps = 30
    clock = pygame.time.Clock()

    # Images
    imgBackground = pygame.image.load("../../Resources/Project - SquidGame/MainMenuBackground.png").convert()
    imgBackground = pygame.transform.scale(imgBackground, (width, height))

    # Button positions (centered and scaled for fullscreen)
    button_x = width // 2 - 150
    button_y_start = height // 2 - 200

    # Buttons
    buttonGreenLight = ButtonImg((button_x, button_y_start),
                                       "../../Resources/Project - SquidGame/Buttons/1.png",
                                       scale=0.8,
                                       pathSoundClick="../../Resources/Sounds/click.mp3",
                                       pathSoundHover="../../Resources/Sounds/hover.mp3")


    buttonCookieCutter = ButtonImg((button_x, button_y_start + 120),
                                   "../../Resources/Project - SquidGame/Buttons/2.png",
                                   scale=0.8,
                                   pathSoundClick="../../Resources/Sounds/click.mp3",
                                   pathSoundHover="../../Resources/Sounds/hover.mp3")

    buttonQuit = ButtonImg((button_x, button_y_start + 240),
                           "../../Resources/Project - SquidGame/Buttons/3.png",
                           scale=0.8,
                           pathSoundClick="../../Resources/Sounds/click.mp3",
                           pathSoundHover="../../Resources/Sounds/hover.mp3")

    # Font for labels
    font_large = pygame.font.Font(None, 60)
    font_small = pygame.font.Font(None, 40)

    # Main loop
    start = True
    while start:
        # Get Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start = False
                    pygame.quit()

        # Draw Background
        window.blit(imgBackground, (0, 0))

        # Draw title with enhanced styling
        title_text = font_large.render("SQUID GAME", True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(width // 2, 100))

        # Add shadow effect
        shadow_text = font_large.render("SQUID GAME", True, (0, 0, 0))
        window.blit(shadow_text, (title_rect.x + 3, title_rect.y + 3))
        window.blit(title_text, title_rect)

        # Draw Buttons and Labels

        buttonGreenLight.draw(window)
        # label2 = font_small.render("Green Light 2P", True, (255, 255, 255))
        # window.blit(label2, (button_x + 50, button_y_start - 60))

        buttonCookieCutter.draw(window)
        # label3 = font_small.render("Cookie Cutter", True, (255, 255, 255))
        # window.blit(label3, (button_x + 50, button_y_start + 60))

        buttonQuit.draw(window)
        # label4 = font_small.render("Quit Game", True, (255, 255, 255))
        # window.blit(label4, (button_x + 80, button_y_start + 180))

        # Handle button clicks
        if buttonGreenLight.state == "clicked":
            SceneManager.OpenScene("GameGreenLightMode")

        if buttonCookieCutter.state == "clicked":
            SceneManager.OpenScene("GameCookieCutter")

        if buttonQuit.state == "clicked":
            pygame.quit()
            start = False

        # Update Display
        pygame.display.update()
        # Set FPS
        clock.tick(fps)


if __name__ == "__main__":
    Menu()