# Import
import pygame

# Initialize
pygame.init()
pygame.mixer.pre_init()

class ButtonImg:
    def __init__(self, pos, pathImg, scale=1,pathSoundHover=None, pathSoundClick=None):
        # Loading Main Image
        img = pygame.image.load(pathImg).convert_alpha()
        width, height = img.get_size()
        img = pygame.transform.smoothscale(img, (int(width * scale), int(height * scale)))

        # Split image to get all frames
        width, height = img.get_size()
        heightSingleFrame = int(height / 3)
        self.imgList = []

        for i in range(3):
            imgCrop = img.subsurface((0, i * heightSingleFrame,
                                      width, heightSingleFrame))
            self.imgList.append(imgCrop)

        self.pos = pos
        self.state = None
        self.img = self.imgList[0]
        self.rectImg = self.imgList[0].get_rect()
        self.rectImg.topleft = self.pos
        self.pathSoundClick = pathSoundClick
        self.pathSoundHover = pathSoundHover
        if self.pathSoundHover is not None:
            self.soundHover = pygame.mixer.Sound(self.pathSoundHover)
        if self.pathSoundClick is not None:
            self.soundClick = pygame.mixer.Sound(self.pathSoundClick)

    def draw(self, window):
        # Get mouse position to check if inside button
        posMouse = pygame.mouse.get_pos()
        self.img = self.imgList[0]
        if self.rectImg.collidepoint(posMouse):

            if pygame.mouse.get_pressed()[0]:
                self.img = self.imgList[2]  # Clicked
                if self.pathSoundClick is not None and self.state != "clicked":
                    self.soundClick.play()
                self.state = 'clicked'
            else:
                self.img = self.imgList[1]  # Hovering
                if self.pathSoundHover is not None and self.state != "hover" and self.state != "clicked":
                    self.soundHover.play()
                self.state = 'hover'
        else:
            self.state = None

        window.blit(self.img, self.rectImg)


if __name__ == "__main__":

    # Create Window/Display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("My Awesome Game")

    # Initialize Clock for FPS
    fps = 30
    clock = pygame.time.Clock()

    # Create Buttons
    button1 = ButtonImg((100, 100), "../../Resources/Buttons/ButtonBack.png", scale=0.5,
                        pathSoundClick="../../Resources/Sounds/click.mp3",
                        pathSoundHover="../../Resources/Sounds/hover.mp3")
    button2 = ButtonImg((500, 100), "../../Resources/Buttons/ButtonStart.png", scale=1,
                        pathSoundClick="../../Resources/Sounds/click.mp3",
                        pathSoundHover="../../Resources/Sounds/hover.mp3")


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
        button1.draw(window)
        button2.draw(window)
        # Update Display
        pygame.display.update()
        # Set FPS
        clock.tick(fps)
