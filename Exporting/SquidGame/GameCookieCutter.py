# Import
import pickle
import pygame
import SceneManager
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from myUtils import *
from Button import ButtonImg
import sys


def Game():
    # Initialize
    pygame.init()
    pygame.event.clear()

    # Create Window/Display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Cookie Cutter")

    # Initialize Clock for FPS
    fps = 30
    clock = pygame.time.Clock()

    # Webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # width
    cap.set(4, 720)  # height

    # Images
    imgCookie = cv2.imread("Resources/Project - SquidGame/cookie.png")
    imgCookieCrack = cv2.imread("Resources/Project - SquidGame/cookieCut.png")
    imgGameOver = cv2.imread("Resources/Project - SquidGame/Eliminated.png")
    imgGameWon = cv2.imread("Resources/Project - SquidGame/Passed.png")

    # Hand Detector
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    # Flags
    gameStart, gameOver, gameWon = False, False, False

    # Parameter
    difficulty = 20  # lower is harder

    # Variables
    colorIndex = (0, 0, 255)
    countRed = 0
    countCrack = 0
    countPath = 0
    pointsCut = []  # Stores all values of index finger

    # Load path
    with open('Resources/path', 'rb') as f:
        pathMain = pickle.load(f)
    pointCrossList = [0] * len(pathMain)
    pathMainNP = np.array(pathMain, np.int32).reshape((-1, 1, 2))
    pathOuter = makeOffsetPoly(pathMain, difficulty)
    pathOuterNP = np.array(pathOuter, np.int32).reshape((-1, 1, 2))
    pathInner = makeOffsetPoly(pathMain, -difficulty)
    pathInnerNP = np.array(pathInner, np.int32).reshape((-1, 1, 2))

    # Sounds
    pygame.mixer.init()
    soundShot = pygame.mixer.Sound('Resources/Sounds/shot.mp3')
    soundCrack = pygame.mixer.Sound('Resources/Sounds/crack.wav')
    pygame.mixer.music.load("Resources/Sounds/timer.mp3")

    # Buttons
    buttonBack = ButtonImg((575, 475), "Resources/Buttons/ButtonBack.png", scale=0.6,
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
                if event.key == pygame.K_a:
                    SceneManager.OpenScene("Menu")
                if event.key == pygame.K_s:
                    gameStart = True
                    soundShot.play()
                    pygame.mixer.music.play()

        # Apply Logic

        # OpenCV
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands = detector.findHands(img, draw=False)

        if gameOver is False and gameWon is False:

            img = cv2.addWeighted(img, 0.35, imgCookie, 0.9, 0)

            # Display the paths
            img = cv2.polylines(img, [pathMainNP], True, (225, 225, 225), 5)
            # img = cv2.polylines(img, [pathOuterNP], True, (0, 200, 0), 5)
            # img = cv2.polylines(img, [pathInnerNP], True, (0, 200, 0), 5)

            if hands:
                hand = hands[0]
                index = hand['lmList'][8][0:2]

                if gameStart:

                    # Check if index finger is inside the region
                    resultOutter = cv2.pointPolygonTest(pathOuterNP, index, False)
                    resultInner = cv2.pointPolygonTest(pathInnerNP, index, False)

                    # print(resultOutter,resultInner)

                    # When index in the correct region
                    if resultOutter == 1 and resultInner == -1:
                        # print("Inside")
                        colorIndex = (0, 255, 0)
                        countRed = 0
                    else:
                        colorIndex = (0, 0, 255)
                        countRed += 1
                        if countRed > 3:
                            gameStart = False
                            gameOver = True
                            print("Outside")
                            soundCrack.play()
                            pygame.mixer.music.stop()

                    # Check how many points/lines  have been passed
                    pointsCut.append(index)
                    if isPointInLine([pathOuter[countPath], pathInner[countPath]], pointsCut[-1]):
                        pointCrossList[countPath] = 1
                        countPath += 1

                    # cv2.line(img, pathOuter[countPath], pathInner[countPath], (0, 0, 255), 5)

                    if len(set(pointCrossList[:-2])) == 1 and pointCrossList[0] != 0:
                        print("gameWon")
                        gameWon = True
                        pygame.mixer.music.stop()

                    # Draw the path that has been covered
                    for x in range(1, len(pathMain)):
                        if pointCrossList[x] == 1:
                            cv2.line(img, pathMain[x - 2], pathMain[x - 1], (0, 200, 0), 10)
                    print(pointCrossList)
                cv2.circle(img, index, 10, colorIndex, cv2.FILLED)

        elif gameOver and gameWon is False:
            countCrack += 1

            # delay before playing shot sound
            if countCrack == 20:
                soundShot.play()
            # delay before changing the image
            if countCrack > 50:
                img = imgGameOver
            else:
                img = cv2.addWeighted(img, 0.35, imgCookieCrack, 0.9, 0)

        elif gameOver is False and gameWon:
            img = imgGameWon

        # Display image
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, (0, 0))

        # add back button if game over or won
        if (gameOver and countCrack > 50) or gameWon:
            buttonBack.draw(window)
            if buttonBack.state == 'clicked':
                SceneManager.OpenScene("Menu")

        # Update Display
        pygame.display.update()
        # Set FPS
        clock.tick(fps)


if __name__ == "__main__":
    Game()
