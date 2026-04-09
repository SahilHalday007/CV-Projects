import pygame
import SceneManager
import sys
import cv2
from B_Basics.CustomClasses.Button import ButtonImg


class GameModeSelector:
    def __init__(self):
        self.cap1 = None
        self.cap2 = None
        self.run()

    def FadeOut(self, window, width, height):
        fade = pygame.Surface((width, height))
        fade.fill((0, 0, 0))
        for alpha in range(0, 255, 15):
            fade.set_alpha(alpha)
            window.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(10)

    def run(self):
        pygame.init()
        screen_info = pygame.display.Info()
        width, height = screen_info.current_w, screen_info.current_h
        window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

        # self.cap1 = cv2.VideoCapture(0)  # Primary Camera
        # self.cap2 = cv2.VideoCapture(1)

        fps = 30
        clock = pygame.time.Clock()
        background = pygame.Surface((width, height))
        background.fill((20, 20, 40))

        center_x, center_y = width // 2, height // 2

        button_single = ButtonImg((center_x - 350, center_y - 50),
                                  "../../Resources/Project - SquidGame/Buttons/4.png", scale=0.9)
        button_multi = ButtonImg((center_x + 50, center_y - 50),
                                 "../../Resources/Project - SquidGame/Buttons/5.png", scale=0.9)
        button_back = ButtonImg((center_x - 120, center_y + 200),
                                "../../Resources/Buttons/ButtonBack.png", scale=0.7)

        font_title = pygame.font.Font("../../Resources/Marcellus-Regular.ttf", 100)
        font_desc = pygame.font.Font(None, 40)



        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.FadeOut(window, width, height)
                    SceneManager.OpenScene("Menu")
                    running = False

            window.blit(background, (0, 0))

            # Title
            title = font_title.render("SELECT MODE", True, (255, 0, 0))
            window.blit(title, title.get_rect(center=(center_x, 100)))

            button_single.draw(window)
            button_multi.draw(window)
            button_back.draw(window)

            self.draw_decorative_elements(window, width, height, center_x, center_y)

            # Labels
            s_lab = font_desc.render("SINGLE PLAYER", True, (255, 255, 255))
            window.blit(s_lab, (button_single.rectImg.centerx - 100, button_single.rectImg.top - 40))

            m_lab = font_desc.render("MULTIPLAYER", True, (255, 255, 255))
            window.blit(m_lab, (button_multi.rectImg.centerx - 80, button_multi.rectImg.top - 40))

            if button_single.state == "clicked":
                self.FadeOut(window, width, height)
                SceneManager.OpenScene("GameGreenLightSingle")
                running = False

            if button_multi.state == "clicked":
                self.FadeOut(window, width, height)
                SceneManager.OpenScene("GameGreenLightMulti")
                running = False

            if button_back.state == "clicked":
                self.FadeOut(window, width, height)
                SceneManager.OpenScene("Menu")
                running = False

            pygame.display.update()
            clock.tick(fps)

        pygame.quit()

    @staticmethod
    def draw_gradient_overlay(window, width, height):
        """Draw a subtle gradient overlay"""
        for y in range(height):
            alpha = int(255 * (y / height) * 0.1)  # Subtle gradient
            color = (20 + alpha, 20 + alpha, 40 + alpha)
            pygame.draw.line(window, color, (0, y), (width, y))

    @staticmethod
    def draw_decorative_elements(window, width, height, center_x, center_y):
        """Draw decorative visual elements"""
        # # Vertical lines
        # pygame.draw.line(window, (100, 100, 150), (center_x - 400, 250), (center_x - 400, height - 250), 3)
        # pygame.draw.line(window, (100, 100, 150), (center_x + 400, 250), (center_x + 400, height - 250), 3)
        #
        # # Horizontal accent lines
        # pygame.draw.line(window, (255, 100, 100), (100, center_y - 80), (width - 100, center_y - 80), 2)
        # pygame.draw.line(window, (100, 255, 100), (100, center_y + 280), (width - 100, center_y + 280), 2)

        # Corners
        corner_size = 50
        corner_color = (200, 50, 50)

        # Top left
        pygame.draw.line(window, corner_color, (50, 50), (50 + corner_size, 50), 3)
        pygame.draw.line(window, corner_color, (50, 50), (50, 50 + corner_size), 3)

        # Top right
        pygame.draw.line(window, corner_color, (width - 50, 50), (width - 50 - corner_size, 50), 3)
        pygame.draw.line(window, corner_color, (width - 50, 50), (width - 50, 50 + corner_size), 3)

        # Bottom left
        pygame.draw.line(window, corner_color, (50, height - 50), (50 + corner_size, height - 50), 3)
        pygame.draw.line(window, corner_color, (50, height - 50), (50, height - 50 - corner_size), 3)

        # Bottom right
        pygame.draw.line(window, corner_color, (width - 50, height - 50), (width - 50 - corner_size, height - 50), 3)
        pygame.draw.line(window, corner_color, (width - 50, height - 50), (width - 50, height - 50 - corner_size), 3)


if __name__ == "__main__":
    GameModeSelector()