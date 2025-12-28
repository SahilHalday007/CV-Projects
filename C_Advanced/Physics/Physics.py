# Import
import pygame
import pymunk

# Initialize
pygame.init()

# Create Window/Display
width, height = 800, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Physics")

# Initialize Clock for FPS
fps = 30
clock = pygame.time.Clock()

# Physics
# 1. Space  2. Body  3. Shape  4. Add To Space  5. Display
# 1. Space
space = pymunk.Space()
space.gravity = 0.0, -1000.0

# 2. Body
body = pymunk.Body()
body.position = 500, 800
bodySegment = pymunk.Body(body_type=pymunk.Body.STATIC)

# 3. Shape
shape = pymunk.Circle(body, 50)
shape.density = 1
shape.elasticity = 0.5
shapeSegment = pymunk.Segment(bodySegment, (0, 150), (800, 50), 5)
shapeSegment.elasticity = 1

# 4. Add to Space
space.add(body, shape)
space.add(bodySegment, shapeSegment)

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

    # 5. Display
    x, y = body.position[0], height - body.position[1]
    pygame.draw.circle(window, (255, 0, 0), (int(x), int(y)), 50)
    pygame.draw.line(window, (0, 0, 0), (0, 650), (800, 750), 5)

    # Update Display
    pygame.display.update()
    # Set FPS
    clock.tick(fps)
    # Pymunk Step
    space.step(1 / fps)
