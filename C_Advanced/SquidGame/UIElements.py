import pygame
import math

class UIElements:
    """Handle all UI drawing and animations"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.frame_count = 0

        # Try to load custom font, fall back to default
        try:
            self.font_large = pygame.font.Font("../../Resources/Marcellus-Regular.ttf", 72)
            self.font_medium = pygame.font.Font("../../Resources/Marcellus-Regular.ttf", 48)
            self.font_small = pygame.font.Font("../../Resources/Marcellus-Regular.ttf", 36)
        except:
            self.font_large = pygame.font.Font(None, 72)
            self.font_medium = pygame.font.Font(None, 48)
            self.font_small = pygame.font.Font(None, 36)

    def draw_timer(self, window, time_left, time_total):
        """Draw animated timer with progress bar"""
        self.frame_count += 1

        # Timer position and dimensions
        timer_x = self.width - 250
        timer_y = 30
        timer_width = 200
        timer_height = 80

        # Calculate progress (0 to 1)
        progress = max(0, min(1, time_left / time_total))

        # Color based on time remaining
        if progress > 0.5:
            color = (0, 255, 100)  # Green
        elif progress > 0.25:
            color = (255, 165, 0)  # Orange
        else:
            color = (255, 0, 0)  # Red

        # Draw background box
        pygame.draw.rect(window, (20, 20, 40), (timer_x, timer_y, timer_width, timer_height), 0, border_radius=15)

        # Draw progress bar
        progress_width = int(timer_width * progress)
        pygame.draw.rect(window, color, (timer_x + 5, timer_y + 5, progress_width - 10, timer_height - 10), 0,
                         border_radius=10)

        # Draw border
        pygame.draw.rect(window, color, (timer_x, timer_y, timer_width, timer_height), 3, border_radius=15)

        # Draw pulsing effect when time is low
        if time_left <= 5 and time_left > 0:
            pulse = math.sin(self.frame_count * 0.2) * 2
            pygame.draw.rect(window, (255, 0, 0),
                             (timer_x - pulse, timer_y - pulse, timer_width + pulse * 2, timer_height + pulse * 2), 2,
                             border_radius=15)

        # Draw time text
        time_text = self.font_medium.render(f"{max(0, time_left)}s", True, (255, 255, 255))
        text_rect = time_text.get_rect(center=(timer_x + timer_width // 2, timer_y + timer_height // 2))

        # Add shadow effect
        shadow_text = self.font_medium.render(f"{max(0, time_left)}s", True, (0, 0, 0))
        window.blit(shadow_text, (text_rect.x + 2, text_rect.y + 2))
        window.blit(time_text, text_rect)

    def draw_player_status(self, window, players, player_count):
        """Draw animated player status badges"""
        for idx, player in enumerate(players):
            # Position based on player count
            if player_count == 1:
                x_pos = 30
                y_pos = 30
            else:
                x_pos = (idx * self.width // player_count) + 30
                y_pos = 30

            # Determine status and color
            if player.gameWon:
                status = "WON"
                color = (255, 215, 0)  # Gold
                bg_color = (50, 50, 0)
            elif player.gameOver:
                status = "ELIMINATED"
                color = (255, 50, 50)  # Red
                bg_color = (50, 20, 20)
            else:
                status = "ALIVE"
                color = (100, 255, 100)  # Green
                bg_color = (20, 50, 20)

            # Draw status box
            status_text = self.font_small.render(f"Player {player.id + 1}", True, color)
            status_sub = self.font_small.render(status, True, color)

            # Background box
            box_width = max(status_text.get_width(), status_sub.get_width()) + 30
            box_height = status_text.get_height() + status_sub.get_height() + 20

            pygame.draw.rect(window, bg_color, (x_pos - 10, y_pos - 10, box_width, box_height), 0, border_radius=10)
            pygame.draw.rect(window, color, (x_pos - 10, y_pos - 10, box_width, box_height), 2, border_radius=10)

            # Draw text
            window.blit(status_text, (x_pos, y_pos))
            window.blit(status_sub, (x_pos, y_pos + status_text.get_height() + 5))

    def draw_light_indicator(self, window, is_green_light):
        """Draw animated green/red light indicator"""
        indicator_x = self.width // 2 - 50
        indicator_y = self.height - 120
        indicator_size = 60

        if is_green_light:
            color = (0, 255, 0)
            text = "GREEN LIGHT"
            text_color = (0, 255, 0)
        else:
            # Pulsing red light
            pulse = math.sin(self.frame_count * 0.15) * 50 + 150
            color = (int(pulse), 0, 0)
            text = "RED LIGHT"
            text_color = (255, 0, 0)

        # Draw circle
        pygame.draw.circle(window, color, (indicator_x + indicator_size // 2, indicator_y + indicator_size // 2),
                           indicator_size // 2)
        pygame.draw.circle(window, (200, 200, 200),
                           (indicator_x + indicator_size // 2, indicator_y + indicator_size // 2), indicator_size // 2,
                           3)

        # Draw text
        light_text = self.font_medium.render(text, True, text_color)
        text_rect = light_text.get_rect(center=(self.width // 2, indicator_y + indicator_size + 40))
        window.blit(light_text, text_rect)

    def draw_instruction(self, window, text, player_id=None):
        """Draw beautiful centered instruction"""
        font = pygame.font.Font(None, 60)
        text_surface = font.render(text, True, (255, 200, 0))

        padding = 30
        bg_rect = text_surface.get_rect()
        bg_rect.center = (self.width // 2, self.height // 2 - 100)
        bg_rect.inflate_ip(padding * 2, padding)

        # Pulsing background
        pulse = math.sin(self.frame_count * 0.05) * 5

        # Draw semi-transparent background with glow
        bg_surface = pygame.Surface((bg_rect.width + int(pulse * 2), bg_rect.height + int(pulse * 2)), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 200))
        window.blit(bg_surface, (bg_rect.x - int(pulse), bg_rect.y - int(pulse)))

        # Draw border with glow
        pygame.draw.rect(window, (0, 255, 255),
                         (bg_rect.x - int(pulse), bg_rect.y - int(pulse),
                          bg_rect.width + int(pulse * 2), bg_rect.height + int(pulse * 2)), 3, border_radius=15)

        text_rect = text_surface.get_rect(center=bg_rect.center)
        window.blit(text_surface, text_rect)

    def draw_transition(self, window, alpha):
        """Draw fade transition overlay"""
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(alpha)))
        window.blit(overlay, (0, 0))