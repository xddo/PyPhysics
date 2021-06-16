import pygame
import random
import math

GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

class Particle:
    '''
    @ Particle - 
        1. (x, y) position
        2. circle size (radius)
    @ Functions
        display()
        - Shows particle
        move()
        - Moves particle
        bounce()
        - Behavior for particle/boundary interaction
    '''

    def __init__(self, position, size, mass = 1):
        self.x, self.y = position
        self.size = size
        self.speed = 0
        self.angle = 0
        self.color = GREEN
        self.thickness = 1
        self.mass = mass
        # Drag = particle mass / total mass to the power of size X
        self.drag = (self.mass/(self.mass + mass_air)) ** self.size
    
    def display(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size, self.thickness)
    
    # Changes x, y position based on speed/angle (velocity)
    # Subtract from y to account for downward pointing y-axis
    # Drag accounted for each time unit
    # Angles in radians, calculated off Y axis
    def move(self):
        (self.angle, self.speed) = add_vectors((self.angle, self.speed), gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag

    # Boundaries @ x = 0, y = 0, x = width, y = height
    # First, calculate distance particle has exceeded boundary
    # -> d = self.x - (width - self.size)
    # Then, position is reflected in boundary
    # -> self.x = (width - self.size) - d
    def bounce(self):
        # Find distance outside of boundary,
        # Then reflect position from boundary
        # Finally, set opposite angle

        # If x is outside of right boundary...
        if self.x > width - self.size:
            self.x = 2 * (width - self.size) - self.x
            self.angle = -self.angle
            self.speed *= elasticity
        # If x is outside of left boundary...
        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = -self.angle
            self.speed *= elasticity

        # Same as above, but angle is subtracted 180 degrees
        # If y is outside of bottom boundary...
        if self.y > height - self.size:
            self.y = 2 * (height - self.size) - self.y 
            self.angle = math.pi - self.angle
            self.speed *= elasticity
        # If y is outside of top boundary...
        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

# add_vector()
# Parameters: two vectors (angle, length)
# Returns one vector (angle, length)
def add_vectors(vector1, vector2):
    angle1, length1 = vector1
    angle2, length2 = vector2

    # Find x, y coordinates for vector sum
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2

    # Length = hypotenuse of added vectors
    # Angle = arctan(y / x) - 90 degrees
    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return (angle, length)

# find_particle()
# Parameters: particles array, (x, y) position
# For each particle,
# Check if distance from mouse to particle's center < particle size
def find_particle(particles, x, y):
    for p in particles:
        if math.hypot(p.x - x, p.y - y) <= p.size:
            return p
    return None

# collide()
# Parameters: two particles
# Measures distance between p1 (x, y) and p2 (x, y) positions
# Checks if distance is less than combined radius (particle collision)
def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    distance = math.hypot(dx, dy)

    # Reference: https://en.wikipedia.org/wiki/Elastic_collision#One-dimensional_Newtonian
    # Take particle vector, add second vector whose angle is perpendicular to angle of collision,
    # As well as whose magnitude is based on momentum (mass * velocity) of second particle
    if distance < p1.size + p2.size:
        angle = math.atan2(dy, dx) + 0.5 * math.pi
        total_mass = p1.mass + p2.mass

        (p1.angle, p1.speed) = add_vectors((p1.angle, p1.speed * (p1.mass-p2.mass)/total_mass), (angle, 2 * p2.speed * p2.mass/total_mass))
        (p2.angle, p2.speed) = add_vectors((p2.angle, p2.speed * (p2.mass-p1.mass)/total_mass), (angle + math.pi, 2 * p1.speed * p1.mass / total_mass))

        p1.speed *= elasticity
        p2.speed *= elasticity

        overlap = 0.5 * (p1.size + p2.size - distance + 1)
        p1.x += math.sin(angle) * overlap
        p1.y -= math.cos(angle) * overlap
        p2.x -= math.sin(angle) * overlap
        p2.y += math.cos(angle) * overlap

pygame.init()
width = 640
height = 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('PyPhysics')

# Gravity vector
# Angle = 180 degrees (downward)
gravity = (math.pi, 0.002)
mass_air = 0.2

# Elasticity = loss of speed experienced when hitting boundary
elasticity = 0.75

number_particles = 100
particles = []

for i in range(number_particles):
        size = random.randint(1, 25)
        density = random.randint(1, 20)

        x = random.randint(size, width - size) 
        y = random.randint(size, height - size)

        # Mass = density * (size^2)
        temp = Particle((x, y), size, (density * size ** 2))
        temp.speed = random.random()
        temp.angle = random.uniform(0, math.pi * 2)
        # Color particle by varying shades depending on mass
        temp.color = (200 - density * 10, 200 - density * 10, 255)

        particles.append(temp)

running = True
clock = pygame.time.Clock()
selected_particle = None
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            (x_pos, y_pos) = pygame.mouse.get_pos()
            selected_particle = find_particle(particles, x_pos, y_pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None

    # If clicking on particle,
    # Get mouse's (x, y) position,
    # Find distance from particle -> mouse position,
    # Then, create vector (angle, length) that joins the two points
    # This allows particle to be released w/ speed equal to mouse speed at time of release
    if selected_particle:
        (x_pos, y_pos) = pygame.mouse.get_pos()
        dx = x_pos - selected_particle.x
        dy = y_pos - selected_particle.y
        selected_particle.angle = math.atan2(dy, dx) + 0.5 * math.pi
        selected_particle.speed = math.hypot(dx, dy) * 0.1

    screen.fill(BLACK)

    for i, p in enumerate(particles):
        p.move()
        p.bounce()
        # For each particle ahead of current (p)...
        for p2 in particles[i + 1:]:
            collide(p, p2)
        p.display()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()