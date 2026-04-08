import random
import cvzone
import pygame
import SceneManager
import cv2
import numpy as np
from cvzone.PoseModule import PoseDetector
import time
from B_Basics.CustomClasses.Button import ButtonImg
import math
import Player


class UIElements:

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

def FadeTransition(window, width, height):
    """Smooth fade to black"""
    fade = pygame.Surface((width, height))
    fade.fill((0, 0, 0))
    for alpha in range(0, 300, 15): # Faster fade
        fade.set_alpha(alpha)
        window.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)


# Global UI instance
ui_elements = None


def draw_instruction_center(window, text, width, height):
    """Draw centered instruction text on window"""
    if ui_elements:
        ui_elements.draw_instruction(window, text)


def GameGreenLightMultiplayer(caps_in=None):
    """Enhanced Green Light Red Light game with 2-player split screen"""
    global ui_elements

    # Initialize
    pygame.init()
    pygame.event.clear()
    pygame.mixer.init()

    # Fade in from dark transition
    transition_alpha = 255
    transition_frames = 30
    transition_count = 0

    # Get fullscreen resolution
    screen_info = pygame.display.Info()
    width, height = screen_info.current_w, screen_info.current_h

    # Create Fullscreen Window
    window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    pygame.display.set_caption("Squid Game - Green Light Red Light (2 Player)")

    # Initialize UI
    ui_elements = UIElements(width, height)

    # Initialize Clock for FPS
    fps = 30
    clock = pygame.time.Clock()

    # Game Parameters
    thresholdDifficulty = 20
    widthStart = int(width * 0.35)
    widthEnd = int(width * 0.55)
    timeTotal = 45

    # Number of players
    num_players = 2
    players = [Player(i, cam_id=i) for i in range(num_players)]

    # Setup cameras
    camera_width = width // num_players
    for i, player in enumerate(players):
        player.update_camera(camera_width, height)
        print(f"Player {i + 1} using camera {i}")

    # Flags
    gameStarted = False
    timeStart = 0
    all_eliminated = False
    winners = []

    # Sounds
    soundShot = pygame.mixer.Sound("../../Resources/Sounds/shot.mp3")
    soundGreenLight = pygame.mixer.Sound("../../Resources/Sounds/GR-2.mp3")
    soundWin = pygame.mixer.Sound("../../Resources/Sounds/shot.mp3")

    # Buttons
    buttonBack = ButtonImg((width // 2 - 100, height - 150),
                           "../../Resources/Buttons/ButtonBack.png",
                           scale=0.6,
                           pathSoundClick="../../Resources/Sounds/click.mp3",
                           pathSoundHover="../../Resources/Sounds/hover.mp3")

    # Images
    imgGameWon = pygame.image.load("../../Resources/Project - SquidGame/Passed.png").convert()
    imgGameOver = pygame.image.load("../../Resources/Project - SquidGame/Eliminated.png").convert()

    # Scale images to fullscreen
    imgGameWon = pygame.transform.scale(imgGameWon, (width, height))
    imgGameOver = pygame.transform.scale(imgGameOver, (width, height))

    # Main loop
    start = True
    game_active = True

    while start:
        # Handle fade transition
        if transition_count < transition_frames:
            transition_alpha = 255 - (transition_count / transition_frames) * 255
            transition_count += 1

        # Get Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_active = False
                    for player in players:
                        player.release()
                    start = False

        # Apply Logic
        if game_active and not all_eliminated and winners == []:

            # Check all players
            active_players = [p for p in players if not p.gameOver and not p.gameWon]

            if len(active_players) == 0:
                all_eliminated = True

            # Process each player
            for player_idx, player in enumerate(players):
                if player.gameOver or player.gameWon:
                    continue

                success, img = player.read_frame()
                if not success:
                    print(f"Failed to read frame from camera {player.cam_id}")
                    continue

                # Find Body
                img = player.detector.findPose(img, draw=False)
                lmList, bboxInfo = player.detector.findPosition(img, draw=False)

                # Get image subtraction
                mask = player.subtractor.apply(img, 1)

                if bboxInfo:
                    x, y, w, h = bboxInfo['bbox']
                    player.bbox = (x, y, w, h)
                    player.detected = True

                    # If game has not started
                    if not player.gameStart and not gameStarted:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)
                        if w < widthStart:
                            player.gameStart = True
                            # Start game when both players are ready
                            if all(p.gameStart for p in players if not p.gameOver and not p.gameWon):
                                gameStarted = True
                                timeStart = time.time()
                                for p in players:
                                    p.timeStart = timeStart

                    # Game is active
                    elif gameStarted:
                        # Find the time Remaining
                        timeLeft = int(timeTotal - (time.time() - timeStart))

                        # Check the number of white pixels in the body region
                        imgMaskCrop = mask[y:y + h, x:x + w]
                        ret, imgThreshold = cv2.threshold(imgMaskCrop, 20, 255, cv2.THRESH_BINARY)
                        whitePixels = cv2.countNonZero(imgThreshold)

                        # Check if movement is present
                        if whitePixels > w * thresholdDifficulty:
                            colorMotion = (0, 0, 255)  # Red - moving
                        else:
                            colorMotion = (0, 255, 0)  # Green - still

                        # Draw thicker bounding box
                        cv2.rectangle(img, (x, y), (x + w, y + h), colorMotion, 5)

                        # If Green Light
                        if player.greenLight:
                            if player.greenFirstFrame:
                                soundGreenLight.play()
                                player.timeStartGreen = time.time()
                                player.greenFirstFrame = False
                            else:
                                if time.time() - player.timeStartGreen > 2:
                                    player.greenLight = False
                                    player.randomDelay = random.randint(30, 50)

                            # Check if reached finish line
                            if w > widthEnd:
                                player.gameWon = True
                                winners.append(player.id)
                                soundWin.play()

                        # If Red Light
                        else:
                            player.countRed += 1
                            if player.countRed > player.randomDelay:
                                player.greenLight = True
                                player.greenFirstFrame = True
                                player.countRed = 0

                            # Check for motion during red light
                            if whitePixels > w * thresholdDifficulty:
                                player.gameStart = False
                                player.gameOver = True
                                soundShot.play()

                        # Check if the time limit is up
                        if timeLeft <= 0:
                            player.gameOver = True
                            soundShot.play()

                # Display the frame - SPLIT SCREEN
                img_height, img_width = img.shape[:2]
                img_resized = cv2.resize(img, (camera_width, height))

                # Convert to pygame format
                imgRGB = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
                imgRGB = np.rot90(imgRGB)
                frame = pygame.surfarray.make_surface(imgRGB).convert()
                frame = pygame.transform.flip(frame, True, False)

                # Position player frame
                x_pos = player_idx * camera_width
                window.blit(frame, (x_pos, 0))

                # Draw vertical line separator
                if num_players == 2:
                    pygame.draw.line(window, (0, 255, 255), (width // 2, 0), (width // 2, height), 4)

                # Draw instruction if needed
                if bboxInfo and not player.gameStart and not gameStarted:
                    x, y, w, h = bboxInfo['bbox']
                    if w >= widthStart:
                        player_center_x = (player_idx * camera_width) + (camera_width // 2)
                        font = pygame.font.Font(None, 50)
                        text_surface = font.render(f"P{player.id + 1}: Move Back", True, (255, 200, 0))
                        padding = 20
                        bg_rect = text_surface.get_rect()
                        bg_rect.center = (player_center_x, height // 2 - 100)
                        bg_rect.inflate_ip(padding * 2, padding)

                        # Animated background
                        pulse = math.sin(ui_elements.frame_count * 0.05) * 3
                        pygame.draw.rect(window, (0, 0, 0), (bg_rect.x - int(pulse), bg_rect.y - int(pulse),
                                                             bg_rect.width + int(pulse * 2),
                                                             bg_rect.height + int(pulse * 2)), 0, border_radius=10)
                        pygame.draw.rect(window, (0, 255, 255), (bg_rect.x - int(pulse), bg_rect.y - int(pulse),
                                                                 bg_rect.width + int(pulse * 2),
                                                                 bg_rect.height + int(pulse * 2)), 3, border_radius=10)

                        text_rect = text_surface.get_rect(center=bg_rect.center)
                        window.blit(text_surface, text_rect)

            # Draw enhanced UI elements
            if gameStarted:
                timeLeft = int(timeTotal - (time.time() - timeStart))
                ui_elements.draw_timer(window, timeLeft, timeTotal)
                ui_elements.draw_light_indicator(window, players[0].greenLight)

            ui_elements.draw_player_status(window, players, num_players)

        # Game Over - All Eliminated
        elif all_eliminated and winners == []:
            window.blit(imgGameOver, (0, 0))
            buttonBack.draw(window)
            if buttonBack.state == 'clicked':
                for player in players:
                    player.release()
                SceneManager.OpenScene("Menu")

        # Game Won
        elif winners != []:
            window.blit(imgGameWon, (0, 0))

            # Draw winner info with animation
            winner_text = f"Player {winners[0] + 1} Wins!" if len(winners) == 1 else "Multiple Players Won!"
            bounce = math.sin(ui_elements.frame_count * 0.05) * 20

            font_win = pygame.font.Font(None, 100)
            win_surface = font_win.render(winner_text, True, (255, 215, 0))
            win_rect = win_surface.get_rect(center=(width // 2, height // 2 - 50 + int(bounce)))

            # Shadow effect
            shadow = font_win.render(winner_text, True, (0, 0, 0))
            window.blit(shadow, (win_rect.x + 3, win_rect.y + 3))
            window.blit(win_surface, win_rect)

            buttonBack.draw(window)
            if buttonBack.state == 'clicked':
                for player in players:
                    player.release()
                SceneManager.OpenScene("Menu")

        # Draw transition overlay
        ui_elements.draw_transition(window, transition_alpha)

        # Update Display
        pygame.display.update()
        clock.tick(fps)

    # Cleanup
    for player in players:
        player.release()
    pygame.quit()


def GameGreenLightSingleplayer():
    """Enhanced single player mode with beautiful UI"""
    global ui_elements

    # Initialize
    pygame.init()
    pygame.event.clear()

    # Fade in from dark transition
    transition_alpha = 255
    transition_frames = 30
    transition_count = 0

    # Get fullscreen resolution
    screen_info = pygame.display.Info()
    width, height = screen_info.current_w, screen_info.current_h

    # Create Fullscreen Window
    window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    pygame.display.set_caption("Squid Game - Green Light Red Light")

    # Initialize UI
    ui_elements = UIElements(width, height)

    # Initialize Clock for FPS
    fps = 30
    clock = pygame.time.Clock()

    # Webcam
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, width)
    cap.set(4, height)

    # Detector Body
    detector = PoseDetector()

    # Background Subtractor
    subtractor = cv2.createBackgroundSubtractorMOG2(3)

    # Flags
    gameStart, gameOver, gameWon = False, False, False
    greenLight, greenFirstFrame = True, True

    # Parameters
    thresholdDifficulty = 20
    widthStart = int(width * 0.35)
    widthEnd = int(width * 0.55)
    timeTotal = 30

    # Variable
    countRed = 0
    timeStart = 0

    # Sounds
    pygame.mixer.init()
    soundShot = pygame.mixer.Sound("../../Resources/Sounds/shot.mp3")
    soundGreenLight = pygame.mixer.Sound("../../Resources/Sounds/GR-2.mp3")

    # Buttons
    buttonBack = ButtonImg((width // 2 - 100, height - 150),
                           "../../Resources/Buttons/ButtonBack.png",
                           scale=0.6,
                           pathSoundClick="../../Resources/Sounds/click.mp3",
                           pathSoundHover="../../Resources/Sounds/hover.mp3")

    # Images
    imgGameWon = pygame.image.load("../../Resources/Project - SquidGame/Passed.png").convert()
    imgGameOver = pygame.image.load("../../Resources/Project - SquidGame/Eliminated.png").convert()
    imgGameWon = pygame.transform.scale(imgGameWon, (width, height))
    imgGameOver = pygame.transform.scale(imgGameOver, (width, height))

    # Main loop
    start = True
    while start:
        # Handle fade transition
        if transition_count < transition_frames:
            transition_alpha = 255 - (transition_count / transition_frames) * 255
            transition_count += 1

        # Get Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    cap.release()
                    SceneManager.OpenScene("Menu")

        # Apply Logic
        if gameOver is False and gameWon is False:
            success, img = cap.read()
            if not success:
                continue

            # Find Body
            img = detector.findPose(img, draw=False)
            lmList, bboxInfo = detector.findPosition(img, draw=False)

            # Get image subtraction
            mask = subtractor.apply(img, 1)

            if bboxInfo:
                x, y, w, h = bboxInfo['bbox']

                # If game has not started
                if gameStart is False:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)
                    if w < widthStart:
                        gameStart = True
                        timeStart = time.time()

                # After Game begins
                else:
                    # Find the time Remaining
                    timeLeft = int(timeTotal - (time.time() - timeStart))

                    # Check the number of white pixels in the body region
                    imgMaskCrop = mask[y:y + h, x:x + w]
                    ret, imgThreshold = cv2.threshold(imgMaskCrop, 20, 255, cv2.THRESH_BINARY)
                    whitePixels = cv2.countNonZero(imgThreshold)

                    # Check if movement is present
                    if whitePixels > w * thresholdDifficulty:
                        colorMotion = (0, 0, 255)
                    else:
                        colorMotion = (0, 255, 0)

                    # Draw thicker bounding box
                    cv2.rectangle(img, (x, y), (x + w, y + h), colorMotion, 5)

                    # If Green Light
                    if greenLight:
                        if greenFirstFrame:
                            soundGreenLight.play()
                            timeStartGreen = time.time()
                            greenFirstFrame = False
                        else:
                            if time.time() - timeStartGreen > 2:
                                greenLight = False
                                randomDelay = random.randint(30, 50)
                        if w > widthEnd:
                            gameWon = True

                    # If Red Light
                    else:
                        countRed += 1
                        if countRed > randomDelay:
                            greenLight = True
                            greenFirstFrame = True
                            countRed = 0

                        # Check for motion during red light
                        if whitePixels > w * thresholdDifficulty:
                            gameStart = False
                            gameOver = True
                            soundShot.play()

                    # Check if the time limit is up
                    if timeLeft <= 0:
                        gameOver = True
                        soundShot.play()

            # Displaying the final image
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgRGB = np.rot90(imgRGB)
            frame = pygame.surfarray.make_surface(imgRGB).convert()
            frame = pygame.transform.flip(frame, True, False)
            frame = pygame.transform.scale(frame, (width, height))
            window.blit(frame, (0, 0))

            if bboxInfo:
                x, y, w, h = bboxInfo['bbox']
                if not gameStart and not gameOver:
                    if w >= widthStart:
                        ui_elements.draw_instruction(window, "Move Back to Start", player_id=1)

            # Draw UI elements
            if gameStart and not gameOver:
                timeLeft = int(timeTotal - (time.time() - timeStart))
                ui_elements.draw_timer(window, timeLeft, timeTotal)
                ui_elements.draw_light_indicator(window, greenLight)

                # Create dummy player for status display
                class DummyPlayer:
                    def __init__(self):
                        self.id = 0
                        self.gameOver = False
                        self.gameWon = False

                dummy = DummyPlayer()
                ui_elements.draw_player_status(window, [dummy], 1)

        # Game Won
        elif gameOver is False and gameWon:
            window.blit(imgGameWon, (0, 0))

            # Animated winner text
            bounce = math.sin(ui_elements.frame_count * 0.05) * 20
            font_win = pygame.font.Font(None, 100)
            win_surface = font_win.render("YOU WIN!", True, (255, 215, 0))
            win_rect = win_surface.get_rect(center=(width // 2, height // 2 - 50 + int(bounce)))

            shadow = font_win.render("YOU WIN!", True, (0, 0, 0))
            window.blit(shadow, (win_rect.x + 3, win_rect.y + 3))
            window.blit(win_surface, win_rect)

            buttonBack.draw(window)
            if buttonBack.state == 'clicked':
                cap.release()
                SceneManager.OpenScene("Menu")

        # Game Over
        elif gameOver and gameWon is False:
            window.blit(imgGameOver, (0, 0))
            buttonBack.draw(window)
            if buttonBack.state == 'clicked':
                cap.release()
                SceneManager.OpenScene("Menu")

        # Draw transition overlay
        ui_elements.draw_transition(window, transition_alpha)

        # Update Display
        pygame.display.update()
        clock.tick(fps)

    cap.release()
    pygame.quit()


if __name__ == "__main__":
    # Choose between singleplayer and multiplayer
    GameGreenLightSingleplayer()
    # GameGreenLightMultiplayer()