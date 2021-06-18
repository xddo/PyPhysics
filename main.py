import pygame
import Particle

def display(particle):
    pygame.draw.circle(screen, particle.color, (particle.x, particle.y), particle.size, particle.thickness)

# Set up pygame
pygame.init()
width = 640
height = 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('PyPhysics')

# Set up environment class
env = Particle.Environment(width, height)
env.add_particles(25)

running = True
clock = pygame.time.Clock()
selected_particle = None
LEFT, RIGHT = 1, 3
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT:
                selected_particle = env.find_particle(pygame.mouse.get_pos())
            if event.button == RIGHT:
                env.add_particle(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
            selected_particle = None

    # If clicking on particle,
    # Get mouse's (x, y) position,
    # Find distance from particle -> mouse position,
    # Then, create vector (angle, length) that joins the two points
    # This allows particle to be released w/ speed equal to mouse speed at time of release
    if selected_particle:
        selected_particle.mouse(pygame.mouse.get_pos())

    env.update()
    screen.fill(env.color)

    for p in env.particles:
        display(p)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()