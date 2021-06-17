import random, math

class Particle:
    def __init__(self, position, size, mass = 1):
        self.x, self.y = position
        self.size = size
        self.speed = 0
        self.angle = 0
        self.thickness = 0
        self.mass = mass
        self.drag = 1
        self.elasticity = 0.85
        self.color = (0, 255, 0)

    # Changes x, y position based on speed/angle (velocity)
    # Subtract from y to account for downward pointing y-axis
    # Drag accounted for each time unit
    # Angles in radians, calculated off Y axis
    def move(self, gravity=(math.pi, 0.002)):
        (self.angle, self.speed) = add_vectors((self.angle, self.speed), gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag
    
    def mouse(self, position):
        x, y = position
        dx = x - self.x
        dy = y - self.y
        self.angle = 0.5 * math.pi + math.atan2(dy, dx)
        self.speed = math.hypot(dx, dy) * 0.1 


class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.particles = []
        self.color=(0,0,0)
        self.mass_air = 0.2
        self.elasticity = 0.75
        self.acceleration = None

    def add_particles(self, n=1):
        for i in range(n):
            size = random.randint(3, 30)
            mass = random.randint(100, 10000)
            x = random.randint(size, self.width - size)
            y = random.randint(size, self.height - size)

            temp = Particle((x, y), size, mass)
            temp.speed = (random.random())
            temp.angle = random.uniform(0, math.pi * 2)
            temp.color = (0, 255, 0)
            temp.drag = (temp.mass/(temp.mass + self.mass_air)) ** temp.size

            self.particles.append(temp)

    # Moves particles, checks for collisions
    def update(self):
        for i, p in enumerate(self.particles):
            p.move()
            if self.acceleration:
                p.accelerate(self.acceleration)
            self.bounce(p)
            # For each particle ahead of current (p)...
            for p2 in self.particles[i + 1:]:
                collide(p, p2)

    # Boundaries @ x = 0, y = 0, x = width, y = height
    # First, calculate distance particle has exceeded boundary
    # -> d = self.x - (width - self.size)
    # Then, position is reflected in boundary
    # -> self.x = (width - self.size) - d
    def bounce(self, particle):
        # Find distance outside of boundary,
        # Then reflect position from boundary
        # Finally, set opposite angle

        # If x is outside of right boundary...
        if particle.x > self.width - particle.size:
            particle.x = 2 * (self.width - particle.size) - particle.x
            particle.angle = -particle.angle
            particle.speed *= self.elasticity
        
        # If x is outside of left boundary...
        elif particle.x < particle.size:
            particle.x = 2 * particle.size - particle.x
            particle.angle = -particle.angle
            particle.speed *= self.elasticity

        # Same as above, but angle is subtracted 180 degrees
        # If y is outside of bottom boundary...
        if particle.y > self.height - particle.size:
            particle.y = 2 * (self.height - particle.size) - particle.y
            particle.angle = math.pi - particle.angle
            particle.speed *= self.elasticity

        # If y is outside of top boundary...
        elif particle.y < particle.size:
            particle.y = 2 * particle.size - particle.y
            particle.angle = math.pi - particle.angle
            particle.speed *= self.elasticity
    
    def find_particle(self, position):
        x, y = position
        for p in self.particles:
            if math.hypot(p.x - x, p.y - y) <= p.size:
                return p
        return None

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

        elasticity = p1.elasticity * p2.elasticity
        p1.speed *= elasticity
        p2.speed *= elasticity

        overlap = 0.5 * (p1.size + p2.size - distance + 1)
        p1.x += math.sin(angle) * overlap
        p1.y -= math.cos(angle) * overlap
        p2.x -= math.sin(angle) * overlap
        p2.y += math.cos(angle) * overlap

