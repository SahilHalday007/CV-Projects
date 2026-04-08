# VisualEffects.py - Enhanced visual effects and UI enhancements

import cv2
import numpy as np
import pygame
import cvzone


class ParticleEffect:
    """Create particle effects"""

    def __init__(self, x, y, velocity_x=0, velocity_y=0, lifetime=30, color=(0, 255, 0)):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.lifetime = lifetime
        self.initial_lifetime = lifetime
        self.color = color
        self.size = 5

    def update(self):
        """Update particle position"""
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.lifetime -= 1

    def is_alive(self):
        """Check if particle is still alive"""
        return self.lifetime > 0

    def draw(self, image):
        """Draw particle on image"""
        if self.is_alive():
            alpha = self.lifetime / self.initial_lifetime
            size = int(self.size * alpha)
            cv2.circle(image, (int(self.x), int(self.y)), size, self.color, -1)


class GameOverlay:
    """Create game overlays and UI elements"""

    @staticmethod
    def draw_timer_bar(image, time_left, time_total, height=40):
        """Draw a timer progress bar"""
        img_height, img_width = image.shape[:2]

        # Calculate bar dimensions
        bar_width = int(img_width * 0.8)
        bar_height = height
        bar_x = (img_width - bar_width) // 2
        bar_y = img_height - 100

        # Calculate progress
        progress = max(0, min(1, time_left / time_total))

        # Color based on time remaining
        if progress > 0.5:
            color = (0, 255, 0)  # Green
        elif progress > 0.25:
            color = (0, 165, 255)  # Orange
        else:
            color = (0, 0, 255)  # Red

        # Draw background
        cv2.rectangle(image, (bar_x, bar_y),
                      (bar_x + bar_width, bar_y + bar_height),
                      (50, 50, 50), -1)

        # Draw progress
        progress_width = int(bar_width * progress)
        cv2.rectangle(image, (bar_x, bar_y),
                      (bar_x + progress_width, bar_y + bar_height),
                      color, -1)

        # Draw border
        cv2.rectangle(image, (bar_x, bar_y),
                      (bar_x + bar_width, bar_y + bar_height),
                      (255, 255, 255), 2)

        return image

    @staticmethod
    def draw_status_badge(image, text, position, color=(0, 255, 0), scale=1.0):
        """Draw a status badge"""
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.0 * scale
        font_thickness = 2

        # Get text size
        (text_width, text_height), _ = cv2.getTextSize(
            text, font, font_scale, font_thickness
        )

        x, y = position
        padding = 10

        # Draw background rectangle
        cv2.rectangle(image,
                      (x - padding, y - padding - text_height),
                      (x + text_width + padding, y + padding),
                      color, -1)

        # Draw border
        cv2.rectangle(image,
                      (x - padding, y - padding - text_height),
                      (x + text_width + padding, y + padding),
                      (255, 255, 255), 2)

        # Put text
        cv2.putText(image, text, (x, y), font, font_scale, (0, 0, 0), font_thickness)

        return image

    @staticmethod
    def draw_heat_map(image, bbox, intensity):
        """Draw intensity heatmap around bounding box"""
        x, y, w, h = bbox

        # Create overlay
        overlay = image.copy()

        # Color based on intensity (red for high, green for low)
        if intensity > 0.7:
            color = (0, 0, 255)  # Red
        elif intensity > 0.4:
            color = (0, 165, 255)  # Orange
        else:
            color = (0, 255, 0)  # Green

        # Draw rectangle with transparency
        cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
        cv2.addWeighted(overlay, 0.3, image, 0.7, 0, image)

        return image

    @staticmethod
    def draw_pulse_effect(image, position, radius, color=(0, 255, 0), pulse_value=1.0):
        """Draw a pulsing circle effect"""
        x, y = position
        current_radius = int(radius * pulse_value)
        thickness = 2

        cv2.circle(image, (int(x), int(y)), current_radius, color, thickness)

        return image

    @staticmethod
    def draw_corner_indicators(image, width_ratio):
        """Draw corner indicators showing progress"""
        img_height, img_width = image.shape[:2]

        # Draw corner indicators
        corner_size = 50
        indicator_color = (0, 255, 0) if width_ratio > 0.5 else (0, 0, 255)

        # Top left
        cv2.rectangle(image, (0, 0), (corner_size, corner_size), indicator_color, 3)

        # Top right
        cv2.rectangle(image, (img_width - corner_size, 0),
                      (img_width, corner_size), indicator_color, 3)

        return image


