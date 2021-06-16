import pygame
import random
import math
import time 

GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

class Particle:
    '''
    @ Particle - 
        1. (x, y) position
        2. circle size (radius)
    @ Functions
        display()
    '''
    def __init__(self, position, size):
        self.x, self.y = position
        self.size = size
        self.speed = 0.01
        self.angle = math.pi / 2
        self.color = GREEN
        self.thickness = 1
    
    def display(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size, self.thickness)
    
    # Changes x, y position based on speed/angle (velocity)
    # Subtract from y to account for downward pointing y-axis
    # Angles in radians
    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed

    def bounce(self):
        if self.x > width - self.size:
            self.x = 2 * (width - self.size) - self.x
            self.angle = -self.angle
        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = -self.angle
        
        if self.y > height - self.size:
            self.y = 2 * (height - self.size) - self.y 
            self.angle = math.pi - self.angle
        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle

pygame.init()
width = 640
height = 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('PyPhysics')

number_particles = 10
particles = []

for i in range(number_particles):
        size = random.randint(15, 25)
        x = random.randint(size, width - size) 
        y = random.randint(size, height - size)

        temp = Particle((x, y), size)
        temp.speed = random.random()
        temp.angle = random.uniform(0, math.pi * 2)

        particles.append(temp)

running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    for p in particles:
        p.move()
        p.bounce()
        p.display()

    pygame.display.flip()
    time.sleep(0.0009)

pygame.quit()

