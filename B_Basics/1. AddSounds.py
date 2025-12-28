"""
Two ways to play sounds

# Background Music
pygame.mixer.music.load('timer.mp3')
pygame.mixer.music.play()

# Sound Clip
soundClick = pygame.mixer.Sound('click.mp3')
soundClick.play()

"""

# Import
import pygame

# Initialize
pygame.init()

# Create Window/Display
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Awesome Game")

# Initialize Clock for FPS
fps = 30
clock = pygame.time.Clock()

# Sounds
pygame.mixer.pre_init()
pygame.mixer.music.load('../Resources/Sounds/timer.mp3')
pygame.mixer.music.play()
soundClick = pygame.mixer.Sound('../Resources/Sounds/click.mp3')

# Variables
counter = 0

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
    counter += 1
    if counter > 60:
        soundClick.play()
        counter = 0

    # Update Display
    pygame.display.update()
    # Set FPS
    clock.tick(fps)
