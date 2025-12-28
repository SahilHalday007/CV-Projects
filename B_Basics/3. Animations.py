# Import
import pygame
import math

# Initialize
pygame.init()

# Create Window/Display
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Animations")

# Initialize Clock for FPS
fps = 30
clock = pygame.time.Clock()

# Variables
counter = 0

class Dinosaur:
    def __init__(self, pos, path, scale=1, grid=(2, 4),
                 animationFrames=None, speedAnimation=1):
        # Loading Main Image
        img = pygame.image.load(path).convert_alpha()
        width, height = img.get_size()
        img = pygame.transform.smoothscale(img, (int(width * scale), int(height * scale)))

        # Split image to get all frames
        if animationFrames is None:  # When animation frames is not defined then use all frames
            animationFrames = grid[0] * grid[1]
        widthSingleFrame = width / grid[1]
        heightSingleFrame = height / grid[0]
        self.imgList = []
        counter = 0
        for row in range(grid[0]):
            for col in range(grid[1]):
                counter += 1
                if counter <= animationFrames:
                    imgCrop = img.subsurface((col * widthSingleFrame, row * heightSingleFrame,
                                              widthSingleFrame, heightSingleFrame))
                    self.imgList.append(imgCrop)

        self.img = self.imgList[0]
        self.rectImg = self.img.get_rect()
        self.rectImg.x, self.rectImg.y = pos[0], pos[1]
        self.pos = pos
        self.path = path
        self.animationCount = 0
        self.speedAnimation = speedAnimation
        self.isAnimating = False


    def draw(self, window):
        if self.isAnimating:
            if math.floor(self.animationCount) != len(self.imgList) - 1:
                self.animationCount += self.speedAnimation
            else:
                self.animationCount = 0
            self.img = self.imgList[math.floor(self.animationCount)]
        else:
            self.img = self.imgList[0]
        window.blit(self.img, self.rectImg)


# Create Objects
dino1 = Dinosaur((100, 100), '../Resources/Animations/DinosaurRun.png',
                 speedAnimation=0.4)
dino2 = Dinosaur((400, 100), '../Resources/Animations/DinosaurWalk.png',
                 grid=(3,4),animationFrames=10,speedAnimation=0.4)
dino3 = Dinosaur((100, 400), '../Resources/Animations/DinosaurJump.png',
                 grid=(3,4),speedAnimation=0.4)
dino4 = Dinosaur((400, 400), '../Resources/Animations/DinosaurDead.png',
                 grid=(3,4),animationFrames=8,speedAnimation=0.4)

# Main loop
start = True
while start:
    # Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    # Apply Logic
    window.fill((255, 255, 255))
    dino1.draw(window)
    dino2.draw(window)
    dino3.draw(window)
    dino4.draw(window)

    counter +=1
    if counter>50:
        dino1.isAnimating = not dino1.isAnimating
        counter = 0


    # Update Display
    pygame.display.update()
    # Set FPS
    clock.tick(fps)
