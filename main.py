import pygame

(width, height) = (400, 400)
BLACK = (255, 255, 255)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Physics Simulation")
screen.fill(BLACK)

pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
