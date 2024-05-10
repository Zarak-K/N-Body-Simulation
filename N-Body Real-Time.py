import pygame
import numpy as np
pygame.init()

#ZOOM IN AND OUT WITH ARROW KEYS

#Initializing window and text
width, height = 800, 800
win = pygame.display.set_mode((width, height),pygame.RESIZABLE)
pygame.display.set_caption('Orbit Simulation')
pause_text = pygame.font.SysFont('Consolas', 32).render('Pause :)', True, pygame.color.Color('White'))

#Constants
AU = 1.495978707e11
sun_loc = 8.5126e-3 * AU

#Timestep
days = 1
dt = 86400*days

#Colours
yellow = (255, 255, 0)
dark_grey = (80, 78, 81)
white = (255, 255, 255)
green = (0, 128, 0)
red = (255, 0, 0)
orange = (255, 140, 0)
gold = (255, 215, 0)
dark_blue = (0, 0, 139)
blue = (100, 149, 237)
brown = (139, 69, 19)

#Defining Planet Class
class Planet:
    G = 6.67430e-11
    AU = 1.495978707e11
    scale = 150 / AU
    
    #Initializing planet class with characteristics
    def __init__(self, name, location, velocity, mass, kinetic, momentum, color, size, vis): 
        self.name = name
        self.location = location
        self.velocity = velocity
        self.mass = mass
        self.color = color
        self.location_orbit = [] #Append updated locations to this list
        self.velocity_orbit = [] #Append updated velocities to this list
        self.location_update = np.array([0, 0])
        self.velocity_update = np.array([0, 0])
        self.kinetic = kinetic
        self.momentum = momentum
        self.size = size
        self.vis = vis
    
    #Defining function to draw locations onto pygame window
    def draw(self, win):
        x = self.location[0] * self.scale + width/2
        y = self.location[1] * self.scale + height/2
        
        if self.scale >= self.vis:
            if len(self.location_orbit) > 2: 
                updated_points = []
                for point in self.location_orbit:
                    x, y = point
                    x = x * self.scale + width/2
                    y = y * self.scale + height/2
                    updated_points.append((x, y))
            
                pygame.draw.lines(win,  self.color, False, updated_points, 2)
                pygame.draw.circle(win, self.color, (x,y), self.size)
    
    #Defining zoom function
    def zoom_in(self, win):
        self.scale += 10/AU
        if self.scale > 200/AU:
            self.scale -= 10/AU
        
    def zoom_out(self,win):
        self.scale -= 10/AU
        if self.scale < 10/AU:
            self.scale += 10/AU
    
    #Class method for calculating net acceleration caused by other Planets within Planet class
    def acceleration(self, loc, planets):
        acceleration = np.array([0,0]) 
        for planet in planets: 
            if self != planet: 
                radius = planet.location - loc 
                radius_mag = np.linalg.norm(radius)
                acceleration_mag = (self.G * planet.mass)/(radius_mag**2)
                acceleration = acceleration + acceleration_mag * (radius/radius_mag) 
        return acceleration
    
    #Applying RK4 to gain updates for location and velocity at each timestep          
    def RK4(self, dt, planets):
        k1 = self.velocity
        m1 = self.acceleration(self.location, planets)
        mid_point = self.location + k1 * (dt/2)
        k2 = self.velocity + m1*(dt/2)
        m2 = self.acceleration(mid_point, planets)
        mid_point2 = self.location + k2 * (dt/2)
        k3 = self.velocity + m2 * (dt/2)
        m3 = self.acceleration(mid_point2, planets)
        next_point = self.location + k3 * dt
        k4 = self.velocity + m3 * dt
        m4 = self.acceleration(next_point, planets)
        
        location_update = self.location_update = (dt/6)*(k1 + 2*k2 + 2*k3 + k4)
        velocity_update = self.velocity_update = (dt/6)*(m1 + 2*m2 + 2*m3 + m4)
        
        return location_update, velocity_update
    
    #Calling RK4 and appending location and velocity updates to list
    #Calculations for kinetic energy and momentum from updated locations and velocities included 
    def update(self, planets):

        location_update, velocity_update = self.RK4(dt, planets)
        self.location = self.location + location_update
        self.velocity = self.velocity + velocity_update
        self.location_orbit.append(self.location)
        self.velocity_orbit.append(self.velocity)
        self.kinetic = 0.5 * self.mass * (np.linalg.norm(self.velocity))**2
        self.momentum = self.mass * self.velocity[1]
        if len(self.location_orbit) > 1400:
            del self.location_orbit[0]