class TransitionEffect:
    """Create smooth transitions between scenes"""

    def __init__(self, duration=30):
        self.duration = duration
        self.current_frame = 0

    def is_complete(self):
        """Check if transition is complete"""
        return self.current_frame >= self.duration

    def update(self):
        """Update transition"""
        self.current_frame += 1

    def get_alpha(self):
        """Get alpha value for fade effect"""
        return self.current_frame / self.duration

    def apply_fade_in(self, image):
        """Apply fade in effect"""
        alpha = self.get_alpha()
        output = cv2.addWeighted(image, alpha, image * 0, 1 - alpha, 0)
        return output

    def apply_fade_out(self, image):
        """Apply fade out effect"""
        alpha = 1 - self.get_alpha()
        output = cv2.addWeighted(image, alpha, image * 0, 1 - alpha, 0)
        return output


class CameraFilter:
    """Apply various camera filters"""

    @staticmethod
    def grayscale(image):
        """Convert to grayscale"""
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def blur(image, kernel_size=15):
        """Apply blur filter"""
        return cv2.blur(image, (kernel_size, kernel_size))

    @staticmethod
    def edge_detection(image):
        """Detect edges"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    @staticmethod
    def thermal_effect(image):
        """Apply thermal camera effect"""
        # Convert to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Split channels
        h, s, v = cv2.split(hsv)

        # Enhance saturation and value
        s = cv2.multiply(s, 1.5)
        s = np.clip(s, 0, 255)

        # Merge back
        result = cv2.merge([h, s, v])
        result = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

        return result

    @staticmethod
    def mirror_effect(image):
        """Mirror the image horizontally"""
        return cv2.flip(image, 1)

    @staticmethod
    def flip_effect(image):
        """Flip the image vertically"""
        return cv2.flip(image, 0)


class AnimatedText:
    """Create animated text effects"""

    def __init__(self, text, x, y, duration=60):
        self.text = text
        self.x = x
        self.y = y
        self.duration = duration
        self.current_frame = 0

    def update(self):
        """Update animation"""
        self.current_frame += 1

    def is_alive(self):
        """Check if animation is still active"""
        return self.current_frame < self.duration

    def draw_bounce(self, image):
        """Draw bouncing text"""
        import math
        progress = self.current_frame / self.duration
        bounce = math.sin(progress * math.pi) * 30

        y = int(self.y - bounce)
        cvzone.putTextRect(image, self.text, (self.x, y), scale=2, thickness=2)

        return image

    def draw_fade(self, image):
        """Draw fading text"""
        alpha = 1 - (self.current_frame / self.duration)

        # Create text overlay
        overlay = image.copy()
        cvzone.putTextRect(overlay, self.text, (self.x, self.y), scale=2, thickness=2)

        # Blend
        result = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
        return result

    def draw_scale(self, image):
        """Draw scaling text"""
        progress = self.current_frame / self.duration
        scale = 1 + (progress * 2)

        cvzone.putTextRect(image, self.text, (self.x, self.y), scale=scale, thickness=2)

        return image


class UIPanel:
    """Create UI panels for game info"""

    def __init__(self, x, y, width, height, title="", bg_color=(40, 40, 40)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.bg_color = bg_color
        self.items = []

    def add_item(self, label, value):
        """Add an item to the panel"""
        self.items.append((label, value))

    def draw(self, image):
        """Draw the panel"""
        # Draw background
        cv2.rectangle(image, (self.x, self.y),
                      (self.x + self.width, self.y + self.height),
                      self.bg_color, -1)

        # Draw border
        cv2.rectangle(image, (self.x, self.y),
                      (self.x + self.width, self.y + self.height),
                      (255, 255, 255), 2)

        # Draw title
        if self.title:
            cvzone.putTextRect(image, self.title,
                               (self.x + 10, self.y + 25),
                               scale=1.2, thickness=2)

        # Draw items
        item_y = self.y + 60
        for label, value in self.items:
            text = f"{label}: {value}"
            cvzone.putTextRect(image, text, (self.x + 15, item_y), scale=0.8)
            item_y += 30

        return image


# Example usage
def create_visual_effects_demo():
    """Demo of all visual effects"""

    # Create sample image
    image = np.zeros((720, 1280, 3), dtype=np.uint8)

    # Draw timer bar
    GameOverlay.draw_timer_bar(image, 20, 30)

    # Draw status badges
    GameOverlay.draw_status_badge(image, "ALIVE", (100, 100), (0, 255, 0))
    GameOverlay.draw_status_badge(image, "ELIMINATED", (400, 100), (0, 0, 255))

    # Create UI panel
    panel = UIPanel(50, 200, 300, 200, "GAME STATS", (30, 30, 60))
    panel.add_item("Score", "1250")
    panel.add_item("Time", "25s")
    panel.add_item("Players", "2")
    panel.draw(image)

    return image