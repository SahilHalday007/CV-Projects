import pygame
import numpy as np
import cv2
import os
import random
import time
from cvzone.HandTrackingModule import HandDetector
from B_Basics.CustomClasses.Button import ButtonImg
import Scene_manager


class Balloon:
    def __init__(self, pos, path_img=None, scale=1, grid=(2, 4),
                 animation_frames=None, animation_speed=1, speed=1, path_sound=None):

        # load images
        img = pygame.image.load(path_img).convert_alpha()
        width, height = img.get_size()
        img = pygame.transform.smoothscale(img, (int(width * scale), int(height * scale)))
        width, height = img.get_size()

        # split images for frames
        if animation_frames is None:
            animation_frames = grid[0] * grid[1]
        width_single_frame = width / grid[1]
        height_single_frame = height / grid[0]
        self.img_list = []
        counter = 0

        for row in range(grid[0]):
            for col in range(grid[1]):
                counter += 1
                if counter <= animation_frames:
                    img_crop = img.subsurface((col * width_single_frame, row * height_single_frame,
                                                    width_single_frame, height_single_frame))
                    self.img_list.append(img_crop)

        self.img = self.img_list[0]
        self.img_rect = self.img.get_rect()
        self.img_rect.x, self.img_rect.y = pos[0], pos[1]
        self.pos = pos
        self.path = path_img
        self.animation_count = 0
        self.animation_speed = animation_speed
        self.is_animating = False
        self.speed = speed
        self.sound_path = path_sound
        if self.sound_path:
            self.sound_pop = pygame.mixer.Sound(self.sound_path)
        self.pop = False

    def draw(self, window):
        if self.is_animating is False:
            self.img_rect.y -= self.speed
        window.blit(self.img, self.img_rect)

    def check_pop(self, x, y):
        # check for hit
        if self.img_rect.collidepoint(x, y) and self.is_animating is False:
            self.is_animating = True
            if self.sound_path:
                self.sound_pop.play()

        if self.is_animating:
            if self.animation_count != len(self.img_list) - 1:
                self.animation_count += 1
                self.img = self.img_list[self.animation_count]
            else:
                self.pop = True

        if self.pop:
            return self.img_rect.y
        else:
            return None


def Game():
    # Initialize
    pygame.init()
    pygame.event.clear()

    # Create Window/Display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("MACHO MACHO")

    # Initialize Clock for FPS
    fps = 30
    clock = pygame.time.Clock()

    # variables
    balloons = []
    speed = 5
    score = 0
    start_time = time.time()
    generator_start_time = time.time()
    generator_delay = 1
    total_time = 30

    # load music
    pygame.mixer.pre_init()
    pygame.mixer.music.load("../../Resources/Project - Balloon Pop/BackgroundMusicGame.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()


    # create hand detector
    detector = HandDetector(maxHands=1, detectionCon=0.8)

    # load image
    img_score = pygame.image.load("../../Resources/Project - Balloon Pop/BackgroundScore.png")

    # button
    back_button = ButtonImg((578, 450), '../../Resources/Project - Balloon Pop/ButtonBack.png',
                           pathSoundClick='../../Resources/Sounds/click.mp3',
                           pathSoundHover='../../Resources/Sounds/hover.mp3',
                           scale=0.5)

    # webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    # get balloon paths
    path_balloon_folder = "../../Resources/Project - Balloon Pop/Balloons/"
    path_list_balloon = os.listdir(path_balloon_folder)


    # function for generating balloons
    def generate_balloon():
        random_balloon_path = path_list_balloon[random.randint(0, len(path_list_balloon) - 1)]
        x = random.randint(100, img.shape[1] - 100)
        y = img.shape[0]
        random_scale = round(random.uniform(0.3, 0.7))
        balloons.append(Balloon((x, y), path_img=os.path.join(path_balloon_folder, random_balloon_path),
                                grid=(3, 4), scale=random_scale, speed=speed, path_sound="../../Resources/Project - Balloon Pop/Pop.wav"))


    # Main loop
    start = True
    while start:
        # Get Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()

        # check if time is up
        time_remaining = total_time - (time.time() - start_time)

        if time_remaining < 0:
            window.blit(img_score, (0, 0))
            font = pygame.font.Font("../../Resources/Marcellus-Regular.ttf")
            text_score = font.render(f"Score: {text_score}", True, (255, 255,255))
            text_score_rect = text_score.get_rect(center=(1280 / 2, 720 / 2))
            window.blit(text_score, text_score_rect)
            back_button.draw(window)
            if back_button.state == "clicked":
                pygame.mixer.music.stop()
                Scene_manager.open_scene("Menu")

        else:
            # Apply Logic
            # openCV
            success, img = cap.read()
            img = cv2.flip(img, 1)
            hands, img = detector.findHands(img, draw=False, flipType=False)


            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgRGB = np.rot90(imgRGB)
            frame = pygame.surfarray.make_surface(imgRGB).convert()
            frame = pygame.transform.flip(frame, True, False)
            window.blit(frame, (0, 0))

            if hands:
                hand = hands[0]
                x, y = hand["lmList"][8][:2]
                pygame.draw.circle(window, (0, 200, 0), (x, y), 20)
                pygame.draw.circle(window, (200, 200, 200), (x, y), 16)
            else:
                x, y = 0, 0


            for i, balloon in enumerate(balloons):
                if balloon:
                    balloon_score = balloon.check_pop()
                    if balloon_score:
                        score += balloon_score // 10
                        balloons[i] = False
                    balloon.draw(window)

            if time.time() - generator_start_time > generator_delay:
                generator_delay = random.uniform(0.3, 0.8)
                generate_balloon()
                generator_start_time = time.time()
                speed += 1

            font = pygame.font.Font("../../Resources/Marcellus-Regular.ttf", 50)
            text_score = font.render(f"Score: {score}", True, (255, 255, 255))
            txt_time = font.render(f"Time: {int(time_remaining)}", True, (255, 255, 255))
            pygame.draw.rect(window, (200, 0, 200), (10, 10, 300, 70), border_radius=20)
            pygame.draw.rect(window, (200, 0, 200), (950, 10, 300, 70), border_radius=20)
            window.blit(text_score, (40, 13))
            window.blit(txt_time, (1000, 13))


        # Update Display
        pygame.display.update()
        # Set FPS
        clock.tick(fps)


if __name__ == "__main__":
    Game()