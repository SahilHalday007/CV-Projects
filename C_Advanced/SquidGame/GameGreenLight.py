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
from Player import Player
from UIElements import UIElements


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