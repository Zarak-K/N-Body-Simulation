import numpy as np
import matplotlib.pyplot as plt

#Constants
AU = 1.495978707e11
sun_vel_inner = 0.19
sun_vel_outer = 15.8
sun_vel_all = 16
sun_loc = 8.5126e-3 * AU

#Simulation Time
days = 365
dt = 86400
T = dt*days

#Defining Planet class
class Planet:
    G = 6.67430e-11
    AU = 1.495978707e11
    
    #Initialization parameters for Planet class
    def __init__(self, name, location, velocity, mass, kinetic, momentum, time, color): 
        self.name = name
        self.location = location
        self.velocity = velocity
        self.mass = mass
        self.location_orbit = [] 
        self.velocity_orbit = [] 
        self.location_update = np.array([0, 0])
        self.velocity_update = np.array([0, 0])
        self.kinetic = kinetic
        self.momentum = momentum
        self.time = time
        self.time_list = []
        self.color = color
    
    #Class method for calculating net acceleration caused by other Planets within Planet class
    def acceleration(self, loc, planets):
        acceleration = np.array([0,0]) #Acceleration defined as 2D array
        for planet in planets:         #Looping through Planets in class, excluding self
            if self != planet: 
                radius = planet.location - loc 
                
                radius_mag = np.linalg.norm(radius)
                
                acceleration_mag = (self.G * planet.mass)/ \
                (radius_mag**2)
                
                acceleration = acceleration + acceleration_mag * \
                (radius/radius_mag) 
                
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
        
        location_update = self.location_update = \
        (dt/6)*(k1 + 2*k2 + 2*k3 + k4)
        velocity_update = self.velocity_update = \
        (dt/6)*(m1 + 2*m2 + 2*m3 + m4)
        
        return location_update, velocity_update
    
    #Calling RK4 and appending location and velocity updates to list
    #Calculations for kinetic energy and momentum from updated locations and velocities included    
    def update(self, planets):
        location_update, velocity_update = self.RK4(dt, planets)
        self.location = self.location + location_update
        self.velocity = self.velocity + velocity_update
        self.location_orbit.append(self.location)
        self.velocity_orbit.append(self.velocity)
        self.kinetic = 0.5 * self.mass * \
        (np.linalg.norm(self.velocity))**2
        
        self.momentum = self.mass * self.velocity[1]
     
    #Appending time at each update to list               
    def time_update(self):
        self.time = self.time + dt
        self.time_list.append(self.time)

#Initializing parameters for objects in Planet class                 
sun =      Planet( 'Sun',      np.array([0, 0]),            np.array([0, 0]),        1.98892 * 10**30, 0, 0, 0, 'salmon')
asteroid = Planet( 'Asteroid', np.array([-0.6*AU, 0.5*AU]), np.array([0, 20000]), 0.95 * 10**20,    0, 0, 0, 'brown')
mercury =  Planet( 'Mercury',  np.array([-0.39*AU, 0]),     np.array([0, 47360]),    3.285 * 10**23,   0, 0, 0, 'black')
venus =    Planet( 'Venus',    np.array([-0.7233*AU, 0]),   np.array([0, 35020]),    4.867 * 10**24,   0, 0, 0, 'grey')
earth =    Planet( 'Earth',    np.array([-1*AU,0]),         np.array([0, 29783]),    5.9742 * 10**24,  0, 0, 0, 'green')
mars =     Planet( 'Mars',     np.array([-1.524*AU,0]),     np.array([0, 24080]),    6.39 * 10**23,    0, 0, 0, 'red')
jupiter =  Planet( 'Jupiter',  np.array([-5.2026*AU, 0]),   np.array([0, 13060]),    1.89813 * 10**27, 0, 0, 0, 'orange')
saturn =   Planet( 'Saturn',   np.array([-9.5322*AU, 0]),   np.array([0, 9670]),     5.683 * 10**26,   0, 0, 0, 'gold')
uranus =   Planet( 'Uranus',   np.array([-19.22*AU, 0]),    np.array([0, 6790]),     8.681 * 10**25,   0, 0, 0, 'cyan')
neptune =  Planet( 'Neptune',  np.array([-30.07*AU, 0]),    np.array([0, 5450]),     1.024 * 10**26,   0, 0, 0, 'blue')    

#Defining which planets to include in simulation
planets = [sun, mercury, venus, earth, mars]

#For loop for calling class methods to update locations and velocities
for t in np.arange(0, T, dt):
    for planet in planets:
        planet.update(planets)
        planet.time_update()

#For loop for plotting updated locations for planets
for planet in planets:
    scale = 3e11
    x = [loc[0] for loc in planet.location_orbit]
    y = [loc[1] for loc in planet.location_orbit]
    plt.figure(2) 
    plt.scatter(x[-1], y[-1], color = planet.color, label = planet.name)
    plt.plot(x,y, color = planet.color) 
    plt.axis('square')
    plt.xlim(-scale, scale)
    plt.ylim(-scale, scale)
    plt.xlabel('Distance (m) in x')
    plt.ylabel('Distance (m) in y')
    plt.legend(fontsize  = 8)

plt.show()