#Main function to run game loop
def main():
    sun_vel_inner = -0.19
    sun_vel_outer = -15.8
    sun_vel_all = -16
    sun_loc = 8.5126e-3 * AU
    scale = 150/AU
    run = True
    running, pause = 0, 1
    state = running
    clock = pygame.time.Clock()
    
    #Initializing characteristics of objects in planet class
    sun = Planet      ('Sun',       np.array([sun_loc, 0]),      np.array([0, sun_vel_all]),   1.98892 * 10**30, 0, 0, yellow,    18, 10/AU)
    asteroid1 = Planet('Asteroid1', np.array([-3.279*AU, 0]),    np.array([0, 16448]),         0.95 * 10**15,    0, 0, brown,     8,  10/AU) #2:1 resonance
    asteroid2 = Planet('Asteroid2', np.array([-2.502*AU, 0]),    np.array([0, 18832]),         0.95 * 10**15,    0, 0, brown,     8,  10/AU) #3:1 resonance
    asteroid3 = Planet('Asteroid3', np.array([-1.780*AU, 0]),    np.array([0, 22328]),         0.95 * 10**15,    0, 0, brown,     8,  10/AU) #5:1 resonance
    #asteroid4 = Planet('Asteroid4', np.array([-2.6*AU, 4.5*AU]), np.array([11274, 6554]),      0.95 * 10**15,    0, 0, brown,     8,  10/AU) #Lagrange point 
    #asteroid5 = Planet('Asteroid5', np.array([-3.972*AU, 0]),    np.array([0, 14947]),         0.95 * 10**15,    0, 0, brown,     8,  10/AU) #3:2 resonance
    mercury = Planet  ('Mercury',   np.array([-0.39*AU, 0]),     np.array([0, 47360]),         3.285 * 10**23,   0, 0, dark_grey, 10, 150/AU)
    venus = Planet    ('Venus',     np.array([-0.7233*AU, 0]),   np.array([0, 35020]),         4.867 * 10**24,   0, 0, white,     15, 120/AU)
    earth = Planet    ('Earth',     np.array([-1*AU,0]),         np.array([0, 29783]),         5.9742 * 10**24,  0, 0, dark_blue, 15, 80/AU)
    mars = Planet     ('Mars',      np.array([-1.524*AU,0]),     np.array([0, 24080]),         6.39 * 10**23,    0, 0, red,       12, 50/AU)
    jupiter = Planet  ('Jupiter',   np.array([-5.2026*AU, 0]),   np.array([0, 13060]),         1.98892 * 10**27, 0, 0, orange,    10, 10/AU)
    saturn = Planet   ('Saturn',    np.array([-9.5322*AU, 0]),   np.array([0, 9670]),          5.683 * 10**26,   0, 0, gold,      8, 10/AU)
    uranus = Planet   ('Uranus',    np.array([-19.22*AU, 0]),    np.array([0, 6790]),          8.681 * 10**25,   0, 0, blue,      8, 10/AU)
    neptune = Planet  ('Neptune',   np.array([-30.07*AU, 0]),    np.array([0, 5450]),          1.024 * 10**26,   0, 0, dark_blue, 8, 10/AU)
    
    #Selecting which planets to simulate
    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
    
    #Game loop
    while run:
        clock.tick(60)
        win.fill((0, 0, 0))
        
        #Enabling exiting the program by clicking X
        #Enabling pause
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = pause
                elif event.key == pygame.K_RETURN: 
                    state = running
        
        #Calling class methods to update locations and velocities of planets
        if state == running:                          
            for planet in planets:
                planet.update(planets)
                planet.draw(win)
                #print(sun.location)
                
                #Enabling zoom
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        planet.zoom_in(win)
                    
                    if event.key == pygame.K_DOWN:
                            planet.zoom_out(win)
                        
        elif state == pause:
            win.blit(pause_text, [100,100])

        pygame.display.update()
        
    pygame.quit()
    
main()
        
 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
