import pygame
class Particle:
    def __init__(self, coordinates, size):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.size = size
        self.color = (255, 0, 0)
        self.thickness = 1

def display(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size, self.thickness)

(width, height) = (400, 400)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Physics Simulation")
screen.fill(WHITE)

first_particle = Particle((100, 50), 5)
display(first_particle)

pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
